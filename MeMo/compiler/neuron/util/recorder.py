class Recorder:
  def __init__(self, ref, seg=None, dt=1, density_variable=False):
    from neuron import h, nrn
    import numpy as np
      
    self.y = h.Vector()
    self.t = h.Vector()
    
    self._data = None
    
    if seg:
        self.t.record(h._ref_t, sec=seg.sec)
        self.y.record(ref, sec=seg.sec)
    else:
        self.t.record(h._ref_t)
        self.y.record(ref)

    self.density_variable = density_variable
    self.seg = seg
    self.dt = dt

    # it raise an exception if, with the density variable, there is no area
    assert (density_variable and seg is not None) or not density_variable

  def _get(self):
    import numpy as np
    r = np.array([ [self.t.x[i], self.y.x[i]] for i in range(self.t.size()) ])

    if self._data is not None:
      # it is the second or above interpolation
      # add last point
      r = np.concatenate(([self._data[-1, :]], r), axis=0)
      
    # interpolation
    tp = np.arange(r[0, 0], r[-1, 0], self.dt)
    yp = np.interp(tp, r[:, 0], r[:, 1])
    r = np.array([ tp, yp ]).T

    if self._data is not None:
      # remove the first point
      r = np.delete(r, [0], axis=0)
    
    return r


  def _flush(self):
    import numpy as np

    # interpolate the data and concatenate
    if self._data is None:
      self._data = self._get()
    else:
      self._data = np.concatenate((self._data, self._get()), axis=0)

    # clear vectors
    self.t.resize(0)
    self.y.resize(0)


  def get(self, dt=None):
    import numpy as np

    if dt is None:
      dt = self.dt
      
    try:
      self._flush()
    except ValueError:
      pass

    # get it
    r = self._data
    
    # interpolation
    tp = np.arange(r[0, 0], r[-1, 0], dt)
    yp = np.interp(tp, r[:, 0], r[:, 1])

    # if it is a density variable multiply by area
    if self.density_variable:
      yp = yp * self.seg.area()
      
    r = np.array([ tp, yp ]).T    

    return r
  

    



if __name__ == '__main__':
  c = Recorder(None)
  c.y.append(0.1)
  c.t.append(0.0)
  c.y.append(0.1)
  c.t.append(0.3)
  c.y.append(0.1)
  c.t.append(0.7)
  c._flush()
  print (c._data)
  print ('second round')
  c.y.append(0.9)
  c.t.append(0.9)
  c._flush()
  print (c._data)
  print ('third round')
  c.y.append(0.9)
  c.t.append(1.2)
  c._flush()
  print (c._data)
  print ('fourth round')
  try:
    c._flush()
  except ValueError:
    pass
  print (c._data)
  
    
  print ('fourth round')
  print (c.get(dt=0.2))
