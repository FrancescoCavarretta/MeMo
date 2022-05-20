import numpy as np
import os
import sim.nwbio as nwbio
import sys

cellid_control = [11, 3, 6, 2, 5, 1, 8, 3, 6, 11, 4, 2, 5, 15, 12, 14, 13, 16]
cellid_6ohda = [10, 11, 3, 7, 6, 2, 5]

g_mod = 0.0018
n_mod = 346


params = []

for seed in range(5):
    for lesioned_flag in [ True, False ]:
        cellids = cellid_6ohda if lesioned_flag else cellid_control
        for cellid in cellids:
            for g_drv in [0.0033, 0.00775, 0.0122]:
                for n_rtn in [0, 7, 14, 21, 28]:
                    for n_bg in [0, 17, 34, 52]:
                        for n_drv in [0, 17, 35, 52, 69]:
                            key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                            if lesioned_flag:
                                key += '-6ohda'            
                            params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':10000, 'key':key})
                                        
print (len(params))
np.save('test_syn.npy', params, allow_pickle=True)
print ('done')
