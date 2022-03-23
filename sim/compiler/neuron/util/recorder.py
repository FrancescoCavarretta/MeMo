class Recorder:
  def __init__(self, ref, seg=None):
    from neuron import h, nrn
      
    self.y = h.Vector()
    self.t = h.Vector()
    
    is_seg = seg and isinstance(seg, nrn.Segment)
    
    if is_seg:
        seg.sec.push()
        
    h.CVode().record(ref, self.y, self.t)
    
    if is_seg:
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
