import pandas as pd
import numpy as np



def __analyze_key(k):
    params = {}

    # clean first string
    k = k.replace('output-', '')

    # state lesioned vs normal
    params['state'] = '6ohda' if '6ohda' in k else 'normal'

    # clean state
    k = k.replace('-6ohda', '')

    # split in tokens
    tokens = k.split('-')

    # clean the last tokens
    if 'axonal' in tokens[-1]:
        token_type = 'axonal'
        section_token_flag = True
    elif 'basal' in tokens[-1]:
        token_type = 'basal'
        section_token_flag = True
    elif 'somatic' in tokens[-1]:
        token_type = 'somatic'
        section_token_flag = True
    elif 'syn' in tokens[-1]:
        token_type = 'syn'
        section_token_flag = False

    # correct the last token
    tokens[-1], last_part = tokens[-1].split('.' + token_type + '.')
    last_part, variable_part = last_part.split('._ref_')

    # parse parameters
    for tk in tokens:
        # split
        name, val = tk.split('=')

        # ignore tstop
        if name == 'tstop':
            continue

        # convert
        params[name] = (int if name.startswith('n_') else float)(val)


    # get the section
    if section_token_flag:
        # get section number and arc
        section_index_tk, section_arc_tk = last_part.replace(')', '').split('(')

        params['section_name'] = token_type
        params['section_index'] = int(section_index_tk)
        params['section_arc'] = float(section_arc_tk)
    else:
        # get section number and arc
        synapse_name, synapse_index_tk = last_part.replace(']', '').split('[')

        params['synapse_name'] = synapse_name
        params['synapse_index'] = int(synapse_index_tk)   


    # variable type
    if variable_part.startswith('i'):
        params['var_type'] = 'i'
        # it is a ion channel
        if section_token_flag:
            params['channel_name'] = variable_part.replace('i_output_', '')

    elif variable_part.startswith('v'):
        params['var_type'] = 'v'

    return params
    
    
def _analyze_key(f, init_key=0):
    keys = []
    for k in list(f.nwbfile.acquisition.keys()):
        par = __analyze_key(k)
        par.update({'file_object':f, 'key':k})
        keys += [par]
    return pd.DataFrame(data=keys, index=range(init_key, init_key + len(keys)))


def analyze_key(f):
    keys = pd.DataFrame()
    for i in range(len(f)):
        keys = pd.concat([keys, _analyze_key(f[i], keys.shape[0])])
    return keys
