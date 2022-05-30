import numpy as np
import os
import sim.nwbio as nwbio
import sys

g_mod = 0.0018
n_mod = 346


params = []

param_space = np.array([[3.30e-03, 1.70e+01, 1.70e+01, 0.00e+00],
                        [3.30e-03, 1.70e+01, 1.70e+01, 7.00e+00],
                        [3.30e-03, 1.70e+01, 1.70e+01, 1.40e+01],
                        [3.30e-03, 1.70e+01, 1.70e+01, 2.10e+01],
                        [3.30e-03, 1.70e+01, 1.70e+01, 2.80e+01],
                        [1.22e-02, 1.70e+01, 3.40e+01, 0.00e+00],
                        [1.22e-02, 1.70e+01, 3.40e+01, 7.00e+00],
                        [1.22e-02, 1.70e+01, 3.40e+01, 1.40e+01],
                        [1.22e-02, 1.70e+01, 3.40e+01, 2.10e+01],
                        [1.22e-02, 1.70e+01, 3.40e+01, 2.80e+01],
                        [3.30e-03, 3.50e+01, 1.70e+01, 0.00e+00],
                        [3.30e-03, 3.50e+01, 1.70e+01, 7.00e+00],
                        [3.30e-03, 3.50e+01, 1.70e+01, 1.40e+01],
                        [3.30e-03, 3.50e+01, 1.70e+01, 2.10e+01],
                        [3.30e-03, 3.50e+01, 1.70e+01, 2.80e+01],
                        [7.75e-03, 3.50e+01, 3.40e+01, 0.00e+00],
                        [7.75e-03, 3.50e+01, 3.40e+01, 7.00e+00],
                        [7.75e-03, 3.50e+01, 3.40e+01, 1.40e+01],
                        [7.75e-03, 3.50e+01, 3.40e+01, 2.10e+01],
                        [7.75e-03, 3.50e+01, 3.40e+01, 2.80e+01],
                        [1.22e-02, 3.50e+01, 5.20e+01, 0.00e+00],
                        [1.22e-02, 3.50e+01, 5.20e+01, 7.00e+00],
                        [1.22e-02, 3.50e+01, 5.20e+01, 1.40e+01],
                        [1.22e-02, 3.50e+01, 5.20e+01, 2.10e+01],
                        [1.22e-02, 3.50e+01, 5.20e+01, 2.80e+01],
                        [7.75e-03, 5.20e+01, 5.20e+01, 0.00e+00],
                        [7.75e-03, 5.20e+01, 5.20e+01, 7.00e+00],
                        [7.75e-03, 5.20e+01, 5.20e+01, 1.40e+01],
                        [7.75e-03, 5.20e+01, 5.20e+01, 2.10e+01],
                        [7.75e-03, 5.20e+01, 5.20e+01, 2.80e+01],
                        [3.30e-03, 6.90e+01, 3.40e+01, 0.00e+00],
                        [3.30e-03, 6.90e+01, 3.40e+01, 7.00e+00],
                        [3.30e-03, 6.90e+01, 3.40e+01, 1.40e+01],
                        [3.30e-03, 6.90e+01, 3.40e+01, 2.10e+01],
                        [3.30e-03, 6.90e+01, 3.40e+01, 2.80e+01]])

for seed in range(5):
    for lesioned_flag in [ True, False ]:
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for g_drv, n_drv, n_bg, n_rtn in param_space:
                
                g_drv = float(g_drv)
                n_drv = int(n_drv)
                n_bg = int(n_bg)
                n_rtn = int(n_rtn)

                
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                if lesioned_flag:
                    key += '-6ohda'            
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})
                                        
print (len(params))
np.save('selected_cfg.npy', params, allow_pickle=True)
print ('done')
