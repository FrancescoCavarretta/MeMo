##from thalamicsim import *
##        
##params = { 'bg':{"Regularity":1.0, "MeanRate":60.0, "n":17,  "g":0.0015},
##           'rtn':{"Regularity":1.0, "MeanRate":20.0, "n":7,   "g":0.0008},
##           'drv':{"Regularity":1.0, "MeanRate":30.0, "n":41,  "g":0.0033, 'AmpaNmdaRatio':0.6 },
##           'mod':{"Regularity":1.0, "MeanRate":15.0, "n":346, "g":0.0018, 'AmpaNmdaRatio':1.91} }
##
##vmcircuit, i2t = mk_vm_microcircuit(0, True, tstop=50.0, bg_param=params['bg'], rtn_param=params['rtn'], drv_param=params['drv'], mod_param=params['mod'])
##
##print ('model created')
##r = precompiler.precompile(vmcircuit, (0, 0))
##print ('model pre-compiled')
##compiler.compile(r, base)
##print ('model compiled')
##
##rr = run(vmcircuit, i2t, 50.0, (0, 0), 'output', v_init=-78.0, all_section_recording=False, all_synapse_recording=True, rec_invl=100.0, varname=["_ref_v"])
##
##print ('mysim done', rr)

from sim.nwbio import FileReader

fr = FileReader('../prova/all_traces_8_1.nwb')

k = list(fr.nwbfile.acquisition.keys())[0]

import matplotlib.pyplot as plt
plt.plot(*fr.read(k))
plt.show()
