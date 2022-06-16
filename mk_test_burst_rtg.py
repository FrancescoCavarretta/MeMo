import numpy as np
import os
import sim.nwbio as nwbio
import sys


params = []

for n_bg in [17]:
    n_rtn = int(round(n_bg / 17.0 * 7.0))
    
    for seed in [0]:
        for lesioned_flag in [ True, False ]:
            
            cellids = [2, 4, 6, 12, 13] if lesioned_flag else [1, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 20, 25]
            
            for rtgshift in [0]:
                for g_mod in ([0.0005] if lesioned_flag else [0.00125]):            
                    for cellid in cellids:
                        for burst_Regularity_bg in [1000.0]:
                            for burst_BurstMeanRate_bg in [3.5]:
                                    for MeanRate_drv in ([60.0] if lesioned_flag else [30.0]):
                                        for BurstFactor in [2.0]:
                                            b = {
                                                'burst_Tdur_bg':150.0, 'burst_Tpeak_bg':100.0, 'burst_MaxRate_bg':150.0 * BurstFactor, 'burst_MinRate_bg':100.0 * BurstFactor,
                                                'burst_BurstMeanRate_bg':burst_BurstMeanRate_bg, 'burst_MinInterPeriod_bg':200.0, 'burst_Regularity_bg':burst_Regularity_bg, 'burst_tinit_bg':7000.0, 'burst_tstop_bg':10000.0 }
                                             
                                            key = 'output-%d' % len(params)

                                            #for kb, vb in b.items():
                                            #    key += '-' + kb + '=' + str(vb)

                                            #key += '-' + 'MeanRate_drv' + '=' + str(MeanRate_drv)
                                            #key += '-' + 'BurstFreqFactor' + '=' + str(BurstFactor)
                                            
                                            #if lesioned_flag:
                                            #    key += '-6ohda'
                                                
                                            params.append({'cellid':cellid, 'seed':seed, 'n_bg':n_bg, 'g_mod':g_mod, 'n_rtn':n_rtn, 'lesioned_flag':lesioned_flag, 'tstop':16000, 'key':key, 'rtgshift':rtgshift})
                                            params[-1].update({'MeanRate_drv':MeanRate_drv})
                                            params[-1].update(b)
                                            print (lesioned_flag, key)



if __name__ == '__main__':                                    
    print (len(params))
    np.save('burst_test_retigabine_tris.npy', params, allow_pickle=True)
    print ('done')
