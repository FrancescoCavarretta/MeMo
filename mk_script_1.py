import numpy as np
import os
import sim.nwbio as nwbio
import sys



n_mod = 346
n_drv = 17
n_bg = 17
n_rtn = 7

g_mod = 0.002
g_drv = 0.0021
g_bg = 0.001
g_rtn = 0.0006

NmdaAmpaRatio_drv = 0.6
NmdaAmpaRatio_mod = 1.91


params = []

def add_param(name, val):
    for lesioned_flag in [ True, False ]:
        cellids = [2, 4, 6, 12, 13] if lesioned_flag else [1, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 20, 25]
        for cellid in cellids:
            for seed in range(1):
                key = 'output-cellid=%d-seed=%d-tstop=15s' % (cellid, seed)
                key += '-' + name + '=' + str(val)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key, name:val})



for p in [ 0.75, 0.875  ]:
    _g_mod = p * g_mod
    add_param('g_mod', _g_mod)
    
                                        
print (len(params))
np.save('test_syn_properties_3.npy', params, allow_pickle=True)
print ('done')
