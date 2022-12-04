
if __name__ == '__main__':
    from parameters import Parameters
    import numpy as np
    import pandas as pd
    
    gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
    
    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_0.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for b in np.arange(0.1, 1.1, 0.1):
      par.add(n_drv=0, g_drv=0, g_mod=b*gsyn['CX'])
    print(len(par.params))
    par.close()


    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_1.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for b in [1]:
     for a in np.arange(0.02, 0.16, 0.01):
      par.add(n_drv=int(round(a * 346)), g_drv=(b * gsyn['CN_VM'] + (1 - b) * gsyn['CN_VL']), g_mod=0, n_mod=0)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_2.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for b in [0]:
     for a in np.arange(0.02, 0.16, 0.01):
      par.add(n_drv=int(round(a * 346)), g_drv=(b * gsyn['CN_VM'] + (1 - b) * gsyn['CN_VL']), g_mod=0, n_mod=0)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_3.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for b in [0.5]:
     for a in np.arange(0.02, 0.16, 0.01):
      par.add(n_drv=int(round(a * 346)), g_drv=(b * gsyn['CN_VM'] + (1 - b) * gsyn['CN_VL']), g_mod=0, n_mod=0)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_4.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for b in np.arange(0.0, 1.1, 0.1):
     for a in np.arange(0.02, 0.16, 0.02):
       par.add(n_drv=int(round(a * 346)), g_drv=(b * gsyn['CN_VM'] + (1 - b) * gsyn['CN_VL']), n_mod=0)
    print(len(par.params))
    par.close()


    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_5.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for b in np.arange(0.0, 1.1, 0.1):
     for a in np.arange(0.03, 0.16, 0.02):
         par.add(n_drv=int(round(a * 346)), g_drv=(b * gsyn['CN_VM'] + (1 - b) * gsyn['CN_VL']), n_mod=0)
    print(len(par.params))
    par.close()

    cfg = pd.read_csv('configuations_firing_rate.csv')
    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_firing_rate_6.npy', fmt='output-spont-%d', lesioned_flags=[False])
    for i, (g_mod, n_drv, g_drv) in cfg.iterrows():
         par.add(n_drv=n_drv, g_drv=g_drv, g_mod=g_mod)
    print(len(par.params))
    par.close()