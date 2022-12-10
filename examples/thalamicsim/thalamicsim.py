import warnings
warnings.filterwarnings("ignore")

import gc
gc.collect(2)

import sys
import os

import numpy as np
from neuron import h, coreneuron
    
import MeMo.compiler as compiler
import MeMo.compiler.precompiler as precompiler
import MeMo.compiler.neuron as base
import MeMo.compiler.neuron.util.recorder as recorder
import MeMo.memo.microcircuit as mc
import MeMo.nwbio as nwbio
import vmcell

# register cell model
compiler.register_object(base, vmcell.Cell)

# models of thalamic connections
from connectivity import SynapticInputs, InputToThalamus

# read default values of synaptic conductance and their numbers
try:
  gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
except:
  gsyn = { 'SNRx1':0., 'RTN':0., 'CX':0., 'SNR':0., 'CN_VL':0. }
  print('Warning: default synaptic conductances not found')

nsyn = { 'SNR':20, 'RTN':5, 'MOD':300, 'DRV':30 }


# register modules
from MeMo.compiler.neuron import modules as neuron_modules
neuron_modules.register_modules(os.path.join(os.path.dirname(__file__), 'synapses'))
neuron_modules.compile()

 
def mk_default_inputs(tstop, bg_param, rtn_param, drv_param, mod_param):
  
  def mk_abbasi_spike_train(param):    
    if param['template'] is not None:
      # read and attach firing rate template, if any
      template = np.load(param['template'], allow_pickle=True).tolist()
      
      # return the spike train
      return stn.SpikeTrain("abbasi", regularity=param['Regularity'], mean_rate=param["MeanRate"], time=template['time'], rate=template['rate'], tstop=tstop, refractory_period=3.0, time_unit="ms")

    return stn.SpikeTrain("abbasi", regularity=param['Regularity'], mean_rate=param["MeanRate"], tstop=tstop, refractory_period=3.0, time_unit="ms")


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


  rtnST = mk_abbasi_spike_train(RTN_param) 
  drvST = mk_abbasi_spike_train(drv_param) 
  modST = mk_abbasi_spike_train(mod_param) 

  #print(drv_param, mod_param)
  for pars, st in [ (bg_param, bgST_sync), (bg_param, bgST_async), (drv_param, drvST), (mod_param, modST), (RTN_param, RTNST) ]:
    if 'modulation' in pars and pars['modulation']:
      st.modulation_model = stn.SpikeTrain('modulation',
                                           tinit=pars['modulation']['tinit'],
                                           tstop=pars['modulation']['tstop'],
                                           regularity=pars['modulation']['regularity'],
                                           rate=pars['modulation']['rate'],
                                           amplitude=pars['modulation']['amplitude'],
                                           phase=pars['modulation']['phase'],
                                           time_unit='ms')
      
  return bgST_sync, bgST_async, rtnST, drvST, modST


def mk_vm_microcircuit(cellid, lesioned_flag, bgST_sync, bgST_async, rtnST, drvST, modST, 
                       bg_param ={"n":nsyn['SNR'], "g":gsyn['SNRx1']},
                       rtn_param={"n":nsyn['RTN'], "g":gsyn['RTN']},
                       drv_param={"n":nsyn['DRV'], "g":gsyn['CN_VL'], 'NmdaAmpaRatio':0.6},
                       mod_param={"n":nsyn['MOD'], "g":gsyn['CX'], 'NmdaAmpaRatio':1.91}):
  # instantiate cell
  cell =  nrn.Cell("TC", cellid=cellid, lesioned_flag=lesioned_flag)

  # model of synapses
  bgSyn = nrn.Synapse("GABAA", erev=-76.4, tau=14.0)
  rtnSyn = nrn.Synapse("GABAA", erev=-76.4, tau=14.0)
  drvSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=drv_param['NmdaAmpaRatio'])
  modSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=mod_param['NmdaAmpaRatio'])
  
  # instantiate synaptic inputs
  si_drv = SynapticInputs("driver", drvSyn, drvST, cell)
  si_mod = SynapticInputs("modulator", modSyn, modST, cell)
  si_bg_sync = SynapticInputs("nigral", bgSyn, bgST_sync, cell)
  si_bg_async = SynapticInputs("nigral", bgSyn, bgST_async, cell)
  si_rtn = SynapticInputs("reticular", rtnSyn, rtnST, cell)

  i2t = InputToThalamus("InputToVMThalamus", cell, si_drv, si_mod, si_bg_sync, si_bg_async, si_rtn, percentsync_nigral=(1 if bg_param['burst'] is None else bg_param['burst']['PercentSync']))

  # set numbers and conductance of the synapses
  i2t.n_nigral    =  bg_param['n']
  i2t.n_reticular = rtn_param['n']
  i2t.n_modulator = mod_param['n']
  i2t.n_driver    = drv_param['n']

  i2t.gsyn_nigral    = bg_param['g']
  i2t.gsyn_reticular = rtn_param['g']
  i2t.gsyn_modulator = mod_param['g']
  i2t.gsyn_driver    = drv_param['g']

  # microcircuit
  vmcircuit = mc.MicroCircuit("VMThalamus")
  vmcircuit.add(i2t)

  return vmcircuit, i2t


