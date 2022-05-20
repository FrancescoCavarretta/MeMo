import numpy as np
import os
import sim.nwbio as nwbio
import sys



n_mod = 346
n_rtn = 7
n_bg = 17
n_bg = 17
n_drv = 35
g_mod = 0.0018

seed = 0

params = []

for g_drv in [0.00775]:
            for lesioned_flag in [ True, False ]:
                cellids = range(12) if lesioned_flag else range(17)
                for cellid in cellids:
                                        key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                                        
                                        if lesioned_flag:
                                            key += '-6ohda'
                                            
                                        params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':10000, 'key':key})
                                        
print (len(params))
np.save('test_simple.npy', params, allow_pickle=True)
print ('done')
