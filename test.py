
        
        
        
if __name__ == "__main__":
    import compiler.neuron as neuron
    
    import compiler.precompiler as precompiler
    
    import memo.spiketrain as st
    import memo.distribution as ds
    import memo.microcircuit as mc
    import memo.neuron as nrn
    import memo.link as ln
    
    import compiler
    
    mc1 = mc.MicroCircuit("Test")
    s1 = st.SpikeTrain("poissonian", mean_rate=55.0, tstop=500.)
    s2 = st.SpikeTrain("poissonian", mean_rate=25.0, tstop=500.)
    stp = st.SpikeTrainPopulation("Test", st1=s1, st2=s2)
    stp.n_st1=4
    stp.n_st2=8
    
    syn1 = nrn.Synapse("Test")
    sg = nrn.SynapseGroup("TestSyn", syn1=syn1)
    sg.n_syn1=4
    
    l = ln.Link(stp, sg)
    mc1.add(stp)
    mc1.add(sg)
    mc1.add(l)
    
    r = precompiler.precompile(mc1, (0,5))
    compiler.compile(r, neuron)
    
    