def nrn_run(vmcircuit, i2t, tstop, seed, all_section_recording=False, all_synapse_recording=False, current_recording=[], dt=1, v_init=-78.0, save_spike_train=None, save_syn_distribution=None):
  import copy
  import time

  # run the NEURON simulation
  h.load_file("stdgui.hoc")

  # experimental conditions from Inagaki et al
  base.set(celsius=32, ena=76.4, ek=-104.9)

  # set for eventual recordings of total membrane current
  h.cvode.use_fast_imem(1)
  h.cvode.cache_efficient(1)
  h.cvode_active(0)

  # precompile & compile the network representation
  retsim = precompiler.precompile(vmcircuit, seed)
  compiler.compile(retsim, base)

  # save spike trains
  if save_spike_train:
    with open(save_spike_train, 'w') as fo:
      for input_name, spike_tr in [ ('modulator', i2t.modulator.spktr), ('driver', i2t.driver.spktr), ('reticular', i2t.reticular.spktr), ('nigral', i2t.nigralSync.spktr), ('nigral', i2t.nigralASync.spktr) ]:
        for itr, p in  enumerate(retsim["models"][spike_tr]["real_simobj"].product):
          for tspk in p.product:
            fo.write('%s %d %g\n' % (input_name, itr, tspk))

  # save synaptic distributions
  if save_syn_distribution:
    with open(save_syn_distribution, 'w') as fo:
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
  fmt = '%s[%d](%f).%s'

  for sectype in section:
    for i in section[sectype]:
      sec = section[sectype][i]

      # get all the segments
      for seg in sec:
        # create recording for each variable
        for varname in current_recording:
          # test whether it is a density variable
          recordings[fmt % (sectype, i, seg.x, varname)] = recorder.Recorder(getattr(seg, varname), seg=seg, dt=dt, density_variable=varname.startswith('_ref_i_output'))

  # instantiate recorders for synapse
  if all_synapse_recording:
    fmt = 'syn.%s[%d].%s'

    for syngroup in [i2t.driver, i2t.modulator, i2t.reticular, i2t.nigralSync, i2t.nigralASync ]:
      for isyn, syn2cell in enumerate(retsim['models'][syngroup]['submodels']['syn2cell']['real_simobj'].product):
        syn2cell_product = copy.copy(syn2cell.product)
        s, x = syn2cell_product['Segment']['Section'], syn2cell_product['Segment']['Arc']
        syn = syn2cell_product[list(syn2cell_product.keys())[0]]
        recordings[fmt % (retsim['models'][syngroup]['object'].name, isyn, _varname)] = recorder.Recorder(getattr(syn, '_ref_i'), seg=s(x), dt=dt)

  # initialize coreneuron
  h.cvode_active(0)
  coreneuron.enable = True
  coreneuron.verbose = 0
  
  pc = h.ParallelContext(1)
  h.finitialize(v_init)
  h.stdinit()
  h.t = 0.
  
  t = 0.
  while t < tstop:
    if t_checkpoint and (t + t_checkpoint) < tstop:
      tnext = t + t_checkpoint
    else:
      tnext = tstop      

    # solve and profile
    t0 = time.time()
    pc.psolve(tnext)
    tsolve = time.time() - t0

    # flush recordings
    t0 = time.time()
    for rec in recordings.values():
      rec._flush()
    tflush = time.time() - t0

    print ('\t', tnext, h.t, t, tstop, h.tstop, tsolve, tflush, tsolve + tflush)
    
    t_total += tsolve + tflush
    first_run = False

    t = tnext

    
  # clear all the objects
  compiler.clear(retsim)
  pc.done()
  pc = None

  return { k:rec.get() for k, rec in recordings.items() }



