import numpy as np
import os
import sim.nwbio as nwbio
import sys


class Parameters:
    def __init__(self, models, filename, fmt='output-test-%d', lesioned_flags=[True,False]):
        self.params = []
        self.models = models
        self.filename = filename
        self.fmt = fmt
        self.lesioned_flags = lesioned_flags


    def close(self):
        np.save(self.filename, self.params, allow_pickle=True)

        
    def add(self, tstop=20000, ntrial=5, seed_start=0, **kwargs):
        
        for lesioned_flag in self.lesioned_flags:
            
            if lesioned_flag:
                cellids = [i for i in range(len([ k for k in sorted(self.models.keys()) if k[0] == 'lesioned' ]))]
            else:
                cellids = [i for i in range(len([ k for k in sorted(self.models.keys()) if k[0] == 'control'  ]))]
                

            for cellid in cellids:
                for seed in range(ntrial):
                    key = self.fmt % len(self.params)
                    self.params.append({})
                            
                    self.params[-1].update(kwargs)
                    self.params[-1].update({'cellid':cellid, 'seed':(seed_start+seed), 'lesioned_flag':lesioned_flag, 'tstop':tstop, 'key':key})
