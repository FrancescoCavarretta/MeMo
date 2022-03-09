class Recorder:
  def __init__(self, seg):
    from neuron import h
      
    self.y = h.Vector()
    self.t = h.Vector()
    
    seg.sec.push()
    exec("h.CVode().record(seg._ref_v, self.y, self.t)", globals(), locals()) 
    h.pop_section()
    self.interp_flag = True

  def get(self, dt=0.1):
    import numpy as np
    r = np.array([ [self.t.x[i], self.y.x[i]] for i in range(self.t.size()) ])
    
    if self.interp_flag:
      tp = np.arange(0., r[-1, 0], dt)
      yp = np.interp(tp, r[:, 0], r[:, 1])
      r = np.array([ tp, yp ]).T
    return r
