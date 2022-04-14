import matplotlib.pyplot as plt
import sim.nwbio as nwbio


f = nwbio.FileReader('../all_traces_1.nwb')
print (len(f.nwbfile.acquisition))
#t, y = f.read('output-cellid=0-seed=0-tstop=10s-n_drv=17-n_mod=346-n_bg=17-n_rtn=7-g_drv=0.0033-g_mod=0.0018')
#plt.plot(t,y)
#plt.show()
