import sim.memo.model as model
import sim.memo.link as link
import sim.memo.neuron as nrn
import sim.memo.spiketrain as stn
import sim.memo.distribution as distr

import sim.compiler.precompiler as precompiler
import sim.compiler as compiler
import sim.compiler.neuron as base
import sim.compiler.neuron.util.recorder as recorder

import sim.memo.microcircuit as mc

import sim.memo.neuron as nrn

import sim.nwbio as nwbio

from sim.compiler.neuron.modules import neuron_modules

from neuron import h

import pandas as pd

import numpy as np

import gc
gc.collect(2)

import sys

import warnings
warnings.filterwarnings("ignore")


def mk_vm_microcircuit_test(cellid,
                            lesioned_flag,
                            tstop=5000.0):

  
  cell =  nrn.Cell("TC", cellid=cellid, lesioned_flag=lesioned_flag)    

  InhSyn = nrn.Synapse("GABAA", erev=-75.0, tau=14.0)
  bgSyn = InhSyn()
  rtnSyn = InhSyn()
  drvSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=0.6)
  modSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=1.91)


  bgST = stn.SpikeTrain("regular", tstart=5000, number=1, mean_rate=10.0, time_unit="ms")
  rtnST = stn.SpikeTrain("regular", tstart=5000, number=1, mean_rate=10.0, time_unit="ms")
  drvST = stn.SpikeTrain("regular", tstart=5000, number=1, mean_rate=10.0, time_unit="ms")
  modST = stn.SpikeTrain("regular", tstart=5000, number=1, mean_rate=10.0, time_unit="ms")

  si_drv = SynapticInputs("driver", drvSyn, drvST, cell)
  si_mod = SynapticInputs("modulator", modSyn, modST, cell)
  si_bg_sync = SynapticInputs("nigral", bgSyn, bgST, cell)
  si_bg_async = SynapticInputs("nigral", bgSyn, bgST, cell)
  si_rtn = SynapticInputs("reticular", rtnSyn, rtnST, cell)

  i2t = InputToThalamus("InputToVMThalamus", cell, si_drv, si_mod, si_bg_sync, si_bg_async, si_rtn)

  i2t.n_nigral    =  17
  i2t.n_reticular = 7
  i2t.n_modulator = 346
  i2t.n_driver    = 35
  
  vmcircuit = mc.MicroCircuit("VMThalamus")
  vmcircuit.add(i2t)

  return vmcircuit, i2t


bodor_et_al2008 = {
    "xlabels":[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 'somatic'],
    "weights":np.array([5.33673534681342, 10.590606603532123, 24.91409649347326, 8.85334015868954, 16.012285641156904, 5.302981827489134, 5.387125671871004, 3.6572178141796883, 8.91140900947019, 1.739665984131058, 1.733267212695175, 6.980899667263891])
    }
bodor_et_al2008["weights"] /= np.sum(bodor_et_al2008["weights"])

gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()

from thalamocortical_cell import Cell


compiler.register_object(base, Cell)


