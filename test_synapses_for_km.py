import thalamicsim as ts
from thalamicsim import mk_vm_microcircuit_test, base, compiler, precompiler, rec
import numpy as np
import sys

ntrial = 15
nmodel = 10







def clean(r):
    for _r in list( r.values() ):
        for __r in list( _r.values() ):
            if "real_simobj" in __r:
                del __r["real_simobj"]

## @neuron_modules
def _test(vmcircuit, input_name, gsyn, seed, tstop=5500.0, current_flag=False):
  from neuron import h
  import numpy as np
  
  setattr(list(vmcircuit.models)[0], "gsyn_" + input_name, gsyn)
  
  r = precompiler.precompile(vmcircuit, seed)
  
  compiler.compile(r, base)
  
  #print (time.time()-start)
  soma = r["models"][list(vmcircuit.models)[0].cell]["real_simobj"].section["somatic"][0]
 
  if current_flag:
      seclamp = h.SEClamp(soma(0.5))
      if input_name == 'reticular' or input_name == 'nigral':
          seclamp.amp1 = -25.0
      else:
          seclamp.amp1 = -50.0
      seclamp.dur1 = tstop
      rr = rec.Recorder(seclamp._ref_i, seg=soma(0.5))
  else:
      rr = rec.Recorder(soma(0.5)._ref_v, seg=soma(0.5))
  
  h.load_file("stdgui.hoc")
  h.CVode().active(1)
  h.tstop = tstop
  h.v_init = -79.0
  h.finitialize()
  
  h.run(tstop)
  
  
  #data = rr_i.get()
  data = rr.get()
  data = data[np.logical_and(data[:, 0] >= 5000, data[:,0]<=5250), :]
  data[:, 1] = np.abs(data[:, 1] - data[0, 1])
  Dv = np.max(data[:, 1])
  
  clean(r)
  
  return Dv


def test(vmcirc, input_name, gsyn, tstop=5500.0, current_flag=False):
    from multiprocessing import Pool
    
    with Pool(ntrial) as p:    
        return p.starmap(_test, [ (vmcirc, input_name, gsyn, (iseed, iseed), tstop, current_flag )  for iseed in range(ntrial) ] )



def test_on_all_models(input_name, n=1, g=0.0, tstop=5500.0, current_flag=False):
    
    DeltaV = []
    
    for i in range(nmodel):
        vmcirc, i2t = mk_vm_microcircuit_test(i)
        i2t.n_reticular = 0
        i2t.n_nigral = 0
        i2t.n_modulator = 0
        i2t.n_driver = 0  
        
        setattr(i2t, "n_" + input_name, n)
        
        DeltaV.append( test(vmcirc, input_name, g, tstop=tstop, current_flag=current_flag) )
        print (i, input_name)
        
    return DeltaV


dv_rtn =  test_on_all_models("reticular",  g=0.0008, current_flag=('--current' in sys.argv))
dv_snr =  test_on_all_models("nigral",  g=0.0015, current_flag=('--current' in sys.argv))
dv_drv =  test_on_all_models("driver",  g=0.0033, current_flag=('--current' in sys.argv))
dv_mod =  test_on_all_models("modulator",  g=0.0018, current_flag=('--current' in sys.argv))

print ("rtn", dv_rtn)
print ("snr", dv_snr)
print ("drv", dv_drv)
print ("mod", dv_mod)


suffix = 'i' if '--current' in sys.argv else 'v'
if ts.lesioned_flag:
    filename = "delta_" + suffix + "_single_pulse_6ohda.npy"
else:
    filename = "delta_" + suffix + "_single_pulse.npy"
    
np.save(filename, {
    "reticular":dv_rtn,
    "nigral":dv_snr,
    "driver":dv_drv,
    "modulator":dv_mod
    }, allow_pickle=True)
