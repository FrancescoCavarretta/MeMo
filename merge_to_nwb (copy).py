import numpy as np
import os
import sim.nwbio as nwbio
import sys


#fr0 = nwbio.FileReader('../all_traces_0.nwb')
#fr1 = nwbio.FileReader('../all_traces_1.nwb')

n_mod_ctl = 346
#n_rtn = 7
params = []

n = 0
oldst = ''

for n_rtn in [ 21 ]:
    for g_drv in [ 0.0033, 0.00775, 0.0122 ]:
        for g_mod in [ 0.0018 ]:
            for lesioned_flag in [ False, True ]:
                
                for p_var_mod in [ 0.0 ]:
                    n_mod = int(round((1+p_var_mod) * n_mod_ctl))   


                    for n_bg_fiber_factor in [ 0,1,2,3,4,5,6 ]:
                        n_bg = int(round(n_bg_fiber_factor * 8.5))

                        for p_driver in [ 0.0, 0.05, 0.1, 0.15, 0.2 ]:
                            n_drv = int(round(p_driver * n_mod_ctl))
                            for i in range(10):
                                for j in range(10):
                                    key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (i, j, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                                    if lesioned_flag:
                                        key += '-6ohda'
                                    filename = '../output/' + key + '.npy'
                                    
                                    n += 1
                                    newst = '%.0f%%\n' % (n / (3*2*6*4*100) * 100)
                                    
                                    if newst != oldst:
                                        oldst = newst
                                        print ('\n' * 30)
                                        for kk in range(int(n / (3*2*6*4*100) * 50)):
                                            sys.stdout.write('█')
                                        sys.stdout.write(newst)
                                        sys.stdout.flush()

                                    #if key not in fr0.nwbfile.acquisition and key not in fr1.nwbfile.acquisition:
                                    params.append({'cellid':i, 'seed':j, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':10000, 'key':key})                                    
                                
#fr0.close()
#fr1.close()
np.save('repeat_simulation_4.npy', params, allow_pickle=True)

