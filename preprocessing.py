import sim.nwbio as nwbio
import numpy as np
import pandas as pd
import efel

def psth(t, v, tinit=2000, tend=10000, n_bin=3, threshold=-20): 
    tspk = get_spike_times(t, v, tinit=tinit, tend=tend, threshold=threshold)
    nh, th = np.histogram(tspk, bins=n_bin, range=(tinit, tend))
    th = th[:-1]
    return th, nh
        
def _psth(tspk, tinit=2000, tend=10000, n_bin=3): 
    nh, th = np.histogram(tspk, bins=n_bin, range=(tinit, tend))
    th = th[:-1]
    return th, nh

def get_spike_times(t, v, tinit=2000, tend=10000, threshold=-20):
    """
    Extract the spike time
    t:time array of the trace
    v:voltage array of the trace
    tinit:(default 2000) lower bound of time
    tend:(default 10000) upper bound of time
    threshold:(default 0) spike threshold
    """
    idx = np.logical_and(t >= tinit, t <= tend)
    t = t[idx]
    v = v[idx]
    idx = np.argwhere(v > threshold)[:, 0]
    idx = np.delete(idx, np.argwhere( (idx[1:] - idx[:-1]) == 1)[:, 0] + 1)
    return t[idx]


def cut_spikes(t, v, tinit=2000, tend=10000, threshold=-20):
    """
    Remove spikes
    t:time array of the trace
    v:voltage array of the trace
    tinit:(default 2000) lower bound of time
    tend:(default 10000) upper bound of time
    threshold:(default 0) spike threshold
    """
    idx = np.logical_and(t >= tinit, t <= tend)
    t = t[idx]
    v = v[idx]
    
    efel.setThreshold(threshold)
    trace = {
        'T':t,
        'V':v,
        'stim_start':[t[0]],
        'stim_end':[t[-1]]
    }
    ef = efel.getFeatureValues([trace], ['AP_begin_indices', 'AP_end_indices'])
    
    del_indices = np.array([])
    a = ef[0]['AP_begin_indices']
    b = ef[0]['AP_end_indices']
    j = min([a.size, b.size])
    a = a[:j]
    b = b[:j]
    #print (a.shape, b.shape)
    for init_index, end_index in np.concatenate(([a], [b])).T:
        del_indices = np.concatenate((del_indices, np.arange(init_index, end_index+1)))
    del_indices = del_indices.astype(int)
    t = np.delete(t, del_indices)
    v = np.delete(v, del_indices)
    tp = np.linspace(tinit, tend, idx.size - 1)
    vp = np.interp(tp, t, v)    

    return tp, vp


def get_regularity(t, v, cv_flag=True, tinit=2000, tend=10000, threshold=-20):
    """
    Extract the spike count
    t:time array of the trace
    v:voltage array of the trace
    tinit:(default 2000) lower bound of time
    tend:(default 10000) upper bound of time
    threshold:(default 0) spike threshold
    """
    tspk = get_spike_times(t, v, tinit=tinit, tend=tend, threshold=threshold)
    ISIs = tspk[1:] - tspk[:-1]
    
    if cv_flag:
        return np.std(ISIs) / np.mean(ISIs)
    else:
        MeanLV = 3 * np.mean(np.power(ISIs[1:] - ISIs[:-1], 2.0) / np.power(ISIs[1:] + ISIs[:-1], 2.0))
        reg = (3 - MeanLV) / (2 * MeanLV)
        if np.isnan(reg):
            reg = 0.
        return reg

def get_ap_amplitude(t, v, tinit=2000, tend=10000, threshold=-20):
    """
    Extract the spike count
    t:time array of the trace
    v:voltage array of the trace
    tinit:(default 2000) lower bound of time
    tend:(default 10000) upper bound of time
    threshold:(default 0) spike threshold
    """
    idx = np.logical_and(t >= tinit, t <= tend)
    t = t[idx]
    v = v[idx]
    trace = {'T':t, 'V':v, 'stim_start':[tinit], 'stim_end':[tend] }
    res = efel.getMeanFeatureValues([trace], ['AP_amplitude'])[0]['AP_amplitude']
    return np.nan if res is None else res

