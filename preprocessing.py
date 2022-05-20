import sim.nwbio as nwbio

import numpy as np
import pandas as pd

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



def get_baseline_voltage(t, v, cutoff=10):
    """
    return the average value of baseline membrane potential
    t:time array of the trace (in ms)
    v:voltage array of the trace
    cutoff: (default 10 Hz) cutoff frequency in Hertz
    """
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

    
