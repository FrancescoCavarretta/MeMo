import sim.memo.model as model
import sim.memo.link as link
import sim.memo.neuron as nrn
import sim.memo.spiketrain as stn

import sim.compiler.precompiler as precompiler
import sim.compiler as compiler
import sim.compiler.neuron as base

import sim.memo.microcircuit as mc

   
class SynapticInputs(nrn.Model):
  def __init__(self, name, syn, spktr):
    model.Model.__init__(self, name)
    self.syn = nrn.SynapseGroup("syn", syn=syn)
    self.spktr = stn.SpikeTrainPopulation("spktr", spktr=spktr)
    self.l = link.Link(spktr, syn)
    
    self.n = 1
    
    self.__linkattr__("n", "n_syn")
    self.__linkattr__("n", "n_spktr")
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


mc1 = mc.MicroCircuit("Test")
mc1.add(i2t)


r = precompiler.precompile(mc1, (0, 5))
compiler.compile(r, base)
