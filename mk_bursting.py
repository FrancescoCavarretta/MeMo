
if __name__ == '__main__':
    from parameters import Parameters
    import numpy as np
    import pandas as pd
    
    gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
    amod = 0.2
    adrv = 0.1
    #ndrv = 35
    print('driver', (adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']) )
    print('modulator', amod*gsyn['CX'] )

    '''par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_spiketrain.npy', fmt='output-burst-off-%d', lesioned_flags=[True], cellids=[0])
    for percsync in [0.0, 1.0]:
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)

    for percsync in [0.0, 1.0]:
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)

    print(len(par.params))
    par.close()

    from parameters import Parameters
    import numpy as np
    import pandas as pd
    
    gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
    amod = 0.2
    adrv = 0.25
    ndrv = 35
    print('driver', (adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']) )
    print('modulator', amod*gsyn['CX'] )

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_spiketrain_short_async.npy', fmt='output-burst-off-%d', lesioned_flags=[True, False])
    for percsync in [.0]:
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=13000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)

    for percsync in [.0]:
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=13000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)

    print(len(par.params))
    par.close()'''
    
    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_off.npy', fmt='output-burst-off-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_on.npy', fmt='output-burst-on-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()    

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_off_2.npy', fmt='output-burst-off-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(seed_start=5, tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_on_2.npy', fmt='output-burst-on-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(seed_start=5, tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()    



    gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
    amod = 0.1
    adrv = 0.1
    #ndrv = 35
    print('driver', (adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']) )
    print('modulator', amod*gsyn['CX'] )

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_off_3.npy', fmt='output-burst-off-%d', lesioned_flags=[True])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_on_3.npy', fmt='output-burst-on-%d', lesioned_flags=[True])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()    

    gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
    amod = 0.2
    adrv = -0.05
    #ndrv = 35
    print('driver', (adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']) )
    print('modulator', amod*gsyn['CX'] )

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_off_4.npy', fmt='output-burst-off-%d', lesioned_flags=[True])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_on_4.npy', fmt='output-burst-on-%d', lesioned_flags=[True])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()    

    gsyn = np.load('gsyn.npy', allow_pickle=True).tolist()
    amod = 0.2
    adrv = 0.1
    #ndrv = 35
    print('driver', (adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']) )
    print('modulator', amod*gsyn['CX'] )
    print('BG', 1.5*gsyn['SNRx1'])

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_off_5.npy', fmt='output-burst-off-%d', lesioned_flags=[True])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, g_bg=1.5*gsyn['SNRx1'], tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_on_5.npy', fmt='output-burst-on-%d', lesioned_flags=[True])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(ntrial=10, g_bg=1.5*gsyn['SNRx1'], tstop=30000, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()    


    '''par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_1_off.npy', fmt='output-burst-off-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(seed_start=5, tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_1_on.npy', fmt='output-burst-on-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(seed_start=5, tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close() 


    amod = 0.05
    adrv = 0.25
    ndrv = 35
    print('driver', (adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']) )
    print('modulator', amod*gsyn['CX'] )
    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_2_off.npy', fmt='output-burst-off-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_2_on.npy', fmt='output-burst-on-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close() 

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_3_off.npy', fmt='output-burst-off-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':0.0, 'burst_Tpeak_bg':0.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(seed_start=5, tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close()

    par = Parameters(np.load('mkcell/hof_3sd_good_2nd.npy', allow_pickle=True).tolist(), 'test_bursting_v2_3_on.npy', fmt='output-burst-on-%d', lesioned_flags=[True, False])
    for percsync in np.arange(0.0, 1.1, 0.1):
        b = dict({ 'burst_Tdur_bg':100.0, 'burst_Tpeak_bg':20.0, 'burst_MaxRate_bg':320.0, 'burst_MinRate_bg':35.0,
                   'burst_BurstMeanRate_bg':1.0, 'burst_MinInterPeriod_bg':100.0, 'burst_RegularitySync_bg':5000000, 'burst_RegularityAsync_bg':5, 'burst_PercentSync_bg':percsync, 'burst_tstop_bg':30000, 'burst_tinit_bg':10000 })
        par.add(seed_start=5, tstop=30000, n_drv=ndrv, g_drv=(adrv * gsyn['CN_VL'] + (1 - adrv) * gsyn['CN_VM']), g_mod=amod*gsyn['CX'], MeanRate_bg=35.0, Regularity_bg=50, **b)
    print(len(par.params))
    par.close() '''
