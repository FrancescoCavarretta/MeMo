
        
        
        
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


mc1 = mc.MicroCircuit("Test")
s1 = st.SpikeTrain("poissonian", mean_rate=55.0, tstop=0.5, refractory_period=0.005)
s1.time_unit = "ms"
s2 = st.SpikeTrain("poissonian", mean_rate=25.0, tstop=0.5, refractory_period=0.005)
s2.time_unit = "ms"
stp = st.SpikeTrainPopulation("Test", st1=s1, st2=s2)
stp.n_st1=4
stp.n_st2=8
c = nrn.Cell("TestCell")

syn1 = nrn.Synapse("Test")
syn1.gsyn = 0.5

sg = nrn.SynapseGroup("TestSyn", syn1=syn1)
sg.n_syn1=12

lst = ln.Link(stp, sg)
lsg = ln.Link(sg, c)

mc1.add(stp)
mc1.add(sg)
mc1.add(lst)

mc1.add(lsg)
mc1.add(c)

r = precompiler.precompile(mc1, (0,5))
compiler.compile(r, base)

from neuron import h
h("forall insert pas")
h.load_file("nrngui.hoc")
h.cvode_active(1)

#print ( r["models"][syn1]['real_simobj'].product["NetCon"].weight[0] )

rr = recorder.Recorder(r["models"][c]['real_simobj'].Section(0.5))
ns=h.NetStim(0.5)
ns.start=90.0
ns.interval=50.0


#nc = h.NetCon(None, r["models"][syn1]["real_simobj"].product["Exp2Syn"])
#nc.x=r["links"][l1]["real_simobj"].product["VecStim"]
#nc.weight[0]=0.5

h.tstop = 600
h.run(500)
print (h.t)
import matplotlib.pyplot as plt
data = rr.get()
print (data)
plt.plot(data[:,0], data[:,1])
plt.show()
