from bluepyopt.ephys.parameterscalers import ParameterScaler
from bluepyopt.ephys.parameterscalers import DictMixin
from math import exp, log


class NrnSegmentAxonDistanceScaler(ParameterScaler, DictMixin):

    def __init__(self,
                 axon_prox_multiplier,
                 axon_dist_multiplier,
                 somatic_multiplier,
                 dend_1st_order_multiplier,
                 dend_deep_multiplier,
                 name=None, comment=''):
      super(NrnSegmentAxonDistanceScaler, self).__init__(name, comment)

      self.axon_prox_multiplier=axon_prox_multiplier
      self.axon_dist_multiplier=axon_dist_multiplier
      self.somatic_multiplier=somatic_multiplier
      self.dend_1st_order_multiplier=dend_1st_order_multiplier
      self.dend_deep_multiplier=dend_deep_multiplier



    def get_depth(self, sec, sim):
        depth = 1
        sref = sim.neuron.h.SectionRef(sec=sec)
        while sref.has_parent() and \
              ("soma" not in sim.neuron.h.secname(sec=sref.parent)):
            sref = sim.neuron.h.SectionRef(sec=sref.parent)
            depth += 1
        return depth
    
                

    def scale(self, value, segment, sim=None):
        """Scale a value based on a segment"""
        ## if it is not an axon, then it is the same coefficient as proximal
        secname = sim.neuron.h.secname(sec=segment.sec)
        if "axon" in secname:
            multiplier = self.axon_prox_multiplier if segment.x <= 0.5 else self.axon_dist_multiplier
        elif "soma" in secname:
            multiplier = self.somatic_multiplier
        else:
            ## for dendrite we distinguish by order
            sref = sim.neuron.h.SectionRef(sec=segment.sec)
            
            # we assume that no parent is equivalent to soma
            if not sref.has_parent():
                multiplier = self.somatic_multiplier

            # if the parent is soma than it is a first order
            elif "soma" in sim.neuron.h.secname(sec=sref.parent):
                multiplier = self.dend_1st_order_multiplier
            else:
                multiplier = self.dend_deep_multiplier
        
        return multiplier*value


    def __str__(self):
        """String representation"""
        return ""










class NrnSegmentNaDistanceScaler(ParameterScaler, DictMixin):

    def __init__(self,
                 axon_prox_multiplier,
                 axon_dist_multiplier,
                 name=None,
                 comment=''):
      super(NrnSegmentNaDistanceScaler, self).__init__(name, comment)

      self.axon_prox_multiplier=axon_prox_multiplier
      self.axon_dist_multiplier=axon_dist_multiplier


    def get_depth(self, sec, sim):
        depth = 1
        sref = sim.neuron.h.SectionRef(sec=sec)
        while sref.has_parent() and \
              ("soma" not in sim.neuron.h.secname(sec=sref.parent)):
            sref = sim.neuron.h.SectionRef(sec=sref.parent)
            depth += 1
        return depth
    
                

    def scale(self, value, segment, sim=None):
        """Scale a value based on a segment"""
        ## if it is not an axon, then it is the same coefficient as proximal
        secname = sim.neuron.h.secname(sec=segment.sec)
        if "axon" in secname:
            multiplier = self.axon_prox_multiplier if segment.x <= 0.5 else self.axon_dist_multiplier
        elif "soma" in secname:
            multiplier = 1.0
        else:
            order = self.get_depth(segment.sec, sim)
            multiplier = 1.0 / (2**(order-1))

        return multiplier*value


    def __str__(self):
        """String representation"""
        return ""


