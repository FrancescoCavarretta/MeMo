import sim.nwbio as nwbio
import matplotlib.pyplot as plt
import sys

plt.figure(figsize=(15, 7.5))

def _avg_h(filename, varname, sectype):
  v = None
  t = None
  n = None
  f = nwbio.FileReader(filename)
  for k in list(f.nwbfile.acquisition.keys()):
    if k.endswith(varname) and sectype in k:
      _t, _v = f.read(k)
      #plt.plot(_t, _v, label=k, color='gray')

      if t is None:
        t = _t
        v = _v
        n = 1
      else:
        v = v + _v
        n += 1
  v = v / n
  return t, v
    

def avg_h(filenames, varname, sectype):
  v = None
  t = None
  n = None
  for filename in filenames:
    try:
      _t, _v = _avg_h(filename, varname, sectype)
      #plt.plot(_t, _v, label=k, color='gray')

      if t is None:
        t = _t
        v = _v
        n = 1
      else:
        v = v + _v
        n += 1
    except:
      pass
  v = v / n
  return t, v


ax = plt.subplot(1, 2, 1)
ax.plot(*avg_h(['output-5.nwb', 'output-6.nwb', 'output-7.nwb', 'output-8.nwb', 'output-9.nwb',
                'output-10.nwb', 'output-11.nwb', 'output-12.nwb', 'output-13.nwb', 'output-14.nwb',
                'output-15.nwb', 'output-16.nwb', 'output-17.nwb'], '_ref_i_output_TC_iT_Des98', 'basal'), color='blue')
ax2 = ax.twinx()
ax2.plot(*avg_h(['output-5.nwb', 'output-6.nwb', 'output-7.nwb', 'output-8.nwb', 'output-9.nwb',
                'output-10.nwb', 'output-11.nwb', 'output-12.nwb', 'output-13.nwb', 'output-14.nwb',
                'output-15.nwb', 'output-16.nwb', 'output-17.nwb'], '_ref_v', 'soma'), color='darkgray')

##for k in list(f.nwbfile.acquisition.keys()):
##  if k.endswith('_ref_v') and 'soma' in k:
##        ax2.plot(*f.read(k), color='darkgray')
##        break
ax.set_xlim([5000, 16000])
ax.set_ylim([0, -0.001])
ax2.set_ylim([-85, 30])

ax = plt.subplot(1, 2, 2)
ax.plot(*avg_h(['output-0.nwb', 'output-1.nwb', 'output-2.nwb', 'output-3.nwb', 'output-4.nwb'], '_ref_i_output_TC_iT_Des98', 'basal'), color='red')
ax2 = ax.twinx()
ax2.plot(*avg_h(['output-0.nwb', 'output-1.nwb', 'output-2.nwb', 'output-3.nwb', 'output-4.nwb'], '_ref_v', 'soma'), color='darkgray')
ax.set_xlim([5000, 16000])
ax.set_ylim([0, -0.001])
ax2.set_ylim([-85, 30])

plt.legend()

plt.show()
