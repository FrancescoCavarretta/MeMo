from thalamocortical_cell import Cell
import neurom
from neurom import viewer
import pandas as pd
import matplotlib.pyplot as plt
import random


def section_index(x):
  x = x[x.index('.')+1:]
  return int(x[x.index('[')+1:x.index(']')])


def section_type(x):
  x = x[x.index('.')+1:]
  x = x[:x.index('[')]
  return x

  
def section_arc(x):
  return float(x[x.index('(')+1:x.index(')')])


def arc2xyz(m, sectype, index, arc):
    import numpy as np
    sec = m.cell.dend[index]

    points = np.array([[sec.x3d(i), sec.y3d(i), sec.z3d(i), sec.diam3d(i)] for i in range(sec.n3d())])
    
    d = np.cumsum(np.linalg.norm(points[1:, :-1] - points[:-1, :-1], axis=1))
    ds = arc * d[-1]
    index = np.argwhere(ds <= d).T[0, 0]
    if index == 0:
      dmin = 0
    else:
      dmin = d[index-1]
    dmax = d[index]
    
    a = points[index, :-1]
    b = points[index + 1, :-1]
    return (b - a) * (ds - dmin) / (dmax - dmin) + a

  
data = []
for i in [1]:
    with open('distr_%d.txt' % i, 'r') as fi:
        l = fi.readline()
        while l:
            tk = l.split()
            
            data.append([tk[0], tk[1].split('.')[1].split('[')[0], float(tk[2]), float(tk[3]), tk[4], float(tk[5])])
            l = fi.readline()
                        
data = pd.DataFrame(data, columns=['input_name', 'section_name', 'path_distance', 'diameter', 'segment_id', 'area'])
data['section_index'] = data['segment_id'].apply(lambda x : section_index(x))
data['section_type'] = data['segment_id'].apply(lambda x : section_type(x))
data['section_arc'] = data['segment_id'].apply(lambda x : section_arc(x))
c = Cell('Test')
c.make()
m = neurom.load_morphology('test.swc')
fig, ax = viewer.draw(m, mode='3d', color='black')
fig.set_size_inches(20, 20)
ax.set_xlim([-350, 350])
ax.set_ylim([-250, 450])
ax.set_zlim([-275, 425])
ax.set_xlabel('x ($\mu$m)')
ax.set_ylabel('y ($\mu$m)')
ax.set_zlabel('z ($\mu$m)')
ax.set_axis_off()

def plot_synapses(ax, c, data, input_name, sz, color):
  x = []
  y = []
  z = []
  for _, r in data[data.input_name == input_name].iterrows():
    #print(, , r.path_distance)
    _x, _y, _z = arc2xyz(c, r.section_type, r.section_index, r.section_arc)
    x.append(_x)
    y.append(_y)
    z.append(_z)
  ax.scatter(x, y, z, color=color, s=sz)



#plot_synapses(ax, c, data, 'driver', 8, 'red')
#plot_synapses(ax, c, data, 'modulator', 4, 'magenta')
#plt.show()

plot_synapses(ax, c, data, 'nigral', 8, 'blue')
plot_synapses(ax, c, data, 'reticular', 5, 'cyan')
plt.show() 