class SynapticInputs(nrn.Model):

  def __init__(self, name, syn, spktr, cell, distribution=None, target=None, **kwargs):
    """
        Represent a set of synaptic inputs to the thalamocortical cells
        name: identifier of the inputs ('driver', 'modulator', 'nigral', 'reticular')
        syn: model of synapse
        spktr: model of spike train
        cell: cell model
        distribution: information on the distribution (default:None)
        target: morphological information on the postsynaptic target (default:None)
    """

    # check synaptic input names
    assert name == 'driver' or name == 'modulator' or name == 'nigral' or name == 'reticular'

    model.Model.__init__(self, name, **kwargs)

    self.syn = nrn.SynapseGroup("syn", syn=syn)
    self.spktr = stn.SpikeTrainPopulation("spktr", spktr=spktr)
    self.spktr2syn = link.Link(self.spktr, self.syn)

    self.cell = cell

    if distribution is None:
        distribution = { "driver":distr.Distribution("uniform"),
                        "modulator":distr.Distribution("uniform"),
                        "reticular":distr.Distribution("uniform"),
                        "nigral":distr.Distribution("empirical", x=bodor_et_al2008["xlabels"], freq=bodor_et_al2008["weights"])
                        }[name]

    if target is None:
        target = { "driver":("dist", "basal", 0.0, 75, "area"),
                   "modulator":("dist", "basal", 75, None, "area"),
                   "reticular":("diam", "basal", None, None, "area"),
                   "nigral":("diam", ["basal", "soma"], None, None, None)
                   }[name]

    self.syn2cell = link.Link(self.syn, self.cell, distribution=distribution, target=target)

    self.n = 1

    self.__linkattr__("n", "n_syn", submodel=self.syn)
    self.__linkattr__("n", "n_spktr", submodel=self.spktr)
    self.__linkattr__("erev", "erev", submodel=self.syn.syn)

    if not hasattr(self, "gsyn"):
        self.gsyn = 0.

    if hasattr(self.syn.syn, "gsyn_ampa") and hasattr(self.syn.syn, "gsyn_nmda"):
        self.ratio = self.syn.syn.ratio
        
        self.__linkattr__(("gsyn", "ratio"), "gsyn_ampa", submodel=self.syn.syn, function="gsyn_ampa=gsyn/(1+ratio)")
        self.__linkattr__(("gsyn", "ratio"), "gsyn_nmda", submodel=self.syn.syn, function="gsyn_nmda=gsyn*ratio/(1+ratio)")
        
    elif hasattr(self.syn.syn, "gsyn"):
        self.__linkattr__("gsyn", "gsyn", submodel=self.syn.syn)
    else:
        raise Warning("Unknown property name describing synaptic conductance")







