import sim.memo.model as model
import sim.memo.link as link
import sim.memo.neuron as nrn
import sim.memo.spiketrain as stn
import sim.memo.distribution as distr

import sim.compiler.precompiler as precompiler
import sim.compiler as compiler
import sim.compiler.neuron as base
import sim.compiler.neuron.util.recorder as rec

import sim.memo.microcircuit as mc

import sim.memo.neuron as nrn

import sim.nwbio as nwbio

from sim.compiler.neuron.modules import neuron_modules

from neuron import h

import pandas as pd

import numpy as np


import matplotlib.pyplot as plt

import sys

lesioned_flag = '--6ohda' in sys.argv
try:
  cellid = int(sys.argv[sys.argv.index('--cellid')+1])
except:
  cellid = 0

bodor_et_al2008 = {
    "xlabels":[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 'somatic'],
    "weights":np.array([5.33673534681342, 10.590606603532123, 24.91409649347326, 8.85334015868954, 16.012285641156904, 5.302981827489134, 5.387125671871004, 3.6572178141796883, 8.91140900947019, 1.739665984131058, 1.733267212695175, 6.980899667263891])
    }
bodor_et_al2008["weights"] /= np.sum(bodor_et_al2008["weights"])


class Cell:
    
  def __del__(self):
      del self.bpo_cell
      del self.cell
      del self.section
      del self.product 
      
      self.bpo_cell = self.cell = self.section = self.product = None
      
    
  __control__ = not lesioned_flag
  def load_params(self, filename):
    import numpy as np
    return sorted(np.load(filename, allow_pickle=True).tolist().items())


  def mk_cell_model(self, cellid, control=False):
    import mkcell
    import os
    
    filename = "test_model_" + ("control" if control else "lesioned") + "_edyta_test_good.npy"
    param = self.load_params(os.path.join(os.path.dirname(__file__), 'mkcell', filename))[cellid][1][0]
    etype=("control" if control else "lesioned") + "_BK_short_AP"

    return mkcell.mk_cell_model(param, etype=etype)

  def __init__(self, name, cellid=cellid):
      self.name = name
      self.cellid = cellid
      self.product = None
      

  def make(self):
    import numpy as np
    import pandas as pd

    if self.product is None:
      self.bpo_cell = self.mk_cell_model(self.cellid, control=Cell.__control__)
      self.cell = self.bpo_cell.icell
      self.morph_table, self.section = Cell.bpo2memo_cell(self.bpo_cell)
      self.product = { "Cell":self.section, "MorphologyTable":self.morph_table }
                
    return self.product
      

  def branch_order(sec, soma_sec):
    from neuron import h
    order = 0
    sref = h.SectionRef(sec=sec)
    while sref.sec != soma_sec:
      sref = h.SectionRef(sec=sref.parent)
      order += 1
    return order

  def bpo2memo_cell(bpo_cell):
    from neuron import h
    import pandas as pd
    
    section_collection = {}
    h.distance(sec=bpo_cell.icell.soma[0])
    tab = pd.DataFrame(columns=["type", "segment", "name", "number", "diam", "len", "dist"])
    for section_type in bpo_cell.seclist_names:
      section_collection[section_type] = {}
      if section_type != "all":
        for section in getattr(bpo_cell.icell, section_type):
          section_number = int(h.secname(sec=section).split("[")[-1].replace("]", ""))
          section_collection[section_type][section_number] = section
          for segment in section.allseg():
            tab = tab.append({ "type":section_type,
                               "segment":segment.x,
                               "name":section,
                               "number":section_number,
                               "diam":segment.diam,
                               "len":section.L / section.nseg,
                               "dist":h.distance(segment.x, sec=section),
                               "order":Cell.branch_order(section, bpo_cell.icell.soma[0])},
                             ignore_index=True)
            
    tab["segment"] = tab["segment"].astype(float)
    tab["dist"] = tab["dist"].astype(float)
    tab["len"] = tab["len"].astype(float)
    tab["number"] = tab["number"].astype(int)
    tab["weights"] = tab["len"] / tab["len"].min()
    return tab, section_collection        
          

  def get(self, target_feature=None, min_value=None, max_value=None, section_type="basal", optional_X=None):
    import pandas as pd
    
    f = self.morph_table
    if section_type:
        if type(section_type) != list:
            section_type = [ section_type ]
        _f = pd.DataFrame()
        for _st in section_type:
            _f = _f.append(f[f["type"] == _st])
        f = _f
        del _f, _st 
    
    if target_feature:
      if min_value:
        f = f[f[target_feature] >= min_value]
       
      if max_value:
        f = f[f[target_feature] < max_value]

    f = f[[ 'type', 'number', 'segment', 'weights' ]]
    
    if f.shape[0] == 0:
        return None
    
    if optional_X:
        f['weights_cdf'] = (f['weights'] / f['weights'].sum()).cumsum()
        f = f.loc[ f[f['weights_cdf'] >= optional_X].index[:1], ['type', 'number', 'segment']]
    return [self.section[x["type"]][x["number"]](x["segment"]) for k, x in f.iterrows()]


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
        target = { "driver":("order", "basal", None, 2), 
                        "modulator":("order", "basal", 2, None),
                        "reticular":("diam", "basal", None, None),
                        "nigral":("diam", ["basal", "soma"], None, None)
                        }[name]        
        
    self.syn2cell = link.Link(self.syn, self.cell, distribution=distribution, target=target)
    
    self.n = 1
    
    self.__linkattr__("n", "n_syn", submodel=self.syn)
    self.__linkattr__("n", "n_spktr", submodel=self.spktr)
    self.__linkattr__("erev", "erev", submodel=self.syn.syn)
    
    if not hasattr(self, "gsyn"):
        self.gsyn = 0.
        
    if hasattr(self.syn.syn, "gsyn_ampa") and hasattr(self.syn.syn, "gsyn_nmda"):        
        if not hasattr(self, "ratio"):
            self.ratio = 1.
        
        self.__linkattr__(("gsyn", "ratio"), "gsyn_ampa", submodel=self.syn.syn, function="gsyn_ampa=gsyn/(1+ratio)")
        self.__linkattr__(("gsyn", "ratio"), "gsyn_nmda", submodel=self.syn.syn, function="gsyn_nmda=gsyn*ratio/(1+ratio)")

    elif hasattr(self.syn.syn, "gsyn"):
        self.__linkattr__("gsyn", "gsyn", submodel=self.syn.syn)
    else:
        raise Warning("Unknown property name describing synaptic conductance")




        
    
        
