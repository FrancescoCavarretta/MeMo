import sim.nwbio as nwbio
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pandas as pd
import numpy as np
import time
import datetime

def open_nwb_file(filename):
    """
    Open an NWB file and profile the operation.
    """
    print ("time", datetime.datetime.now())
    t = time.time()
    ff = nwbio.FileReader(filename)
    t = time.time() - t
    print (t)
    return ff

def open_model_param_file(filename):
    """
    Model collections
    """
    return sorted(list(np.load(filename, allow_pickle=True).tolist().items()))

def print_model_parameters(cellid, lesioned_flag, verbose=True):
    """
    Print the parameters of a given model indicated in cellid and whether is lesioned/depleted
    """
    import mkcell
    
    model_params = model_params_6ohda if lesioned_flag else model_params_control
    params = pd.DataFrame(data=mkcell.param_dict(np.array(model_params[cellid][1][0]).astype(float)), index=[0])
    
    if verbose:
        print(params)
            
    return params



def process_key(nwb_key):
    """
    Extract the information about a simulation from the key in the NWB file.
    nwb_key: identifier of the trace
    """
    def _process_section(token):
        """
        Extract information on the section
        """
        for sec_type in ["somatic", "axonal", "basal"]:
            if sec_type in token:

                # second part of the token
                _sec_index, _arc = token.split("." + sec_type + ".")[-1].replace(")", "").split("(")

                # convert to numeric
                sec_index = int(_sec_index)
                arc = float(_arc)
                return sec_type, sec_index, arc

            
    def _process_config_info(token):
        """
        Extract configuration info
        token: left key
        """
        for tk in ["somatic", "axonal", "basal", "syn"]:
            if tk in token:
                token = token[:token.index("." + tk)].replace('output-', '')

                # check whether lesioned
                lesioned_flag = '-6ohda' in token

                # remove
                token = token.replace("-6ohda", "")

                # get cell id and seed tokens
                token = token.split('-')

                # configuration info tokens
                config = {}
                for x in tuple(token[2:]):
                    name, value = x.split('=')
                    value = value.replace("s", "")
                    config[name] = (int if name.startswith('n_') else float)(value)
                    
                # cell id
                cellid = int(token[0].split('=')[-1])

                # seed
                seed = int(token[1].split('=')[-1])
                
                return cellid, seed, config, lesioned_flag

            
    
    # recorded variable identifier and reference
    obj_identifier, variable_name = nwb_key.split("._ref_")
    
    if variable_name.endswith("i") and "syn" in obj_identifier:
        # it is a synapse
        # configuration and synapse identifier extraction
        config_key, syn_identifier = obj_identifier.split(".syn.")
        
        # read the synapse type (reticular, nigral, ...)
        syn_type, _syn_index = syn_identifier.replace("]", "").split("[")
        
        # synapse number
        syn_index = int(_syn_index)
        
        # pack into info
        entry_info = { 'synapse_type':syn_type, 'synapse_index':syn_index } 
        
        # trace type
        trace_type = 'syn'        
    elif variable_name.endswith("v"):
        # it is a membrane potential
        
        # segment info
        sec_type, sec_index, arc = _process_section(obj_identifier)
        
        # entry info
        entry_info = { 'section_type':sec_type, 'section_index':sec_index, 'section_arc':arc}  
        
        # trace type
        trace_type = 'v'
    elif "i_output_" in variable_name:
        # it is a ion channel
        
        # the ion channel name is the suffix
        ion_channel_name = variable_name.replace("i_output_", "")
        
        # segment info
        sec_type, sec_index, arc = _process_section(obj_identifier)
        
        # entry info
        entry_info = { 'section_type':sec_type, 'section_index':sec_index, 'section_arc':arc, 
                      'channel_type':ion_channel_name }
        
        # trace type
        trace_type = 'i'
    else:
        # unknown
        print(f"{nwb_key} is unknown")
        return None
    
    # configuration info processing
    cellid, seed, config, lesioned_flag = _process_config_info(obj_identifier)
    
    # return
    ret = { 'trace_type':trace_type, 'cell id':cellid, 
            'seed':seed, 'state':lesioned_flag }
    ret.update(config)
    ret.update(entry_info)
    return ret



def organize_keys(*args):
    from IPython.display import clear_output
    
    def _organize_keys(f):
        """
        Organizes the keys from one file
        """
        table = pd.DataFrame()

        keys = list(f.nwbfile.acquisition.keys())

        old_perc = 0.

        # process all the keys
        for i, nwb_key in enumerate(keys):
            perc = int(i / len(keys) * 100)

            # process
            row = process_key(nwb_key)

            # add key
            row["nwb_key"] = nwb_key

            # add ref to file object
            row["file_object"] = f

            # add row
            table = table.append(row, ignore_index=True)

            # print some output
            if old_perc < perc:
                clear_output(wait=True)
                old_perc = perc
                print(perc, "%")

        return table


    table = pd.DataFrame()

    for f in args:
        table = pd.concat([table, _organize_keys(f)])
        
    return table

def get_average_y(f, nwb_key, tinit=2000.0):
    """
    average value of a y from a trace
    """
    t, y = f.read(nwb_key)
    dt = t[1] - t[0]
    y = y[t >= tinit]
    t = t[t >= tinit]
    return np.sum(y * dt) / (t[-1] - t[0])

def elaborate(key_table):
    from IPython.display import clear_output
    
    """
    Elaboration of dataset, estimating average
    """
    key_table = key_table.copy()
    key_table['y'] = np.nan
    
    old_perc = 0.   
    i = 0
    for key, row in key_table.iterrows():
        key_table.loc[key, 'y'] = get_average_y(row['file_object'], row['nwb_key']) 
        i += 1
        perc = int(i / key_table.shape[0] * 100)
            
        # print some output
        if old_perc < perc:
            clear_output(wait=True)
            old_perc = perc
            print(perc, "%")
    return key_table

def nwb_to_csv(filenamein, filenameout):
    f = open_nwb_file(filenamein)
    df = elaborate(organize_keys(f)).to_csv(filenameout)
    f.close()
    return df

from multiprocessing import Pool
def f(i):
    nwb_to_csv('../Downloads/all_recordings_%d.nwb' % i, 'all_recordings_%d.csv' % i)

with Pool(2) as p:
    p.map(f, [5])

print ('done')

def f(i):
    nwb_to_csv('../Downloads/all_recordings_%d.nwb' % i, 'all_recordings_%d.csv' % (i+9))

with Pool(2) as p:
    p.map(f, [0,1,2,3])

print ('done')
