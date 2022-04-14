import numpy as np
import os
import sim.nwbio as nwbio
import sys


fw = nwbio.FileWriter('../all_traces_3.nwb', "thalamic_test", "thalamic_test_id")

n_mod_ctl = 346
n_rtn = 7
params = []

n = 0
oldst = ''

for g_drv in [ 0.0033, 0.00775, 0.0122 ]:
    for g_mod in [ 0.0018 ]:
        for lesioned_flag in [ False, True ]:
            
            for p_var_mod in [ 0.0 ]:
                n_mod = int(round((1+p_var_mod) * n_mod_ctl))   


                for n_bg_fiber_factor in [ 4, 5, 6 ]:
                    n_bg = int(round(n_bg_fiber_factor * 8.5))

                    for p_driver in [ 0 ]:
                        n_drv = int(round(p_driver * n_mod_ctl))
                        for i in range(10):
                            for j in range(10):
                                key = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g-g_mod=%g' % (i, j, n_drv, n_mod, n_bg, n_rtn, g_drv, g_mod)
                                if lesioned_flag:
                                    key += '-6ohda'
                                filename = '../MeMo_All_traces/all_traces_2.nwb.' + key + '.npy'
                                
                                n += 1
                                newst = '%.0f%%\n' % (n / (3*2*6*4*100) * 100)
                                
                                if newst != oldst:
                                    oldst = newst
                                    print ('\n' * 30)
                                    for kk in range(int(n / (3*2*6*4*100) * 50)):
                                        sys.stdout.write('█')
                                    sys.stdout.write(newst)
                                    sys.stdout.flush()
                                
                                try:
                                    data = np.load(filename, allow_pickle=True)
                                    fw.add(key, data[0], data[1])
                                except:
                                    #if not os.path.exists(filename):
                                    params.append({'cellid':i, 'seed':j, 'n_drv':n_drv, 'n_mod':n_mod, 'n_bg':n_bg, 'n_rtn':n_rtn, 'g_drv':g_drv, 'lesioned_flag':lesioned_flag, 'tstop':10000, 'key':key})
                                
fw.close()
print (params)
#np.save('repeat_simulation.npy', params, allow_pickle=True)

