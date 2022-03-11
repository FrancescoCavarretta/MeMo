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

import mkcell

import mkmodules

from neuron import h

import pandas as pd


import matplotlib.pyplot as plt

mkmodules.mk_mod_files()



    


class Cell:
  def __init__(self, name):
    self.name = name
    self.bpo_cell = mk_cell_model(0)
    self.cell = self.bpo_cell.icell
    self.morph_table, self.section = Cell.bpo2memo_cell(self.bpo_cell)
    self.product = { "Cell":self.section, "MorphologyTable":self.morph_table }


  def make(self):            
      return self.product
      

  def bpo2memo_cell(bpo_cell):
    from neuron import h
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
                               "dist":h.distance(segment.x, sec=section) },
                             ignore_index=True)
            
    tab["segment"] = tab["segment"].astype(float)
    tab["dist"] = tab["dist"].astype(float)
    tab["len"] = tab["len"].astype(float)
    tab["number"] = tab["number"].astype(int)
    return tab, section_collection


  def get(self, target_feature=None, min_value=None, max_value=None, section_type="basal"):
    f = self.morph_table
    if section_type:
      f = f[f["type"]==section_type]
    if target_feature:
      if min_value:
        f = f[f[target_feature] > min_value]
      if max_value:
        f = f[f[target_feature] < max_value]
    f = f[[ 'type', 'number', 'segment' ]]
    return [self.section[x["type"]][x["number"]](x["segment"]) for k, x in f.iterrows()]
      

def load_params(filename):
  import numpy as np
  return sorted(np.load(filename, allow_pickle=True).tolist().items())


def mk_cell_model(cellid, control=True):
  filename = "test_model_" + ("control" if control else "lesioned") + "_edyta_test.npy"
  param = load_params(filename)[cellid][1][0]
  etype=("control" if control else "lesioned") + "_BK_short_AP"
  return mkcell.mk_cell_model(param, etype=etype)


class SynapticInputs(nrn.Model):
  def __init__(self, name, syn, spktr):
    model.Model.__init__(self, name)
    self.syn = nrn.SynapseGroup("syn", syn=syn)
    self.spktr = stn.SpikeTrainPopulation("spktr", spktr=spktr)
    self.l = link.Link(self.spktr, self.syn)
    
    self.n = 1
    
    self.__linkattr__("n", "n_syn", submodel=self.syn)
    self.__linkattr__("n", "n_spktr", submodel=self.spktr)
    self.__linkattr__("erev", "erev", submodel=self.syn.syn)

    if hasattr(self.syn.syn, "gsyn"):
      self.gsyn = 0.
      self.__linkattr__("gsyn", "gsyn", submodel=self.syn.syn)
      
    if hasattr(self.syn.syn, "gsyn_ampa"):
      self.gsyn_ampa = 0.
      self.__linkattr__("gsyn_ampa", "gsyn_ampa", submodel=self.syn.syn)
      
    if hasattr(self.syn.syn, "gsyn_nmda"):
      self.gsyn_nmda = 0.
      self.__linkattr__("gsyn_nmda", "gsyn_nmda", submodel=self.syn.syn)   


