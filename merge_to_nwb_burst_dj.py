import numpy as np
import os
import sim.nwbio as nwbio
import sys



n_mod = 346
seed = 0
n_rtn = 7
n_bg = 26 #17
g_mod = 0.0018
g_drv = 0.00775
params = []

for n_bg in [17]:
    for seed in [0]:
        for n_drv in [35]:
            for lesioned_flag in [ False, True ]:
                cellids = [4] if lesioned_flag else [0]
                for cellid in cellids:
                    for burst_Regularity_bg in [None, 10.0, 1000.0]:
                        for burst_BurstMeanRate_bg in [3]:
                            for MeanRate_mod in [30.0]:
                                for MeanRate_drv in [30.0]:
                                    for BurstFactor in [2.0]:
                                        if burst_Regularity_bg is not None:
                                            b = {
                                                'burst_Tdur_bg':150.0, 'burst_Tpeak_bg':100.0, 'burst_MaxRate_bg':150.0 * BurstFactor, 'burst_MinRate_bg':100.0 * BurstFactor,
                                                'burst_BurstMeanRate_bg':burst_BurstMeanRate_bg, 'burst_MinInterPeriod_bg':200.0, 'burst_Regularity_bg':burst_Regularity_bg }
                                         
                                        key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (cellid, seed, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)

                                        if burst_Regularity_bg is not None:
                                            for kb, vb in b.items():
                                                key += '-' + kb + '=' + str(vb)

                                        key += '-' + 'MeanRate_drv' + '=' + str(MeanRate_drv)
                                        key += '-' + 'MeanRate_mod' + '=' + str(MeanRate_mod)
                                        
                                        if burst_Regularity_bg is not None:
                                            key += '-' + 'BurstFreqFactor' + '=' + str(BurstFactor)
                                        
                                        if lesioned_flag:
                                            key += '-6ohda'
                                            
                                        params.append({'cellid':cellid, 'seed':seed, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':4000, 'key':key})
                                        params[-1].update({'MeanRate_mod':MeanRate_mod, 'MeanRate_drv':MeanRate_drv})
                                        
                                        if burst_Regularity_bg is not None:
                                            params[-1].update(b)           
print (len(params))
np.save('burst_test_dj.npy', params, allow_pickle=True)
print ('done')
