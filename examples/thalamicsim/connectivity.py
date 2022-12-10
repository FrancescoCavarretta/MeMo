import numpy as np

import MeMo.memo.model as model
import MeMo.memo.link as link
import MeMo.memo.neuron as nrn
import MeMo.memo.spiketrain as stn
import MeMo.memo.distribution as distr


# distribution of synapses by Bodor et al 2008
bodor_et_al2008 = {
    "xlabels":[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 'somatic'],
    "weights":np.array([5.33673534681342, 10.590606603532123, 24.91409649347326, 8.85334015868954, 16.012285641156904, 5.302981827489134, 5.387125671871004, 3.6572178141796883, 8.91140900947019, 1.739665984131058, 1.733267212695175, 6.980899667263891])
    }
bodor_et_al2008["weights"] /= np.sum(bodor_et_al2008["weights"])


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
