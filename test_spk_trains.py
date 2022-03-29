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


bgST = stn.SpikeTrainPopulation("spktr", spktr=stn.SpikeTrain("abbasi", regularity=0.5, mean_rate=20.0, tstop=2000.0, refractory_period=5.0, time_unit="ms"))
rtnST = stn.SpikeTrainPopulation("spktr", spktr=stn.SpikeTrain("abbasi", regularity=0.5, mean_rate=30.0, tstop=2000.0, refractory_period=5.0, time_unit="ms"))
drvST = stn.SpikeTrainPopulation("spktr", spktr=stn.SpikeTrain("abbasi", regularity=0.5, mean_rate=40.0, tstop=2000.0, refractory_period=5.0, time_unit="ms"))
modST = stn.SpikeTrainPopulation("spktr", spktr=stn.SpikeTrain("abbasi", regularity=0.5, mean_rate=10.0, tstop=2000.0, refractory_period=5.0, time_unit="ms"))
modST.n_spktr = 100

drvST.n_spktr = 30

bgST.n_spktr = 20
rtnST.n_spktr = 10

vmcircuit = mc.MicroCircuit("VMThalamus")
vmcircuit.add(modST)
vmcircuit.add(drvST)
vmcircuit.add(bgST)
vmcircuit.add(rtnST)


r = precompiler.precompile(vmcircuit, (0, 5))
compiler.compile(r, base)

i = 0
for k, v in r["models"].items():
  if isinstance(k, stn.SpikeTrainPopulation):
    try:
      for tt in v['real_simobj'].product:
        plt.eventplot(tt.product, lineoffsets=i, color='black', linewidths=1)
        i += 1
      
      i += 10
    except:
      pass

plt.show()
