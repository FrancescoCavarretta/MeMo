import numpy as np
import os
import sim.nwbio as nwbio
import sys



n_mod = 346

params = []

for lesioned_flag in [ True, False ]:
    cellids = range(14) if lesioned_flag else range(26)
    for cellid in cellids:
        for seed in range(1):
            key = 'output-cellid=%d-seed=%d-tstop=15s' % (cellid, seed)
            
            if lesioned_flag:
                key += '-6ohda'
                
            params.append({'cellid':cellid, 'seed':seed, 'lesioned_flag':lesioned_flag, 'tstop':100, 'key':key})
                                        
print (len(params))
np.save('test.npy', params, allow_pickle=True)
print ('done')