class InputToThalamus(model.Model):
  def __init__(self, name, cell, driver, modulator, nigralSync, nigralASync, reticular, percentsync_nigral=1.0):
    model.Model.__init__(self, name, cell=cell, driver=driver, modulator=modulator, nigralSync=nigralSync, nigralASync=nigralASync, reticular=reticular, percentsync_nigral=percentsync_nigral)

    for inputname in ["driver", "modulator", "nigralSync", "nigralASync", "reticular"]:
      self.__linkattr__("n_" + inputname, "n", submodel=getattr(self, inputname))
      self.__linkattr__("gsyn_" + inputname, "gsyn", submodel=getattr(self, inputname))
      self.__linkattr__("erev_" + inputname, "erev", submodel=getattr(self, inputname))

    self.n_total = 0
    
    self.__linkattr__("n_nigral", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")
    self.__linkattr__("n_driver", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")
    self.__linkattr__("n_modulator", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")
    self.__linkattr__("n_reticular", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")

    for inputname in ["nigralSync", "nigralASync"]:
      self.__linkattr__("erev_nigral", "erev", submodel=getattr(self, inputname))
      self.__linkattr__("gsyn_nigral", "gsyn", submodel=getattr(self, inputname))
      if inputname == 'nigralSync':
        self.__linkattr__("n_nigral", "n", function="n=int(round(n_nigral * percentsync_nigral))", submodel=getattr(self, inputname))
        self.__linkattr__("percentsync_nigral", "n", function="n=int(round(n_nigral * percentsync_nigral))", submodel=getattr(self, inputname))
      elif inputname == 'nigralASync':
        self.__linkattr__("n_nigral", "n", function="n=int(round(n_nigral * (1-percentsync_nigral)))", submodel=getattr(self, inputname))
        self.__linkattr__("percentsync_nigral", "n", function="n=int(round(n_nigral * (1-percentsync_nigral)))", submodel=getattr(self, inputname))      

  
def mk_vm_microcircuit(cellid,
                       lesioned_flag,
                       bg_param ={"Regularity":5.0, "MeanRate":50.0, "n":20,  "g":gsyn['SNRx1'], 'burst':None, 'modulation':None, 'template':None },
                       rtn_param={"Regularity":5.0, "MeanRate":10.0, "n":5,   "g":gsyn['rtn'], 'burst':None, 'modulation':None, 'template':None  },
                       drv_param={"Regularity":5.0, "MeanRate":30.0, "n":60,  "g":gsyn['CN_VM'], 'modulation':None, 'NmdaAmpaRatio':0.6, 'template':None },
                       mod_param={"Regularity":5.0, "MeanRate":15.0, "n":585, "g":gsyn['CX'], 'modulation':None, 'NmdaAmpaRatio':1.91, 'template':None },
                       tstop=5000.0):



  def mk_abbasi_spike_train(param):    
    if param['template'] is not None:
      # read and attach firing rate template, if any
      template = np.load(param['template'], allow_pickle=True).tolist()
      
      # return the spike train
      return stn.SpikeTrain("abbasi", regularity=param['Regularity'], mean_rate=param["MeanRate"], time=template['time'], rate=template['rate'], tstop=tstop, refractory_period=3.0, time_unit="ms")

    return stn.SpikeTrain("abbasi", regularity=param['Regularity'], mean_rate=param["MeanRate"], tstop=tstop, refractory_period=3.0, time_unit="ms")

    

  cell =  nrn.Cell("TC", cellid=cellid, lesioned_flag=lesioned_flag)

  InhSyn = nrn.Synapse("GABAA", erev=-76.4, tau=14.0)
  bgSyn = InhSyn()
  rtnSyn = InhSyn()
  drvSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=drv_param['NmdaAmpaRatio'])
  modSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=mod_param['NmdaAmpaRatio'])


  bgST_sync = mk_abbasi_spike_train(bg_param) 
  bgST_async = mk_abbasi_spike_train(bg_param) 

  if bg_param['burst']:
    bg_burst_sync = stn.SpikeTrain('burst', Tpeak=bg_param['burst']['Tpeak'], Tdur=bg_param['burst']['Tdur'],
                       max_rate=bg_param['burst']['MaxRate'],
                       fast_rise=False,
                       fast_decay=True,
                       refractory_period=1.5,
                       time_unit = 'ms',
                       intra_burst_k=3, intra_burst_theta = 0.1,
                       min_rate=bg_param['burst']['MinRate'],
                       regularity=bg_param['burst']['RegularitySync'],
                       tstop=bg_param['burst']['tstop'],
                       burst_mean_rate=bg_param['burst']['BurstMeanRate'],
                       min_inter_period=bg_param['burst']['MinInterPeriod'],
                       tinit=bg_param['burst']['tinit'])
    
    bg_burst_async = stn.SpikeTrain('burst', Tpeak=bg_param['burst']['Tpeak'], Tdur=bg_param['burst']['Tdur'],
                       max_rate=bg_param['burst']['MaxRate'],
                       fast_rise=False,
                       fast_decay=True,
                       refractory_period=1.5,
                       time_unit = 'ms',
                       intra_burst_k=3, intra_burst_theta = 0.1,
                       min_rate=bg_param['burst']['MinRate'],
                       regularity=bg_param['burst']['RegularityAsync'],
                       tstop=bg_param['burst']['tstop'],
                       burst_mean_rate=bg_param['burst']['BurstMeanRate'],
                       min_inter_period=bg_param['burst']['MinInterPeriod'],
                       tinit=bg_param['burst']['tinit'])
    
    bgST_sync.burst_model = bg_burst_sync # add burst
    bgST_async.burst_model = bg_burst_async # add burst


  rtnST = mk_abbasi_spike_train(rtn_param) 
  drvST = mk_abbasi_spike_train(drv_param) 
  modST = mk_abbasi_spike_train(mod_param) 

  #print(drv_param, mod_param)
  for pars, st in [ (bg_param, bgST_sync), (bg_param, bgST_async), (drv_param, drvST), (mod_param, modST), (rtn_param, rtnST) ]:
    if 'modulation' in pars and pars['modulation']:
      st.modulation_model = stn.SpikeTrain('modulation',
                                           tinit=pars['modulation']['tinit'],
                                           tstop=pars['modulation']['tstop'],
                                           regularity=pars['modulation']['regularity'],
                                           rate=pars['modulation']['rate'],
                                           amplitude=pars['modulation']['amplitude'],
                                           phase=pars['modulation']['phase'],
                                           time_unit='ms')


  si_drv = SynapticInputs("driver", drvSyn, drvST, cell)
  si_mod = SynapticInputs("modulator", modSyn, modST, cell)
  si_bg_sync = SynapticInputs("nigral", bgSyn, bgST_sync, cell)
  si_bg_async = SynapticInputs("nigral", bgSyn, bgST_async, cell)
  si_rtn = SynapticInputs("reticular", rtnSyn, rtnST, cell)

  i2t = InputToThalamus("InputToVMThalamus", cell, si_drv, si_mod, si_bg_sync, si_bg_async, si_rtn, percentsync_nigral=(1 if bg_param['burst'] is None else bg_param['burst']['PercentSync']))

  i2t.n_nigral    =  bg_param['n'] # 6
  i2t.n_reticular = rtn_param['n'] # 2
  i2t.n_modulator = mod_param['n'] # 137
  i2t.n_driver    = drv_param['n'] # 10%

  i2t.gsyn_nigral    = bg_param['g']
  i2t.gsyn_reticular = rtn_param['g']
  i2t.gsyn_modulator = mod_param['g']
  i2t.gsyn_driver    = drv_param['g']

  
  vmcircuit = mc.MicroCircuit("VMThalamus")
  vmcircuit.add(i2t)

  return vmcircuit, i2t








def run(vmcircuit, i2t, tstop, seed, key, v_init=-78.0, all_section_recording=False,
        all_synapse_recording=False, current_recording=[], rec_invl=50.0, varname=["_ref_v", "_ref_i_membrane_"], dt=0.1, t_checkpoint=500.0):

  import copy
  from neuron import h
  import time

  # run the NEURON simulation
  h.load_file("stdgui.hoc")

  # experimental conditions from Inagaki et al
  base.set(celsius=32, ena=76.4, ek=-104.9)

  h.cvode.use_fast_imem(1)
  h.cvode.cache_efficient(1)
  h.cvode_active(0)

  # precompile & compile the network representation
  retsim = precompiler.precompile(vmcircuit, seed)
  compiler.compile(retsim, base)

  if '--save-spike-train' in sys.argv:
    with open(sys.argv[sys.argv.index('--save-spike-train') + 1], 'w') as fo:
      for input_name, spike_tr in [ ('modulator', i2t.modulator.spktr), ('driver', i2t.driver.spktr), ('reticular', i2t.reticular.spktr), ('nigral', i2t.nigralSync.spktr), ('nigral', i2t.nigralASync.spktr) ]:
        for itr, p in  enumerate(retsim["models"][spike_tr]["real_simobj"].product):
          for tspk in p.product:
            fo.write('%s %d %g\n' % (input_name, itr, tspk))
            
  if '--save-syn-distribution' in sys.argv:
    with open(sys.argv[sys.argv.index('--save-syn-distribution') + 1], 'w') as fo:
      for input_name, syn2cell in [ ('modulator', i2t.modulator.syn2cell), ('driver', i2t.driver.syn2cell), ('reticular', i2t.reticular.syn2cell), ('nigral', i2t.nigralSync.syn2cell), ('nigral', i2t.nigralASync.syn2cell) ]:
        for isyn, p in  enumerate(retsim["links"][syn2cell]["real_simobj"].product):
          p = p.product['Segment']
          fo.write('%s %s %d %g %s %g\n' % (input_name, h.secname(sec=p['Section']), h.distance(p['Arc'], sec=p['Section']), p['Section'](p['Arc']).diam, p['Section'](p['Arc']), p['Section'](p['Arc']).area()))



  # instantiate the recorders
  recordings = {}

  # instantiate recorders for sections
  if all_section_recording:
    section = retsim["models"][i2t.cell]["real_simobj"].section
  else:
    section = {"somatic":retsim["models"][i2t.cell]["real_simobj"].section["somatic"]}

  # nwb key id format
  fmt = key + '.%s.%d(%f).%s'

  for sectype in section:
    for i in section[sectype]:
      s = section[sectype][i]

      # segments
      if s.L < rec_invl or sectype == "somatic":
        arcs = np.array([0.5])
      else:
        arcs = np.arange(rec_invl, s.L, rec_invl) / s.L

      # create recorders
      for x in arcs:
        # voltage membrane, currents
        for _varname in ( varname + current_recording ):
          print(_varname)
          recordings[fmt % (sectype, i, x, _varname)] = recorder.Recorder(getattr(s(x), _varname), seg=s(x), dt=dt)




  # instantiate recorders for synapse
  if all_synapse_recording:
    fmt = key + '.syn.%s[%d].%s'

    for syngroup in [i2t.driver, i2t.modulator, i2t.reticular, i2t.nigral]:
      for isyn, syn2cell in enumerate(retsim['models'][syngroup]['submodels']['syn2cell']['real_simobj'].product):

        syn2cell_product = copy.copy(syn2cell.product)

        s, x = syn2cell_product['Segment']['Section'], syn2cell_product['Segment']['Arc']

        del syn2cell_product['Segment']

        syn = syn2cell_product[list(syn2cell_product.keys())[0]]

        for _varname in ['_ref_i']: #, '_ref_g']:
          recordings[fmt % (retsim['models'][syngroup]['object'].name, isyn, _varname)] = recorder.Recorder(getattr(syn, _varname), seg=s(x), dt=dt)

  # print recording list
  for k in recordings:
    print ("\t", k)
  print(len(recordings), "recorders")

  # run the NEURON simulation
#  h.load_file("stdgui.hoc")

  # experimental conditions from Inagaki et al
#  base.set(celsius=32, ena=76.4, ek=-104.9)

  # check point

##  #try:
##  for msh in sys.argv:
##    if msh.startswith('--rtgshift'):
##      msh = float(msh.split('=')[-1])
##      break
##
##  #except:
##  #    msh = 0.0
##
##  # retigabine effets
##  h('forall if(ismembrane("iM")) m_steadyState_midpoint_iM = (-36.7 - %f)' % msh)

#  h.cvode.use_fast_imem(1)
#  h.cvode.cache_efficient(1)

  if '--no-run' not in sys.argv:
    h.cvode_active(0)

    #pc = h.ParallelContext(1)

    from neuron import coreneuron
    coreneuron.enable = True
    coreneuron.verbose = 0
    #coreneuron.gpu = True
    pc = h.ParallelContext(1)

    h.finitialize(v_init)
    h.stdinit()
    h.t = 0.

    

    first_run = True
    t_total = 0.
    
    t = 0.
    while t < tstop:
      if t_checkpoint and (t + t_checkpoint) < tstop:
        tnext = t + t_checkpoint
      else:
        tnext = tstop

      


      t0 = time.time()
      if first_run:
        #h.tstop = tnext # update
        pc.psolve(tnext)
      else:
        pc.psolve(tnext)
      tsolve = time.time() - t0
      
      # verbose
      #print ('checkpoint', h.t, tnext)
      t0 = time.time()
      # flush recordings
      for rec in recordings.values():
        rec._flush()
      tflush = time.time() - t0

      t_total += tsolve + tflush
      first_run = False

      t = tnext
      print ('\t', tnext, first_run, h.t, t, tstop, h.tstop, tsolve, tflush, tsolve + tflush)
    print (t_total, '\n')
    # clear all the objects
    compiler.clear(retsim)

    pc.done()

    pc = None

    # return
    return { k:rec.get(dt=dt) for k, rec in recordings.items() }
  return {}


def run_simulation(cellid, lesioned_flag, tstop, seed, key, all_section_recording=False, all_synapse_recording=False, current_recording=[], rec_invl=50.0, varname=["_ref_v", "_ref_i_membrane_"], dt=0.1, **kwargs):

  params = {
          'bg':{"Regularity":5.0, "MeanRate":50.0, "n":20,   "g":gsyn['SNRx1'], 'burst':None, 'modulation':None, 'template':None },
          'rtn':{"Regularity":5.0, "MeanRate":10.0, "n":5,   "g":gsyn['rtn'], 'burst':None, 'modulation':None, 'template':None},
          'drv':{"Regularity":5.0, "MeanRate":30.0, "n":60,  "g":gsyn['CN_VM'], 'modulation':None, 'NmdaAmpaRatio':0.6, 'template':None },
          'mod':{"Regularity":5.0, "MeanRate":15.0, "n":585, "g":gsyn['CX'], 'modulation':None, 'NmdaAmpaRatio':1.91, 'template':None}
          }

  

  for k, v in kwargs.items():
    params_tokens = k.split('_')
    if len(params_tokens) == 2:
      _param_name, _param_key = params_tokens
      #print (len(params_tokens), _param_name, _param_key, v, params_tokens)
      if _param_key in params and _param_name in params[_param_key]:
        params[_param_key][_param_name] = v

    elif len(params_tokens) == 3:
      _sub_param_name, _param_name, _param_key = params_tokens
      #print (len(params_tokens), _sub_param_name, _param_name, _param_key, v, params_tokens)

      if _param_key in params and _sub_param_name in params[_param_key]:
        if params[_param_key][_sub_param_name] is None:
          params[_param_key][_sub_param_name] = {}
        params[_param_key][_sub_param_name][_param_name] = v
  #print (params)
  for k1 in params:
    for k2 in params[k1]:
      print(k1, k2, params[k1][k2])

  vmcircuit, i2t = mk_vm_microcircuit(cellid, lesioned_flag, tstop=tstop, bg_param=params['bg'], rtn_param=params['rtn'], drv_param=params['drv'], mod_param=params['mod'])

  return run(vmcircuit, i2t, tstop, (seed, 0), key,
             all_section_recording=all_section_recording, all_synapse_recording=all_synapse_recording, current_recording=current_recording,
             rec_invl=rec_invl, varname=varname, dt=dt), params


def save_results(cc, params, fw=None, numpy_flag=False, verbose=False):
    import numpy as np
    for key_res, data_res in cc.items():
        if verbose:
            print (key_res, 'done')
        if not numpy_flag:
            fw.add(key_res, data_res[:, 0], data_res[:, 1])
        else:
            np.save(fw + '.' + key_res, data_res, allow_pickle=True)


def run_simulation_output(cellid, lesioned_flag, tstop, seed, key, all_section_recording=False, all_synapse_recording=False, current_recording=[], rec_invl=50.0, varname=["_ref_v"], dt=0.2, **kwargs):
    import sys
    output, params = run_simulation(cellid, lesioned_flag, tstop, seed, key,
                            all_section_recording=all_section_recording, all_synapse_recording=all_synapse_recording,
                            current_recording=current_recording, rec_invl=rec_invl, varname=varname, dt=dt, **kwargs)

    fw = nwbio.FileWriter(key + ".nwb", "thalamic_data", "thalamic_data_id", max_size=None)
    save_results(output, str(params), fw=fw)
    fw.close()


if __name__ == '__main__':
  import warnings
  warnings.simplefilter("ignore")

  import numpy as np

  if '--dt' in sys.argv:
      dt = float(sys.argv[sys.argv.index('--dt')+1])
  else:
      dt = 0.1

  if '--config_file' in sys.argv:
    filenamein = sys.argv[sys.argv.index('--config_file')+1]



    try:
        index = int(sys.argv[sys.argv.index('--index')+1])
    except:
        index = 0

    cfg = dict(np.load(filenamein, allow_pickle=True).tolist()[index])
    params = dict(cfg.copy())
    del params['cellid'], params['lesioned_flag'], params['tstop'], params['seed'], params['key']
    cellid, lesioned_flag, tstop, seed, key = cfg['cellid'], cfg['lesioned_flag'], cfg['tstop'], cfg['seed'], cfg['key']

  else:
    cellid = int(sys.argv[sys.argv.index('--cellid')+1])
    key = sys.argv[sys.argv.index('--key')+1]
    tstop = float(sys.argv[sys.argv.index('--tstop')+1])
    seed = int(sys.argv[sys.argv.index('--seed')+1])
    lesioned_flag = '--6ohda' in sys.argv

    params = dict()
    for i, k in enumerate(sys.argv):
        if '=' in k:
          try:
            tokens = k[2:].split('=')
            params[tokens[0]] = (int if tokens[0].startswith('n') else float)(tokens[1])
          except:
            pass

  # recording ion channel states
  if '--all_current_recording' in sys.argv:
    current_recording = []
    for suffix in ["BK", "iM", "TC_iT_Des98", "TC_iL", "TC_ih_Bud97", "TC_iD", "TC_iA", "SK_E2", "nat_TC_HH", "nap_TC_HH", "k_TC_HH" ]:
      for prefix in ["_ref_i_output"]:
        current_recording.append(prefix + "_" + suffix)
    print (current_recording)
  else:
    current_recording = []


  print (f"cellid={cellid}\nseed={seed}\n6ohda={'on' if lesioned_flag else 'off'}\ntstop={tstop}\nkey={key}\nother params{params}")
  run_simulation_output(cellid,
                        lesioned_flag,
                        tstop,
                        seed,
                        key,
                        all_section_recording=('--all_section_recording' in sys.argv),
                        all_synapse_recording=('--all_synapse_recording' in sys.argv),
                        current_recording=current_recording,
                        **params)
  sys.exit(0)
