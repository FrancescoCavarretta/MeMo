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
                   Tpeak=100.0,
                   Tdur=150.0, 
                   max_rate=150.0, 
                   fast_rise=False, fast_decay=True, 
                   refractory_period=1.5, 
                   time_unit = 'ms', 
                   intra_burst_k=3, intra_burst_theta = 0.1, min_rate=100,
                   regularity=1,
                   tstop=16000,
                   burst_mean_rate=0.25,
                   min_inter_period=200.0)


st = stn.SpikeTrain('abbasi', tstop=16000, mean_rate=60.0, 
                   refractory_period=10.0, time_unit = 'ms', 
                   regularity=1.0)

st.burst_model = b
sp = stn.SpikeTrainPopulation("Test", train=st, n_train=200)

            
sp.n_train = 10


circuit = mc.MicroCircuit("Burst test")
circuit.add(sp)

r1 = precompiler.precompile(circuit, (0,5))


            
compiler.compile(r1, base)


for i, p in enumerate(r1["models"][sp]["real_simobj"].product):
    plt.eventplot(p.product, lineoffsets=i, color='red', linewidth=0.1)




b = stn.SpikeTrain('burst', 
                   Tpeak=100.0,
                   Tdur=150.0, 
                   max_rate=150.0, 
                   fast_rise=False, fast_decay=True, 
                   refractory_period=1.5, 
                   time_unit = 'ms', 
                   intra_burst_k=3, intra_burst_theta = 0.1, min_rate=100,
                   regularity=1000,
                   tstop=16000,
                   burst_mean_rate=0.25,
                   min_inter_period=200.0)


st = stn.SpikeTrain('abbasi', tstop=16000, mean_rate=60.0, 
                   refractory_period=10.0, time_unit = 'ms', 
                   regularity=1.0)

st.burst_model = b
sp = stn.SpikeTrainPopulation("Test", train=st, n_train=200)

            
sp.n_train = 10


circuit = mc.MicroCircuit("Burst test")
circuit.add(sp)

r1 = precompiler.precompile(circuit, (0,5))


            
compiler.compile(r1, base)


for i, p in enumerate(r1["models"][sp]["real_simobj"].product):
    plt.eventplot(p.product, lineoffsets=i + 10, color='blue', linewidth=0.1)
plt.show()
