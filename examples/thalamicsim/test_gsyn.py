import thalamicsim as ts
from thalamicsim import mk_vm_microcircuit_test, base, compiler, precompiler, recorder as rec
import numpy as np

ntrial = 10
nmodel = len([k for k in np.load('vmcell/hof_3sd_0_good.npy', allow_pickle=True).tolist().keys() if k[0].startswith('control')])
print ('nmodel', nmodel)


def clean(r):
    for _r in list( r.values() ):
        for __r in list( _r.values() ):
            if "real_simobj" in __r:
                del __r["real_simobj"]


## @neuron_modules
def _test(cellid, input_name, gsyn, nsyn, seed, vclamp, kwargs, tstop=5500.0):
  from neuron import h
  import numpy as np

  vmcircuit, i2t = mk_vm_microcircuit_test(cellid, False)

  i2t.n_reticular = 0
  i2t.n_nigral = 0
  i2t.n_modulator = 0
  i2t.n_driver = 0    

  setattr(i2t, "n_" + input_name, nsyn)
  
  
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
  
  base.set(**kwargs)
  
  h.CVode().active(1)
  h.tstop = tstop
  h.v_init = vclamp
  h.finitialize()
  
  h.run(tstop)
  
  
  data = rr_i.get()
  data = data[np.logical_and(data[:, 0] >= 5000, data[:,0]<=5250), :]
  data[:, 1] = np.abs(data[:, 1] - data[0, 1])

  Di = np.max(data[:, 1])
  
  clean(r)
  
  del seclamp
  return Di


def test(input_name, gsyn, vclamp, nsyn, tstop=5500.0, **kwargs):
    from multiprocessing import Pool
    
    params = []
    for cellid in range(nmodel):
        for iseed in range(ntrial):
            params.append((cellid, input_name, gsyn, nsyn, (iseed, iseed), vclamp, kwargs, tstop))
            
    with Pool(44) as p:    
        return p.starmap(_test, params )


    
def search_gsyn(input_name, peak_target, vclamp, n=1, tstop=5500.0, gmin=0.0, gmax=0.05, err=0.0001, **kwargs):

    import numpy as np

    
    
    #import time
    while abs(gmin - gmax) > err:
        g = (gmin+gmax) / 2
        
        peak = test(input_name, g, vclamp, n, tstop=tstop, **kwargs)
        
        peak_mean = np.mean(peak)

        print ('\t', peak_mean)
        
        if peak_mean < peak_target:
            gmin = g
        elif peak_mean > peak_target:
            gmax = g
        else:
            break
    print ('\tfinal:', peak_mean)
    return g


g_mean_snr_1 = search_gsyn("nigral",  2.7 * 4.1 / 1000.0, -64.0, n=1, ena=60.1, ek=-105.8, celsius=32) 
print ("SNRx1", g_mean_snr_1)
g_mean_snr_3 = search_gsyn("nigral",  2.7 * 4.1 / 1000.0, -64.0, n=3, ena=60.1, ek=-105.8, celsius=32) 
print ("SNRx3", g_mean_snr_3)
g_mean_snr_13 = search_gsyn("nigral", 19.4 * 4.1 / 1000.0, -64.0, n=13, ena=60.1, ek=-105.8, celsius=32)
print ("SNRx13", g_mean_snr_13)

g_mean_rtn =  search_gsyn("reticular",  24.43 / 1000.0,     -9.3,  gmax=0.0015, ena=145.2, ek=-209.5, celsius=24, ion_channel_blocker=['TTX', 'Cs', 'AP5'])
print ("rtn", g_mean_rtn)

g_mean_cx = search_gsyn("modulator",  28.4 / 1000.0,       -79.3, ena=145.2, ek=-209.5, celsius=24, ion_channel_blocker=['TTX', 'Cs', 'AP5'])
print ("cx", g_mean_cx)

g_mean_cn_vm = search_gsyn("driver",  165.0 / 1000.0,   -68.4, ena=64.8, n=4, ek=-107.1, celsius=34, ion_channel_blocker=['TTX'])
print ("vm", g_mean_cn_vm)

g_mean_cn_vl = search_gsyn("driver",  847.7 / 1000.0,   -68.4, ena=64.8, n=4, ek=-107.1, celsius=34, ion_channel_blocker=['TTX'])
print ("vl", g_mean_cn_vl)


g = {"SNRx13":g_mean_snr_13, "SNRx1":g_mean_snr_1, "SNRx3":g_mean_snr_3,
     "CX":g_mean_cx,
     "CN_VM":g_mean_cn_vm,
     "CN_VL":g_mean_cn_vl,
     "RTN": g_mean_rtn}

np.save("gsyn.npy", g, allow_pickle=True)

for k in g:
    print (k, np.mean(g[k]))
