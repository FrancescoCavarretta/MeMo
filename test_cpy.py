import numpy as np
import os
import sim.nwbio as nwbio
import sys


oldst = ''

fr = nwbio.FileReader('../all_traces_0.nwb')


print ('file read')

fw = nwbio.FileWriter('all_traces__my__test.nwb', "thalamic_test", "thalamic_test_id")

ntot = len(fr.nwbfile.acquisition)
print (ntot, 'entries in file')
for n, k in enumerate(fr.nwbfile.acquisition):
    t, v = fr.read(k)
    
    newst = '%.0f%%\n' % (n / ntot * 100)
    
    if newst != oldst:
        oldst = newst
        print ('\n' * 30)
        for kk in range(int(n / ntot * 50)):
            sys.stdout.write('█')
        sys.stdout.write(newst)
        sys.stdout.flush()

    fw.add(k, t, v)                     
fw.close()
fr.close()
