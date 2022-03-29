import thalamicsim as ts
from thalamicsim import mk_vm_microcircuit_test, base, compiler, precompiler, rec
import numpy as np

ntrial = 10
nmodel = 10







def clean(r):
    for _r in list( r.values() ):
        for __r in list( _r.values() ):
            if "real_simobj" in __r:
                del __r["real_simobj"]

## @neuron_modules
def _test(vmcircuit, input_name, gsyn, seed, vclamp, tstop=5500.0):
  from neuron import h
  import numpy as np
  
  setattr(list(vmcircuit.models)[0], "gsyn_" + input_name, gsyn)
  
  r = precompiler.precompile(vmcircuit, seed)
  
  compiler.compile(r, base)
  #h('forall gnap_max_TC_HH=0\nforall gna_max_TC_HH=0\npcabar_TC_iT_Des98=0')
  #print (time.time()-start)
  soma = r["models"][list(vmcircuit.models)[0].cell]["real_simobj"].section["somatic"][0]
 
  seclamp = h.SEClamp(soma(0.5))
  seclamp.amp1 = vclamp
  seclamp.dur1 = 5500
  
  rr_i = rec.Recorder(seclamp._ref_i, seg=soma(0.5))
  
  h.load_file("stdgui.hoc")
  h.CVode().active(1)
  h.tstop = tstop
  h.v_init = vclamp
  h.finitialize()
  
  h.run(tstop)
  
  
  data = rr_i.get()
  data = data[np.logical_and(data[:, 0] >= 5000, data[:,0]<=5250), :]
  data[:, 1] = np.abs(data[:, 1] - data[0, 1])
  #import matplotlib.pyplot as plt
  #plt.plot(data[:,0],data[:,1])
  #plt.show()
  Di = np.max(data[:, 1])
  
  clean(r)
  
  del seclamp
  return Di


def test(vmcirc, input_name, gsyn, vclamp, tstop=5500.0):
    from multiprocessing import Pool
    
    with Pool(ntrial) as p:    
        return p.starmap(_test, [ (vmcirc, input_name, gsyn, (iseed, iseed), vclamp, tstop)  for iseed in range(ntrial) ] )



def search_gsyn(input_name, peak_target, vclamp, n=1, tstop=5500.0, gmin=0.0, gmax=0.05, err=0.0001, **kwargs):


    def search(vmcirc, gmin, gmax, err, tstop):
        import numpy as np
        
        #import time
        while abs(gmin - gmax) > err:
            g = (gmin+gmax) / 2
            
            peak = test(vmcirc, input_name, g, vclamp, tstop=tstop)

            peak_mean = np.mean(peak)
            #print(f'{peak_mean}')
            if peak_mean < peak_target:
                gmin = g
            elif peak_mean > peak_target:
                gmax = g
            else:
                break
                
        return g


    g = []
    
    for i in range(nmodel):
        vmcirc, i2t = mk_vm_microcircuit_test(i)
        
        i2t.n_reticular = 0
        i2t.n_nigral = 0
        i2t.n_modulator = 0
        i2t.n_driver = 0    

        setattr(i2t, "n_" + input_name, n)
        
        base.set(**kwargs)

        g.append( search(vmcirc, gmin, gmax, err, tstop) )
        
    return g

            


g_mean_rtn =  search_gsyn("reticular",  24.43 / 1000.0,       -9.3, gmax=0.0015, ena=145.2, ek=-209.5, celsius=24)


print ("rtn", g_mean_rtn)


g = {"RTN":g_mean_rtn}

numpy.save("gsyn_rtn.npy", g, allow_pickle=True)

for k in g:
    print (k, np.mean(g[k]), np.std(g[k]))