class InputToThalamus(model.Model):
  def __init__(self, name, drivers, modulators, inhibitors):
    model.Model.__init__(self, name, drivers=drivers, modulators=modulators, inhibitors=inhibitors, n_total=3, p_drivers=0.5, p_modulators=0.5, p_inhibitors=1/3.0)
    
    for inputname in ["drivers", "modulators", "inhibitors"]:
      self.__linkattr__("n_" + inputname, "n", submodel=getattr(self, inputname))
      
      if hasattr(getattr(self, inputname), "gsyn"):
        self.gsyn = 0.
        self.__linkattr__("gsyn_" + inputname, "gsyn", submodel=inputname)
      
      if hasattr(getattr(self, inputname), "gsyn_ampa"):
        self.gsyn_ampa = 0.
        self.__linkattr__("gsyn_ampa_" + inputname, "gsyn_ampa", submodel=inputname)
        
      if hasattr(getattr(self, inputname), "gsyn_nmda"):
        self.gsyn_nmda = 0.
        self.__linkattr__("gsyn_nmda_" + inputname, "gsyn_nmda", submodel=inputname)
        

      self.__linkattr__("erev_" + inputname, "erev", submodel=getattr(self, inputname))
      
    self.__linkattr__("n_drivers", "n_total", function="n_total=n_drivers+n_modulators+n_inhibitors")
    self.__linkattr__("n_drivers", "p_drivers", function="p_drivers = n_drivers/(n_drivers+n_modulators)")
    
    self.__linkattr__("n_modulators", "n_total", function="n_total=n_drivers+n_modulators+n_inhibitors")
    self.__linkattr__("n_modulators", "p_modulators", function="n_modulators = n_modulators/(n_drivers+n_modulators)")
    
    self.__linkattr__("n_inhibitors", "n_total", function="n_total=n_drivers+n_modulators+n_inhibitors")
    self.__linkattr__("n_inhibitors", "p_inhibitors", function="p_inhibitors = n_inhibitors/n_total")

    self.__linkattr__("n_total", "n_drivers", function="n_drivers=int(round(p_drivers*(1-p_inhibitors)*n_total))")
    self.__linkattr__("n_total", "n_modulators", function="n_modulators=int(round(p_modulators*(1-p_inhibitors)*n_total))")
    self.__linkattr__("n_total", "n_inhibitors", function="n_inhibitors=int(round(p_inhibitors*n_total))")
    self.__linkattr__("n_total", "p_inhibitors", function="p_inhibitors = n_inhibitors/n_total")
    self.__linkattr__("n_total", "p_modulators", function="p_modulators = n_modulators/(n_drivers+n_modulators)")
    self.__linkattr__("n_total", "p_drivers", function="p_drivers = n_drivers/(n_drivers+n_modulators)")
    self.__linkattr__("n_total", "n_total", function="n_total=n_drivers+n_modulators+n_inhibitors")
    
    self.__linkattr__("p_drivers", "p_modulators", function="p_modulators = 1-p_drivers")
    self.__linkattr__("p_modulators", "p_drivers", function="p_drivers = 1-p_modulators")

    
    self.__linkattr__("p_drivers", "n_total", function="n_total=n_total")
    self.__linkattr__("p_modulators", "n_total", function="n_total=n_total")
    self.__linkattr__("p_inhibitors", "n_total", function="n_total=n_total")
    


bgSyn = nrn.Synapse("ExpSyn", erev=-75.0, tau=6.0)
drvSyn = nrn.Synapse("AmpaNmda", erev=0.0)
modSyn = nrn.Synapse("AmpaNmda", erev=0.0)

idrv = SynapticInputs("drivers", drvSyn, stn.SpikeTrain("poissonian", mean_rate=55.0, tstop=5000.0, refractory_period=5.0, time_unit="ms"))
imod = SynapticInputs("modulators", modSyn, stn.SpikeTrain("poissonian", mean_rate=55.0, tstop=5000.0, refractory_period=5.0, time_unit="ms"))
iinh = SynapticInputs("inhibitors", bgSyn, stn.SpikeTrain("poissonian", mean_rate=55.0, tstop=5000.0, refractory_period=5.0, time_unit="ms"))


i2t = InputToThalamus("test1", idrv, imod, iinh)


base.Cell = Cell


c = nrn.Cell("TC")


drv_ln = link.Link(i2t.drivers.syn, c,
                    distribution=distr.Distribution("uniform"),
                    target=("dist", "basal", 0, 150))

mod_ln = link.Link(i2t.modulators.syn, c,
                    distribution=distr.Distribution("uniform"),
                    target=("dist", "basal", 150, None))

bg_ln = link.Link(i2t.inhibitors.syn, c,
                    distribution=distr.Distribution("uniform"),
                    target=("dist", "basal", 50, 200))


mc1 = mc.MicroCircuit("Test")
mc1.add(i2t)
mc1.add(c)
mc1.add(bg_ln)
mc1.add(mod_ln)
mc1.add(drv_ln)

i2t.n_total=10
i2t.gsyn_ampa_drivers = 0.01
i2t.gsyn_ampa_modulators = 0.01
i2t.gsyn_inhibitors = 0.01


r = precompiler.precompile(mc1, (0, 5))
compiler.compile(r, base)

rr = rec.Recorder(r["models"][c]["real_simobj"].section["somatic"][0](0.5))

h.load_file("stdgui.hoc")
h.tstop = 5000.0
h.run(5000.0)
data = rr.get()
plt.plot(data[:,0], data[:,1])
plt.show()
