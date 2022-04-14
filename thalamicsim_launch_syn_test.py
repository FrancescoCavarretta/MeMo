if __name__ == '__main__':
    import os
    import ipyparallel as ipp
    import sys
    
    
    import sim.nwbio as nwbio
    import numpy as np

    filenamein = sys.argv[sys.argv.index('--filenamein')+1]
    filenameout = sys.argv[sys.argv.index('--filenameout')+1]
    numpy_output = '--numpyout' in sys.argv
    
    cfg = np.load(filenamein, allow_pickle=True).tolist()[:2]
    
    
    params = []
    for c in cfg:
        c_cpy = dict(c.copy())
        del c_cpy['cellid'], c_cpy['lesioned_flag'], c_cpy['tstop'], c_cpy['seed'], c_cpy['key']
        params.append((c['cellid'], c['lesioned_flag'], c['tstop'], c['seed'], c['key'], c_cpy))


    def parallel_simulation_function(i, params=params):
        import thalamicsim as ts
        return ts.run_simulation(*params[i])

    if not numpy_output:
        fw = nwbio.FileWriter(filenameout, "thalamic_data", "thalamic_data_id", max_size=None)
    
    # create client & views
    rc = ipp.Client(profile=os.getenv('IPYTHON_PROFILE'))
    dv = rc[:]
    v = rc.load_balanced_view()
    amr = v.map(parallel_simulation_function, range(len(params)))
    
    print (len(params), 'configurations')
    for r in amr.result():
        key, t, y = r
        if not numpy_output:
            fw.add(key, t, y)
        else:
            np.save(filenameout + '.' + key, [t, y], allow_pickle=True)
        print (key, 'done')
        

    rc.wait()
    if not numpy_output:
        fw.close()