class NrnSegmentEClDistanceScaler(ParameterScaler, DictMixin):
    def __init__(self,
                 scaler,
                 name=None,
                 comment=''):
      super(NrnSegmentEClDistanceScaler, self).__init__(name, comment)

      self.scaler = 1.0/scaler
      #self.min_ecl = -80.
      #self.max_ecl = -46.
      self.Ce = 133.1
      self.Ci_Phy = 7.0
      self.Ci_Pipette = 22.



    def get_depth(self, sec, sim):
        depth = 1
        sref = sim.neuron.h.SectionRef(sec=sec)
        while sref.has_parent() and \
              ("soma" not in sim.neuron.h.secname(sec=sref.parent)):
            sref = sim.neuron.h.SectionRef(sec=sref.parent)
            depth += 1
        return depth


    def get_distance(self, segment, sim):
        d = segment.x*segment.sec.L

        sref = sim.neuron.h.SectionRef(sec=segment.sec)
        while sref.has_parent() and \
              ("soma" not in sim.neuron.h.secname(sec=sref.parent)):
            sref = sim.neuron.h.SectionRef(sec=sref.parent)
            d += sref.sec.L
            
        return d if d > 0 else 0.0
        
        
    def _nerst_eq(self, T, Ce, Ci):
        T += 273.15
        R = 8.31446261815324
        F = 96485.3321233100184
        z = -1
        return (R*T/F)/z*log(Ce/Ci)*1000.0

    def scale(self, value, segment, sim=None):
        secname = sim.neuron.h.secname(sec=segment.sec)
        if "soma" in secname:
          d  = 0.0
        else:
          d = self.get_distance(segment, sim)
        """Scale a value based on a segment"""
        Ci = (self.Ci_Pipette-self.Ci_Phy)*exp(-(self.scaler*d)**2)+self.Ci_Phy
        return self._nerst_eq(sim.neuron.h.celsius, self.Ce, Ci)
        


    def __str__(self):
        """String representation"""
        return ""
    


class NrnSegmentCaTDistanceScaler(ParameterScaler, DictMixin):
    def __init__(self,
                 name=None,
                 comment=''):
      super(NrnSegmentCaTDistanceScaler, self).__init__(name, comment)





    def get_depth(self, sec, sim):
        depth = 1
        sref = sim.neuron.h.SectionRef(sec=sec)
        while sref.has_parent() and \
              ("soma" not in sim.neuron.h.secname(sec=sref.parent)):
            sref = sim.neuron.h.SectionRef(sec=sref.parent)
            depth += 1
        return depth


    
                

    def scale(self, value, segment, sim=None):
        """Scale a value based on a segment"""
        ## if it is not an axon, then it is the same coefficient as proximal
        secname = sim.neuron.h.secname(sec=segment.sec)
        if "axon" in secname:
            multiplier = 0
        elif "soma" in secname:
            multiplier = 1.
        else:
            order = self.get_depth(segment.sec, sim)
            if order == 1:
                multiplier = 2.
            else:
                multiplier = 0.5
        
        return multiplier*value


    def __str__(self):
        """String representation"""
        return ""









class NrnSegmentCaLDistanceScaler(ParameterScaler, DictMixin):
    def __init__(self,
                 name=None,
                 comment=''):
      super(NrnSegmentCaLDistanceScaler, self).__init__(name, comment)





    def get_depth(self, sec, sim):
        depth = 1
        sref = sim.neuron.h.SectionRef(sec=sec)
        while sref.has_parent() and \
              ("soma" not in sim.neuron.h.secname(sec=sref.parent)):
            sref = sim.neuron.h.SectionRef(sec=sref.parent)
            depth += 1
        return depth


    
                

    def scale(self, value, segment, sim=None):
        """Scale a value based on a segment"""
        ## if it is not an axon, then it is the same coefficient as proximal
        secname = sim.neuron.h.secname(sec=segment.sec)
        if "axon" in secname:
            multiplier = 0.0
        elif "soma" in secname:
            multiplier = 1.0
        else:
            if self.get_depth(segment.sec, sim) == 1 and \
               (segment.sec.L*segment.x) < 10.0:
                multiplier = (1.25/2.5)
            else:
                multiplier = (0.75/2.5)
        return multiplier*value


    def __str__(self):
        """String representation"""
        return ""
