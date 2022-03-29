
        
        
        
import sim.compiler.neuron as base

import sim.compiler.precompiler as precompiler
import sim.compiler as compiler

import sim.memo.spiketrain as st
import sim.memo.distribution as ds
import sim.memo.microcircuit as mc
import sim.memo.neuron as nrn
import sim.memo.link as ln

import sim.compiler
import sim.compiler.neuron.util.recorder as recorder


d4 = ds.Distribution("empirical", x=[0,1,2,3,4,5,6,7], freq=[1,2,3,4,5,4,3,2])
mc1 = mc.MicroCircuit("Test")
mc1.add(d4)
r = precompiler.precompile(mc1, (0,5))
compiler.compile(r, base)
print ( r["models"][d4]["real_simobj"]() )
print ( r["models"][d4]["real_simobj"]() )
print ( r["models"][d4]["real_simobj"]() )
# mc1 = mc.MicroCircuit("Test")
# s1 = st.SpikeTrain("poissonian", mean_rate=55.0, tstop=0.5, refractory_period=0.005)
# s1.time_unit = "ms"
# s2 = st.SpikeTrain("poissonian", mean_rate=25.0, tstop=0.5, refractory_period=0.005)
# s2.time_unit = "ms"
# stp = st.SpikeTrainPopulation("Test", st1=s1, st2=s2)
# stp.n_st1=5
# stp.n_st2=5
# c = nrn.Cell("TestCell")

# syn1 = nrn.Synapse("ExpSyn")
# syn1.gsyn = 0.5

# sg = nrn.SynapseGroup("TestSyn", syn1=syn1)
# sg.n_syn1=12

# lst = ln.Link(stp, sg)
# lsg = ln.Link(sg, c)

# mc1.add(stp)
# mc1.add(sg)
# mc1.add(lst)

# mc1.add(lsg)
# mc1.add(c)

# r = precompiler.precompile(mc1, (0,5))
# compiler.compile(r, base)

# from neuron import h
# h("forall insert pas")
# h.load_file("nrngui.hoc")
# h.cvode_active(1)

# rr = recorder.Recorder(r["models"][c]['real_simobj'].Section(0.5))

# h.tstop = 600
# h.run(500)
# print (h.t)
# import matplotlib.pyplot as plt
# data = rr.get()
# print (data)
# plt.plot(data[:,0], data[:,1])
# plt.show()