def run(cellid, seed, lesioned_flag, tstop, current_recording, all_section_recording=False, all_synapse_recording=False, **kwargs):
  param = {
          'bg':{"Regularity":5.0, "MeanRate":50.0, "n":nsyn['SNR'],  "g":gsyn['SNRx1'], 'burst':None, 'modulation':None, 'template':None },
          'rtn':{"Regularity":5.0, "MeanRate":10.0, "n":nsyn['RTN'], "g":gsyn['RTN'], 'burst':None, 'modulation':None, 'template':None},
          'drv':{"Regularity":5.0, "MeanRate":30.0, "n":nsyn['DRV'], "g":gsyn['CN_VL'], 'modulation':None, 'NmdaAmpaRatio':0.6, 'template':None },
          'mod':{"Regularity":5.0, "MeanRate":15.0, "n":nsyn['MOD'], "g":gsyn['CX'], 'modulation':None, 'NmdaAmpaRatio':1.91, 'template':None}
          }

  # create default synaptic inputs
  bgST_sync, bgST_async, rtnST, drvST, modST = mk_default_inputs(tstop, param['bg'], param['rtn'], param['drv'], param['mod'])

  # replace inputs if defined
  if 'bgST_sync' in kwargs:
    bgST_sync = kwargs['bgST_sync']
    
  if 'bgST_async' in kwargs:
    bgST_async = kwargs['bgST_async']
    
  if 'rtnST' in kwargs:
    rtnST = kwargs['rtnST']
    
  if 'drvST' in kwargs:
    drvST = kwargs['drvST']
    
  if 'modST' in kwargs:
    modST = kwargs['modST']
  
  # read optional parameters
  for k, v in kwargs.items():
    param_token = k.split('_')
    
    if len(param_tokens) == 2:
      param[param_token[0]][param_token[1]] = v

    elif len(param_tokens) == 3:
      if param[param_token[0]][param_token[1]] is None:
        param[param_token[0]][param_token[1]] = {}
      param[param_token[0]][param_token[1]][param_token[2]] = v
      

  # instantiate the simulation
  vmcircuit, i2t = mk_vm_microcircuit(cellid, lesioned_flag, tstop, bgST_sync, bgST_async, rtnST, drvST, modST, bg_param=param['bg'], rtn_param=param['rtn'], drv_param=param['drv'], mod_param=param['mod'])

  # run and return
  return nrn_run(vmcircuit, i2t, tstop, (seed, 0), all_section_recording=all_section_recording, all_synapse_recording=all_synapse_recording, current_recording=current_recording, **kwargs)


def run_and_save(key, cellid, seed, lesioned_flag, tstop, current_recording, all_section_recording=False, all_synapse_recording=False, **kwargs):
    # run optimizer
    output = run(cellid, lesioned_flag, tstop, seed, all_section_recording=all_section_recording, all_synapse_recording=all_synapse_recording, current_recording=current_recording, **kwargs)

    # store to nwb file
    fw = nwbio.FileWriter(key + ".nwb", "thalamic_data", "thalamic_data_id", max_size=None)
    for key_res, data_res in output.items():
      fw.add(key + '.' + key_res, data_res[:, 0], data_res[:, 1])
    fw.close()


if __name__ == '__main__':  

  # extract arguments
  def strvector(value):
    return [ x for x in values.split(',') ]
  

  # get all the params
  params = { }
  arg_type = {
    'dt':float,
    'index':int,
    'cellid':int,
    'tstop':float,
    'seed':int,
    'current_recording':strvector
  }
    

  for arg in sys.argv:
    if arg.startswith('--'):
      tokens = arg.split('=')
      if len(tokens) > 1:
        name, value = tokens[0], tokens[1]

        # check the type
        if arg_type[name]:
          value = arg_type[name](value)
          
      else:
        name, value = tokens[0], None

      param[name] = value

  if 'config_file' in param:
    param.update(dict(np.load(param['config_file'], allow_pickle=True).tolist()[param['index']]))

  # recording variables
  var_recording = [ "_ref_v" ]

  # total current
  if 'total_current_recording' in param:
    var_recording.append("_ref_i_membrane_")
  
  # ion channels
  if 'all_current_recording' in param:
    current_recording_suffix = ["BK", "iM", "TC_iT_Des98", "TC_iL", "TC_ih_Bud97", "TC_iD", "TC_iA", "SK_E2", "nat_TC_HH", "nap_TC_HH", "k_TC_HH"]
  elif 'current_recording' in param:
    current_recording_suffix = [param['current_recording']]
  else:
    current_recording_suffix = []

  for suffix in current_recording_suffix:
    var_recording.append("_ref_i_output" + suffix)
  
  
  

  print (f"cellid={cellid}\nseed={seed}\n6ohda={'on' if lesioned_flag else 'off'}\ntstop={tstop}\nkey={key}\nother params{params}")

  # remove other params
  for name in ['key', 'cellid', 'seed', 'lesioned', 'tstop', 'all_section_recording', 'all_synapse_recording' ]:
    if name in param:
      del param[name]

  # run and output
  run_and_save(param['key'], param['cellid'], param['seed'], 'lesioned' in param, param['tstop'], var_recording,
                        all_section_recording='all_section_recording' in param, all_synapse_recording='all_synapse_recording' in param, 
                        **params)
  sys.exit(0)
