import sim.nwbio as nwbio
import matplotlib.pyplot as plt
import sys

f = nwbio.FileReader(sys.argv[-1])
k = list(f.nwbfile.acquisition.keys())[0]
plt.plot(*f.read(k))
plt.show()
