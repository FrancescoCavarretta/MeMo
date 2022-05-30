import numpy as np
import os
import sim.nwbio as nwbio
import sys





params = []

n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for g_drv in [0.0033, 0.00775, 0.0122]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})


n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for g_mod in [0.0018, 0.0018 * 1.5, 0.0018 * 2]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})


n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for g_rtn in [0.0008, 0.0008 * 1.5, 0.0008 * 2]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})


n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for g_bg in [0.0015, 0.0015 * 1.5, 0.0015 * 2]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})
n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for n_mod in [0, 173, 346, 519]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})
                
n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for n_drv in [0, 17, 35, 52, 69]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})
                
n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for n_rtn in [0, 7, 14, 21, 28]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})


n_mod = 346
n_drv = 34
n_rtn = 7
n_bg = 17
g_rtn = 0.0008
g_bg = 0.0015
g_mod = 0.0018
g_drv = 0.0033

for n_bg in [0, 17, 34, 52, 68]:
    for lesioned_flag in [ False, True ]:                    
        cellids = [ 9,  8,  6,  5,  4,  2, 13, 12,  1] if lesioned_flag else [ 9,  7,  6,  5,  4,  3, 23, 21, 20,  2, 16, 15, 14, 13, 11, 10,  1]
        for cellid in cellids:
            for seed in range(5):
                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                
                if lesioned_flag:
                    key += '-6ohda'
                    
                params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':15000, 'key':key})

print (len(params))
np.save('test_simple_bis.npy', params, allow_pickle=True)
print ('done')
