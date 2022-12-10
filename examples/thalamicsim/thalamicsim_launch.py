

##class CustomClient:
##    def __init__(self, filename, max_size=None, max_process=None):
##        import os
##        import ipyparallel as ipp
##        import sim.nwbio as nwbio
##            
##        # create client & views
##        self.dview = ipp.Client(profile=os.getenv('IPYTHON_PROFILE'))
##        self.rc = [None] * len(self.dview)
##        self._results = {}
##
##        # create/open new file for output
##        self.filename = filename
##        self.max_size = max_size
##        self.file_index = 0
##        self.fw = nwbio.FileWriter(self.filename  + ("_%d" % self.file_index) + ".nwb", "thalamic_data", "thalamic_data_id", max_size=None)
##        self.max_process = max_process
##        
##
##
##    def __fw_add(self, key_res, x_res, y_res):
##        """
##        add records, create new file if needed
##        """
##
##        # run if the file size cross the threshold
##        if self.max_size is not None and len(self.fw.nwbfile.acquisition) >= self.max_size:
##            import sim.nwbio as nwbio
##            self.fw.close()
##            self.file_index += 1
##            self.fw = nwbio.FileWriter(self.filename  + ("_%d" % self.file_index) + ".nwb", "thalamic_data", "thalamic_data_id", max_size=None)
##
##        # add record
##        self.fw.add(key_res, x_res, y_res)
##
##
##    def flush(self):
##        """
##        Check whether any job is over
##        """
##        for i in range(len(self.rc)):
##            if self.rc[i] and self.rc[i].ready():
##                # get simulated data
##                # makes available
##                out = self.rc[i].get()
##                
##                if out:
##                    # merge
##                    import sim.nwbio as nwbio
##                    import os
##                    fr = nwbio.FileReader(out)
##                    for key_res in fr.nwbfile.acquisition.keys():
##                        self.__fw_add(key_res, *fr.read(key_res))
##                    fr.close()
##                    # remove file
##                    os.system('rm ' + out)
##                    
####                    for key_res, data_res in out.items():
######                        print (data_res[:, 0])
######                        print (data_res[:, 1])
####                        self.__fw_add(str(key_res), data_res[:, 0].astype(float), data_res[:, 1].astype(float))
##                        
##                    # if the file was defined store data
##                    #if self.fw:
##                    #    for key_res, data_res in out.items():
##                    #        fw.add(key_res, data_res[:, 0], data_res[:, 1])
##                    #else:
##                    #    self._results.update(out)
##
##                # mark the client as available
##                self.rc[i] = None
##                
##                
##    def running(self):
##        """
##        Check whether any client is busy
##        """
##        self.flush()
##        
##        for _rc in self.rc:
##            if _rc is not None:
##                return True
##        return False
##
##
##    def any_available(self):
##        self.flush()
##
##        cnt = 0
##        for x in self.rc:
##            if x is None:
##                cnt += 1
##
##        if self.max_process is None:
##            return cnt > 0
##        else:
##            return (len(self.rc) - cnt) < self.max_process
##
##
##    def apply(self, func, *args, **kwargs):
##        self.flush()
##        #print (self.rc)
##        i = self.rc.index(None)
##        self.rc[i] = self.dview[i].apply_async(func, *args, **kwargs)
##    
##
##    def results(self):
##        self.flush()
##        res = list( self._results.items() )
##        self._results.clear()
##        return res
##
##
##
##    def close(self):
##        self.flush()
##        self.fw.close()


def to_command_line(cellid, lesioned_flag, tstop, seed, key,
                    all_section_recording, all_synapse_recording, all_current_recording, total_current_recording, **kwargs):
    s = '--cellid %d' % cellid

    if lesioned_flag:
        s +=  ' --6ohda'
        
    s +=  ' --tstop %f' % tstop
    s +=  ' --seed %d' % seed   
    s +=  ' --key %s' % key

    if all_section_recording:
        s += ' --all_section_recording'

    if all_synapse_recording:
        s += ' --all_synapse_recording'

    if total_current_recording:
        s += ' --total_current_recording'
        
    if all_current_recording:
        s += ' --all_current_recording'
        
    for k, v in kwargs.items():
        s += ' --' + k + '=' + str(v)

    return s
        
        
