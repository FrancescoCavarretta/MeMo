# import libraries
import numpy as np
import pandas as pd
import sim.nwbio as nwbio
import preprocessing

def read_table(files, tinit=10000.0, tstop=20000.0):
    tab = pd.DataFrame()

    for i, (cfg_filename, nwb_filename) in enumerate(files):

        _tab = pd.DataFrame(np.load(cfg_filename, allow_pickle=True).tolist()).set_index('key')
        f = nwbio.FileReader(nwb_filename) 

        _tab['file_object'] = f

        for file_key in f.nwbfile.acquisition.keys():
            if '_ref_v' not in file_key:
                continue
            k = file_key.split('.')[0]
            _tab.loc[file_key.split('.')[0], 'file_key'] = file_key    

        # set the data types
        for col in tab.columns:
            # eliminate excess of decimal digits
            if col.startswith('g_') or col.startswith('NmdaAmpaRatio'):
                _tab[col] = _tab[col].apply(lambda x: round(x, 5) if not np.isnan(x) else np.nan)

        tab = pd.concat([tab, _tab.reset_index()], ignore_index=True)

    for idx, r in tab.iterrows():
        try:
            trace = r['file_object'].read(r['file_key'])
            tab.loc[idx, 'firing rate'] = preprocessing.get_spike_count(*trace, tinit=tinit, tend=tstop, threshold=-30) / ((tstop - tinit) / 1000)
            tab.loc[idx, 'baseline v'] = preprocessing.get_baseline_voltage(*trace, tinit=tinit, tend=tstop)
            tab.loc[idx, 'regularity'] = preprocessing.get_regularity(*trace, tinit=tinit, tend=tstop, threshold=-30)
            tab.loc[idx, 'AP_amplitude'] = preprocessing.get_ap_amplitude(*trace, tinit=tinit, tend=tstop, threshold=-30)  
        except:
            print(r)
            
    return tab

#read_table([('test_firing_rate_0.npy', 'test_firing_rate_mod_only_0.nwb')]).to_csv('test_mod_only.csv')
#read_table([('test_firing_rate_1.npy', 'test_firing_rate_drv_only_0.nwb')]).to_csv('test_drv_only.csv')
#read_table([('test_firing_rate_2.npy', 'test_firing_rate_0.nwb')]).to_csv('test_firing_rate.csv')
#print (read_table([('test_firing_rate.npy', 'test_firing_rate_0.nwb')]).mean())
#pd.concat([read_table([('test_firing_rate_8.npy', 'test_firing_rate_8_0.nwb')]), read_table([('test_firing_rate_6.npy', 'test_firing_rate_6_0.nwb')]), read_table([('test_firing_rate_7.npy', 'test_firing_rate_7_0.nwb')])]).to_csv('test_6.csv')
read_table([('test_firing_rate_3.npy', 'test_firing_rate_6ohda_0.nwb'), ('test_firing_rate_3_bis.npy', 'test_firing_rate_6ohda_3_0.nwb')]).to_csv('test_6ohda.csv')
#read_table([('test_firing_rate_4.npy', 'test_firing_rate_6ohda_2_0.nwb')]).to_csv('test_6ohda_2.csv')

#pd.concat([read_table([('test_firing_rate_9.npy', 'test_firing_rate_9_0.nwb')]), read_table([('test_firing_rate_10.npy', 'test_firing_rate_10_0.nwb')])]).to_csv('test_9.csv')
#read_table([('test_bursting_0_off.npy', 'test_bursting_0_off_0.nwb')], tstop=30000).to_csv('test_bursting_0_off.csv')
#read_table([('test_bursting_0_on.npy', 'test_bursting_0_on_0.nwb')], tstop=30000).to_csv('test_bursting_0_on.csv')
