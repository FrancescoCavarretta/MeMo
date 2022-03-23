#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sim.memo.spiketrain as stn
import sim.compiler.neuron as nrn
import numpy as np
import matplotlib.pyplot as plt
import sim.compiler.precompiler as precompiler
import sim.compiler as compiler
import sim.compiler.neuron as base
import sim.memo.microcircuit as mc

b = stn.SpikeTrain('burst', 
                   Tpeak=25, Tdur=100, 
                   max_rate=400, 
                   fast_rise=True, fast_decay=True, 
                   refractory_period=(1/500.0/2*1000), 
                   time_unit = 'ms', 
                   intra_burst_k = 3, intra_burst_theta = 0.1, min_rate=200,
                   regularity=1.0, tstop=8000,
                   burst_mean_rate=1.0/0.5,
                   min_inter_period=1.0)


st = stn.SpikeTrain('abbasi', tstop=8000, mean_rate=100, 
                   refractory_period=(1/500.0/2*1000), time_unit = 'ms', 
                   regularity=1.0)

st.burst_model = b
sp = stn.SpikeTrainPopulation("Test", train=st, n_train=200)


sp.n_train=3


circuit = mc.MicroCircuit("Burst test")
circuit.add(sp)

r1 = precompiler.precompile(circuit, (0,5))
  
compiler.compile(r1, base)


for i, p in enumerate(r1["models"][sp]["real_simobj"].product):
    plt.eventplot(p.product, lineoffsets=i*2, color='red')




b = stn.SpikeTrain('burst', 
                   Tpeak=25, Tdur=100, 
                   max_rate=400, 
                   fast_rise=True, fast_decay=True, 
                   refractory_period=(1/500.0/2*1000), 
                   time_unit = 'ms', 
                   intra_burst_k = 3, intra_burst_theta = 0.1, min_rate=200,
                   regularity=1.0, tstop=8000,
                   burst_mean_rate=1.0/0.5,
                   min_inter_period=1.0)


st = stn.SpikeTrain('abbasi', tstop=8000, mean_rate=100, 
                   refractory_period=(1/500.0/2*1000), time_unit = 'ms', 
                   regularity=1.0)

st.burst_model = b
sp = stn.SpikeTrainPopulation("Test", train=st, n_train=200)


sp.n_train=3


circuit = mc.MicroCircuit("Burst test")
circuit.add(sp)

r2 = precompiler.precompile(circuit, (0,5))
  
for m in r2["models"]:
    if isinstance(m, stn.SpikeTrain):
        if "burst_model" in r2["models"][m]["submodels"]:
            del r2["models"][m]["submodels"]["burst_model"]
            m.burst_model = None
            #print (r2["models"][m])
#        try:
#            .burst_model  = None
#        except:
#            pass
        
compiler.compile(r2, base)



for i, p in enumerate(r2["models"][sp]["real_simobj"].product):
    plt.eventplot(p.product, lineoffsets=i*2+1)
plt.show()