if __name__ == '__main__':


    #def save_results(cc, fw, verbose=True):
    #    import numpy as np
    #    for key_res, data_res in cc.results():
    #        if verbose:
    #            print (key_res, 'done')
    #        np.save(fw + '.' + key_res, data_res, allow_pickle=True)

        
    import os
    #import ipyparallel as ipp
    import sys
    
    
    import sim.nwbio as nwbio
    import numpy as np
    from multiprocessing import Pool
    #import thalamicsim as ts

    import time


    def simstub(cmd, key):
        if '--no-sim' not in sys.argv:
          os.system(cmd)
        return key + '.nwb'

    
    twait = 1.0 # seconds

    
    filenamein = sys.argv[sys.argv.index('--filenamein')+1]
    if '--no-output' not in sys.argv:
      filenameout = sys.argv[sys.argv.index('--filenameout')+1]
    
    try:
        file_max_size = int(sys.argv[sys.argv.index('--filemaxsize')+1])
    except:
        file_max_size =  64 * 200
        
    #numpy_output = '--numpyout' in sys.argv
    


    all_section_recording = '--all_section_recording' in sys.argv
    all_synapse_recording = '--all_synapse_recording' in sys.argv
    all_current_recording = '--all_current_recording' in sys.argv
    total_current_recording =  = '--total_current_recording' in sys.argv
    
    if '--dt' in sys.argv:
        dt = float(sys.argv[sys.argv.index('--dt')+1])
    else:
        dt = 0.1
    
    try:
        init_index = int(sys.argv[sys.argv.index('--init_index')+1])
    except:
        init_index = 0
    
    try:
        end_index = int(sys.argv[sys.argv.index('--end_index')+1])
    except:
        end_index = None
        
    try:
        max_process = int(sys.argv[sys.argv.index('--max_process')+1])
    except:
        max_process = None      
    cfgs = np.load(filenamein, allow_pickle=True).tolist()
    params = []
    for c in cfgs[init_index:end_index]:
        c_cpy = dict(c.copy())
        del c_cpy['cellid'], c_cpy['lesioned_flag'], c_cpy['tstop'], c_cpy['seed'], c_cpy['key']
        params.append({'args':(c['cellid'], c['lesioned_flag'], c['tstop'], c['seed'], c['key']),
                       'kwargs':c_cpy})



    print ('n', len(params))

    # use nwb format
    #if not numpy_output:
    #fw = nwbio.FileWriter(, "thalamic_data", "thalamic_data_id", max_size=None)
    #else:
    #    fw = None

    # client
##    cc = CustomClient(filenameout, max_size=file_max_size, max_process=max_process)
    
####    if all_current_recording:
######                current_recording = [
######                    '_ref_i_output_BK', '_ref_output_BK',
######                    '_ref_i_output_iM', '_ref_output_iM',
######                    '_ref_i_output_TC_iT_Des98', '_ref_output_TC_iT_Des98',
######                    '_ref_i_output_TC_iL', '_ref_output_TC_iL',
######                    '_ref_i_output_TC_ih_Bud97', '_ref_output_TC_ih_Bud97',
######                    '_ref_i_output_TC_iD', '_ref_output_TC_iD',
######                    '_ref_i_output_TC_iA', '_ref_output_TC_iA',
######                    '_ref_i_output_SK_E2', '_ref_output_SK_E2',
######                    '_ref_i_output_nat_TC_HH', '_ref_output_nat_TC_HH',
######                    '_ref_i_output_nap_TC_HH', '_ref_output_nap_TC_HH',
######                    '_ref_i_output_k_TC_HH', '_ref_output_k_TC_HH'
######                    ]
####        current_recording = [
####            '_ref_i_output_BK', 
####            '_ref_i_output_iM', 
####            '_ref_i_output_TC_iT_Des98', 
####            '_ref_i_output_TC_iL', 
####            '_ref_i_output_TC_ih_Bud97', 
####            '_ref_i_output_TC_iD', 
####            '_ref_i_output_TC_iA', 
####            '_ref_i_output_SK_E2', 
####            '_ref_i_output_nat_TC_HH', 
####            '_ref_i_output_nap_TC_HH', 
####            '_ref_i_output_k_TC_HH', 
####            ]                
####    else:
####        current_recording = []

    #while len(params) or cc.running():
        #print (len(params), cc.running(), cc.any_available())
        
        # enqueue if any available
        #while len(params) and cc.any_available():
   #         _param = params.pop()
            
            #print ('applying', _param, to_command_line(*_param['args'], all_section_recording, all_synapse_recording, all_current_recording, **_param['kwargs']))
    with Pool() as pool:
        res = pool.starmap(simstub, [('./x86_64/special thalamicsim.py ' + to_command_line(*_param['args'], all_section_recording, all_synapse_recording, all_current_recording, total_current_recording, **_param['kwargs']), _param['args'][4]) \
                               for _param in params ])
            #print ('\t', './x86_64/special thalamicsim.py ' + to_command_line(*_param['args'], all_section_recording, all_synapse_recording, all_current_recording, **_param['kwargs']))


    if '--no-output' not in sys.argv:
        file_index = 0
        fw = nwbio.FileWriter(filenameout  + ("_%d" % file_index) + ".nwb", str(cfgs), "thalamic_data_id", max_size=None)
        filenames_to_del = []
        
        for out in res:
            if fw is not None and fw.nwbfile is not None and len(fw.nwbfile.acquisition) >= file_max_size:
                fw.close()
                file_index += 1
                fw = nwbio.FileWriter(filenameout  + ("_%d" % file_index) + ".nwb", str(cfgs), "thalamic_data_id", max_size=None)

            filenames_to_del.append(out)
            
            try:
                fr = nwbio.FileReader(out)
                for key_res in fr.nwbfile.acquisition.keys():
                    fw.add(key_res, *fr.read(key_res))
                fr.close()
            except: 
                print('warning', out)
                
        fw.close()
        for out in filenames_to_del:
#            pass
            os.system('rm ' + out)
                    

        
        # check for results and save
        #if numpy_output:
        #    save_results(cc, filenameout)

        # sleep
        #time.sleep(twait)

    #cc.flush() # last

    # save results
    #if numpy_output:
    #    save_results(cc, filenameout)



    # close
    #if not numpy_output:
    #    fw.close()
    #fw.close()

    # delete client manager
    # cc.close()
    
    sys.exit(0)

