class CustomClient:
    def __init__(self):
        import os
        import ipyparallel as ipp
        
        # create client & views
        self.dview = ipp.Client(profile=os.getenv('IPYTHON_PROFILE'))
        self.rc = [None] * len(self.dview)
        self._results = {}


    def flush(self):
        """
        Check whether any job is over
        """
        for i in range(len(self.rc)):
            if self.rc[i] and self.rc[i].ready():
                # get simulated data
                # makes available
                self._results.update(self.rc[i].get())

                # mark the client as available
                self.rc[i] = None
                
                
    def running(self):
        """
        Check whether any client is busy
        """
        self.flush()
        
        for _rc in self.rc:
            if _rc is not None:
                return True
        return False


    def any_available(self):
        self.flush()
        return None in self.rc


    def apply(self, func, *args, **kwargs):
        self.flush()
        print (self.rc)
        i = self.rc.index(None)
        self.rc[i] = self.dview[i].apply_async(func, *args, **kwargs)
    

    def results(self):
        self.flush()
        res = list( self._results.items() )
        self._results.clear()
        return res



        
    
        
if __name__ == '__main__':

    def save_results(cc, fw=None, numpy_flag=False, verbose=True):
        import numpy as np
        for key_res, data_res in cc.results():
            if verbose:
                print (key_res, 'done')
            if not numpy_flag:
                fw.add(key_res, data_res[:, 0], data_res[:, 1])
            else:
                np.save(fw + '.' + key_res, data_res, allow_pickle=True)

        
    import os
    import ipyparallel as ipp
    import sys
    
    
    import sim.nwbio as nwbio
    import numpy as np
    import thalamicsim as ts

    import time

    twait = 10.0 # seconds
    
    filenamein = sys.argv[sys.argv.index('--filenamein')+1]
    filenameout = sys.argv[sys.argv.index('--filenameout')+1]
    numpy_output = '--numpyout' in sys.argv
    
    try:
        init_index = int(sys.argv[sys.argv.index('--init_index')+1])
    except:
        init_index = 0
    
    try:
        end_index = int(sys.argv[sys.argv.index('--end_index')+1])
    except:
        end_index = -1
        
    
    params = []
    for c in np.load(filenamein, allow_pickle=True).tolist()[init_index:end_index]:
        c_cpy = dict(c.copy())
        del c_cpy['cellid'], c_cpy['lesioned_flag'], c_cpy['tstop'], c_cpy['seed'], c_cpy['key']
        params.append({'args':(c['cellid'], c['lesioned_flag'], c['tstop'], c['seed'], c['key']),
                       'kwargs':c_cpy})



    # use nwb format
    if not numpy_output:
        fw = nwbio.FileWriter(filenameout, "thalamic_data", "thalamic_data_id", max_size=None)

    # client
    cc = CustomClient()
    
    while len(params) or cc.running():
        #print (len(params), cc.running(), cc.any_available())
        
        # enqueue if any available
        while len(params) and cc.any_available():
            _param = params.pop()
            cc.apply(ts.run_simulation, *_param['args'], **_param['kwargs'])

        # check for results and save
        save_results(cc, numpy_flag=numpy_output, fw=(filenameout if numpy_output else fw))

        # sleep
        time.sleep(twait)


    # save results
    save_results(cc, numpy_flag=numpy_output, fw=(filenameout if numpy_output else fw))


    # close
    if not numpy_output:
        fw.close()

    sys.exit(0)
