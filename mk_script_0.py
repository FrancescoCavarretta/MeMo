import numpy as np
import os
import sim.nwbio as nwbio
import sys



n_mod = 346
g_mod = 0.0018

params = []

for g_drv in [0.0033, 0.00775, 0.0122]:
    for n_rtn in [0,7,14,21,28]:
        for n_bg in [0, 17, 34, 52]:
            for n_drv in [ 0, 17, 34, 52, 69 ]:
                for lesioned_flag in [ False, True ]:
                    cellids = range(14) if lesioned_flag else range(26)
                    for cellid in cellids:
                        for seed in range(5):
                            key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                            
                            if lesioned_flag:
                                key += '-6ohda'
                                
                            params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})
                                        
print (len(params))
np.save('test_simple.npy', params, allow_pickle=True)
print ('done')