class InputToThalamus(model.Model):
  def __init__(self, name, cell, driver, modulator, nigral, reticular):
    model.Model.__init__(self, name, cell=cell, driver=driver, modulator=modulator, nigral=nigral, reticular=reticular)    
    
    for inputname in ["driver", "modulator", "nigral", "reticular"]:
      self.__linkattr__("n_" + inputname, "n", submodel=getattr(self, inputname))
      
      if hasattr(getattr(self, inputname), "gsyn"):
        self.gsyn = 0.
        self.__linkattr__("gsyn_" + inputname, "gsyn", submodel=inputname)
        
      self.__linkattr__("erev_" + inputname, "erev", submodel=getattr(self, inputname))
    
    self.__linkattr__("n_driver", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")
    self.__linkattr__("n_modulator", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")
    self.__linkattr__("n_nigral", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")
    self.__linkattr__("n_reticular", "n_total", function="n_total=n_driver+n_modulator+n_nigral+n_reticular")



def mk_vm_microcircuit(cellid,
                       bg_param ={"Regularity":1.0, "MeanRate":60.0, "n":17,  "g":0.00082},
                       rtn_param={"Regularity":1.0, "MeanRate":20.0, "n":7,   "g":0.00096},
                       drv_param={"Regularity":1.0, "MeanRate":30.0, "n":41,  "g":0.00223, 'AmpaNmdaRatio':0.6 },
                       mod_param={"Regularity":1.0, "MeanRate":15.0, "n":346, "g":0.00182, 'AmpaNmdaRatio':1.91},
                       tstop=5000.0):

  
  cell =  nrn.Cell("TC", cellid=cellid)    

  InhSyn = nrn.Synapse("GABAA", erev=-75.0, tau=14.0)
  bgSyn = InhSyn()
  rtnSyn = InhSyn()
  drvSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=drv_param['AmpaNmdaRatio'])
  modSyn = nrn.Synapse("AmpaNmda", erev=0.0, ratio=mod_param['AmpaNmdaRatio'])


  bgST = stn.SpikeTrain("abbasi", regularity=bg_param['Regularity'], mean_rate=bg_param["MeanRate"], tstop=tstop, refractory_period=3.0, time_unit="ms")
  rtnST = stn.SpikeTrain("abbasi", regularity=rtn_param['Regularity'], mean_rate=rtn_param["MeanRate"], tstop=tstop, refractory_period=3.0, time_unit="ms")
  drvST = stn.SpikeTrain("abbasi", regularity=drv_param['Regularity'], mean_rate=drv_param["MeanRate"], tstop=tstop, refractory_period=3.0, time_unit="ms")
  modST = stn.SpikeTrain("abbasi", regularity=mod_param['Regularity'], mean_rate=mod_param["MeanRate"], tstop=tstop, refractory_period=3.0, time_unit="ms")


  si_drv = SynapticInputs("driver", drvSyn, drvST, cell)
  si_mod = SynapticInputs("modulator", modSyn, modST, cell)
  si_bg = SynapticInputs("nigral", bgSyn, bgST, cell)
  si_rtn = SynapticInputs("reticular", rtnSyn, rtnST, cell)

  i2t = InputToThalamus("InputToVMThalamus", cell, si_drv, si_mod, si_bg, si_rtn)

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




def mk_vm_microcircuit_test(cellid, 
                       tstop=5000.0):

  
  cell =  nrn.Cell("TC", cellid=cellid)    

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
  si_bg = SynapticInputs("nigral", bgSyn, bgST, cell)
  si_rtn = SynapticInputs("reticular", rtnSyn, rtnST, cell)

  i2t = InputToThalamus("InputToVMThalamus", cell, si_drv, si_mod, si_bg, si_rtn)

  vmcircuit = mc.MicroCircuit("VMThalamus")
  vmcircuit.add(i2t)
  
  return vmcircuit, i2t


# 200 ms increase/decrease
# F-I curve for variations and background
#@neuron_modules
def run(vmcircuit, i2t, filename, tstop, seed, v_init=-78.):
  
  
  
  r = precompiler.precompile(vmcircuit, seed)
  compiler.compile(r, base)
  
  soma = r["models"][i2t.cell]["real_simobj"].section["somatic"][0]
  
  rr = rec.Recorder(soma(0.5)._ref_v, seg=soma(0.5))
  
  h.load_file("stdgui.hoc")
  h.tstop = tstop
  h.finitialize(v_init)
  h.run(tstop)
  
  data = rr.get()
  
  #fw = nwbio.FileWriter(filename, "thalamic_test", "thalamic_test_id")
  #cw = fw.get_cell_writer("test_cell")
  #cw.add(data[:, 0], data[:, 1])
  #fw.close()

  np.save(filename, data, allow_pickle=True)
  



if __name__ == '__main__':
  cellid = int(sys.argv[sys.argv.index('--cellid')+1])
  filename = sys.argv[sys.argv.index('--filename')+1]
  tstop = float(sys.argv[sys.argv.index('--tstop')+1])
  seed = int(sys.argv[sys.argv.index('--seed')+1])
  
  params = {
          'bg':{"Regularity":1.0, "MeanRate":60.0, "n":17,  "g":0.0015},
          'rtn':{"Regularity":1.0, "MeanRate":20.0, "n":7,   "g":0.0008},
          'drv':{"Regularity":1.0, "MeanRate":30.0, "n":41,  "g":0.0033, 'AmpaNmdaRatio':0.6 },
          'mod':{"Regularity":1.0, "MeanRate":15.0, "n":346, "g":0.0018, 'AmpaNmdaRatio':1.91}
          }


  for i, k in enumerate(sys.argv):
          tokens = k[2:].split('=')
          if len(tokens) == 2:
            params_tokens = tokens[0].split('_')
            if len(params_tokens) == 2:
              _param_key, _param_name = params_tokens
              if _param_key in params and _param_name in params[_param_key]:
                value =  (int if _param_name == 'n' else float)(tokens[1])
                params[_param_key][_param_name] = value
              else:
                print ('Warning {_param_key}{_param_name}{tokens[1]} not found')

  print (params)

  vmcircuit, i2t = mk_vm_microcircuit(cellid, tstop=tstop, bg_param=params['bg'], rtn_param=params['rtn'], drv_param=params['drv'], mod_param=params['mod'])
  run(vmcircuit, i2t, filename, tstop, (seed, seed))