def get_spike_count(t, v, tinit=2000, tend=10000, threshold=-20):
    """
    Extract the spike count
    t:time array of the trace
    v:voltage array of the trace
    tinit:(default 2000) lower bound of time
    tend:(default 10000) upper bound of time
    threshold:(default 0) spike threshold
    """
    return get_spike_times(t, v, tinit=tinit, tend=tend, threshold=threshold).size

def butter_lowpass_filter(data, cutoff, fs, order=5):
    import numpy as np
    from scipy.signal import butter, lfilter, freqz

    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a


    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def low_pass_filter(t, v, cutoff):
    """
    low pass filtering by FFT
    t:time array of the trace (in ms)
    v:voltage array of the trace
    cutoff:cutoff frequency in Hertz
    """
    # sampling frequency, assuming time is measured in ms
    # the internal unit is however seconds and thus Hertz for frequency band
    # time bins are assumed equally spaced
    sample_freq = np.fft.fftfreq(v.size, d=((t[1] - t[0]) / 1000.0))
    
    # fast fourier transform
    sig_fft = np.fft.fft(v)
    
    # clean the frequencies higher than cutoff
    sig_fft[np.abs(sample_freq) > cutoff] = 0.

    # reconvert and return 
    v = np.fft.ifft(sig_fft).astype(float)
                                 
    return t, v


def get_band_density(t, v, tinit=6000, tend=16000, cutoff=200, norm=True, band_range=(13, 30), nperseg=4096):
    from scipy import signal
    
    t, v = low_pass_filter(t, v, cutoff)
    
    idx = np.logical_and(t >= tinit, t < tend)
    t = t[idx]
    v = v[idx]
    
    freq, psd = signal.welch(v, fs=(1000.0/(t[1] - t[0])), nperseg=nperseg)
    
    if norm:
        psd = psd / np.sum(psd)
        
    idx = np.logical_and(freq >= band_range[0], freq <= band_range[1])
    #print(freq)
    freq = freq[idx]
    psd = psd[idx]
    #print(freq)
    
    return np.sum(psd) * (freq[1] - freq[0])


def get_baseline_voltage(t, v, tinit=2000, tend=10000, cutoff=10):
    """
    return the average value of baseline membrane potential
    t:time array of the trace (in ms)
    v:voltage array of the trace
    cutoff: (default 10 Hz) cutoff frequency in Hertz
    """
    idx = np.logical_and(t >= tinit, t <= tend)
    t = t[idx]
    v = v[idx]    
    return np.mean(low_pass_filter(t, v, cutoff)[1])


def elaborate(f, filter_param_name = ['g_mod', 'g_drv', 'cellid', 'seed', 'n_drv', 'n_rtn', 'n_mod', 'n_bg']):
    import sys
    
    keys = list ( f.nwbfile.acquisition.keys() )

    df = pd.DataFrame(columns=filter_param_name + ['AP count', 'baseline', 'state']) # create the dataframe

    oldst = ''

    for i, k in enumerate(keys):
        
        newst = '%.0f%%\n' % (i / len(keys) * 100)
        if newst != oldst:
            oldst = newst
            print ('\n' * 32)
            for kk in range(int(i / len(keys) * 50)):
                sys.stdout.write('█')
            sys.stdout.write(newst)
            sys.stdout.flush()
                                    
        # read the trace
        t, v = f.read(k)

        param = {}

        param['AP count'] = get_spike_count(t, v)
        param['baseline'] = get_baseline_voltage(t, v)
        param['state'] = '6ohda' if '6ohda' in k else 'control'

        for arg in k.split('-'):
            try:
                name, val = arg.split('=')
                val = (int if name.startswith('n_') else float)(val)
            except ValueError:
                continue
            if name in filter_param_name:
                param[name] = val

        # add to the dataframe
        df.loc[df.shape[0], :] = pd.DataFrame(data=param, index=[df.shape[0]]).loc[df.shape[0],:]

        # free memory
        del t, v, param, name, val

    
    return df


if __name__ == '__main__':
    pd.concat([elaborate(nwbio.FileReader('../prova/all_traces_1.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_2.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_3.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_0.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_4.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_5.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_6.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_6_1.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_7.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_7_1.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_8.nwb')),
               elaborate(nwbio.FileReader('../prova/all_traces_8_1.nwb')),], ignore_index=True).to_csv('all_traces.csv')

    
