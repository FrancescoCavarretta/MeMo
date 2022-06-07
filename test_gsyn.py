import thalamicsim as ts
from thalamicsim import mk_vm_microcircuit_test, base, compiler, precompiler, rec
import numpy as np

ntrial = 5
nmodel = len(np.load('mkcell/test_model_control_edyta_test_good.npy', allow_pickle=True).tolist())







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
##  import matplotlib.pyplot as plt
##  plt.plot(data[:,0],data[:,1])
##  plt.show()
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
            
            if peak_mean < peak_target:
                gmin = g
            elif peak_mean > peak_target:
                gmax = g
            else:
                break
                
        return g


    g = []
    
    for i in range(nmodel):
        vmcirc, i2t = mk_vm_microcircuit_test(i, False)
        
        i2t.n_reticular = 0
        i2t.n_nigral = 0
        i2t.n_modulator = 0
        i2t.n_driver = 0    

        setattr(i2t, "n_" + input_name, n)
        
        base.set(**kwargs)

        g.append( search(vmcirc, gmin, gmax, err, tstop) )
        
    return g

            
g_mean_rtn =  search_gsyn("reticular",  24.43 / 1000.0,     -9.3,  gmax=0.0015, ena=145.2, ek=-209.5, celsius=24)

g_mean_cx = search_gsyn("modulator",  28.4 / 1000.0,       -79.3, ena=145.2, ek=-209.5, celsius=24)

g_mean_cn_vm = search_gsyn("driver",  165.0 / 1000.0,   -68.4, ena=64.8, n=4, ek=-107.1, celsius=34) 
g_mean_cn_vl = search_gsyn("driver",  847.7 / 1000.0,   -68.4, ena=64.8, n=4, ek=-107.1, celsius=34)

#g_min_cn_vm  = search_gsyn("driver", (165.0-139.2) / 1000.0, -68.4, n=2, ena=64.8, ek=-107.1, celsius=34)
#g_max_cn_vm  = search_gsyn("driver", (165.0+139.2) / 1000.0, -68.4, n=5, ena=64.8, ek=-107.1, celsius=34)

#g_min_sc  = search_gsyn("driver", (238.0-82.5) / 1000.0, -70, ena=109.3, ek=-103.9, celsius=32)
#g_mean_sc = search_gsyn("driver",  238.0 / 1000.0,       -70, ena=109.3, ek=-103.9, celsius=32) 
#g_max_sc  = search_gsyn("driver", (238.0+82.5) / 1000.0, -70, ena=109.3, ek=-103.9, celsius=32)

#g_mean_snr_1 = search_gsyn("nigral",  2.7 * 4.1 / 1000.0, -64.0, n=1, ena=60.1, ek=-105.8, celsius=32) 
#g_mean_snr_3 = search_gsyn("nigral",  2.7 * 4.1 / 1000.0, -64.0, n=3, ena=60.1, ek=-105.8, celsius=32) 
g_mean_snr_13 = search_gsyn("nigral", 19.4 * 4.1 / 1000.0, -64.0, n=13, ena=60.1, ek=-105.8, celsius=32)

print ("rtn", g_mean_rtn)
print ("cx", g_mean_cx)
print ("vm", g_mean_cn_vm)
print ("vl", g_mean_cn_vl)
#print ("SC", g_min_sc, g_mean_sc, g_max_sc)
#print ("SNRx1", g_mean_snr_1, "SNRx3", g_mean_snr_3, "SNRx13", g_mean_snr_13)
print ("SNRx13", g_mean_snr_13)



##g = {"SNRx1":g_mean_snr_1,
##     "SNRx3":g_mean_snr_3,
##     "SNRx13":g_mean_snr_13,
##     "CX":g_mean_cx,
##     "CN_VM":g_mean_cn_vm,
##     "CN_VL":g_mean_cn_vl,
##     "CN_VM_MIN":g_min_cn_vm,
##     "CN_VM_MAX":g_max_cn_vm,
##     "SC_MIN":g_min_sc,
##     "SC_MEAN":g_mean_sc,
##     "SC_MAX":g_max_sc,
##     "rtn": g_mean_rtn}

g = {"SNRx13":g_mean_snr_13,
     "CX":g_mean_cx,
     "CN_VM":g_mean_cn_vm,
     "CN_VL":g_mean_cn_vl,
     "rtn": g_mean_rtn}

np.save("gsyn.npy", g, allow_pickle=True)

for k in g:
    print (k, np.mean(g[k]))
