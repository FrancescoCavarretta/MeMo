#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from . import modules


class SpikeTrain:
    time_conversion = {
        "tenth_ms":1e-4,
        "ms":1e-3,
        "s":1.0,
        "m":60,
        "h":3600.0
        }
    
    def abbasi(self, distribution, time, rate, refractory_period, tstop):
        
        conversion_factor = SpikeTrain.time_conversion[self.time_unit]
        tstop *= conversion_factor
        refractory_period *= conversion_factor
        time *= conversion_factor
        
        UnGamma   =self.UnGamma
        Precision =self.Precision
        
        #max_frequency=None
        #min_frequency=None
        
        import numpy as np
        
        """ let's test the consistency of the configuration """
        #if max_frequency is None:
        max_frequency = 1.0/refractory_period
        
        #if min_frequency is None:
        min_frequency = 1e-5
          
        #assert min_frequency < max_frequency
        #assert max_frequency <= 1.0/refractory_period
          
        # calculate time bin sizeself._gen_spike_train(*self._args)
        TimeBinSz = time[1] - time[0]
          
          
        """ check validity of the numbstg.get()er and convert """
        def RateToISI(FRate):
            if FRate > max_frequency:
                FRate = max_frequency
            elif FRate < min_frequency:
                FRate = min_frequency
      
            try:
                return 1.0/FRate
            except:
                return 1.0/max_frequency
    
        
        # Pull spike times from Gamma distribution to generate AST
        # Params for Gamma: rate from rate template (and k from Lv distribution = reg)
        ISIs = []
        I = 0
        while I < len(time):
            # gamrnd = matlab fn for random arrays from gamma distribution. 
            # Given arguments get a mean firing rate of 1
            X = distribution() #np.random.gamma(Reg, scale=1.0/Reg)
            
            
            J = I
            for z in range(Precision):
                MeanRate = np.mean(rate[I:(J+1)]) # calculate mean rate over expected mean interval
                CurrentISI = X*RateToISI(MeanRate)  
                J = min([ len(rate)-1, I+int(round(CurrentISI/TimeBinSz)) ])  # calculate the interval boundary
    
              
            
            if UnGamma:
                # for cases where templates have sudden large
                # increases in rate, which leads to very slow catchup performance wiht
                # default algorithm.  If algorithmflag==2 then the current interval is
                # examied for rate changes of factor > ungam, and if one is found, the
                # maximal rate for the original interval is determined.  Then the
                # original interval is shortened to the time where the rate exceeds
                # ungam, and a 2nd interval for the new max rate is added.
                MaxRate = np.max(rate[I:(J+1)])
                if MaxRate > UnGamma*rate[I]:
                    CurrentISI = X*RateToISI(MaxRate)
            
            
            ISIs.append(CurrentISI)
            I += int(round(CurrentISI/TimeBinSz))
        
        
        # spike times
        SpikeTimes = np.cumsum(ISIs)
        SpikeTimes = SpikeTimes[SpikeTimes <= tstop]
        
        SpikeTimes /= conversion_factor
        
        return SpikeTimes

    
    def poissonian(self, distribution, refractory_period, tstop):
        conversion_factor = SpikeTrain.time_conversion[self.time_unit]
        tstop *= conversion_factor
        refractory_period *= conversion_factor
        
        import numpy as np
            
        SpikeTimes = np.array([0.])
        
        while SpikeTimes[-1] < tstop:
            while True:
                try:
                    CurrentISI = 1.0 / distribution()
                    while CurrentISI < refractory_period:
                        CurrentISI = 1.0 / distribution()
                    break
                except ZeroDivisionError:
                    continue
                
            SpikeTimes = np.concatenate((SpikeTimes, [SpikeTimes[-1] + CurrentISI]))
        
        SpikeTimes /= conversion_factor
        
        return SpikeTimes
    
    
    
    def __init__(self, name):
        self.name = name
        self.product = None
        
        self.time_unit = "s"
        
        if self.name == "abbasi":
            self.UnGamma = None
            self.Precision = 10
            
        self.generation_function = getattr(self, name)
        for x in self.generation_function.__code__.co_varnames[1:self.generation_function.__code__.co_argcount]:
            setattr(self, x, None)

        
            
            
    def make(self):
        if self.product is None:
            self.distribution.make()
            self.product = self.generation_function(*[getattr(self, x) for x in self.generation_function.__code__.co_varnames[1:self.generation_function.__code__.co_argcount]])
        return self.product
        
        
        

class RNG:
    __distribution__ = {
        "uniform":("neuron", "uniform","a", "b"),
        "discunif":("neuron", "discunif","a", "b"),
        "normal":("neuron", "normal","mean", "var"),
        "poisson":("neuron", "poisson","mean"),
        "gamma":("numpy", "gamma", "k", "theta"),
        "empirical":("neuron","uniform","a","b")
        }
    
    
    def neuron(self):
        import neuron as nrn    
        rng = nrn.h.Random()
        rng.Random123(*self.seed)
        return rng
    
    def numpy(self):
        import numpy as np
        return np.random.Generator(np.random.Philox(*self.seed))
        
    
    def __init__(self, seed, name, **kwargs):
        self.seed = seed
        self.name = name
        self.params = kwargs
        self._params = RNG.__distribution__[name]
        self._rng = {
            "numpy":getattr(self, "numpy")(),
            "neuron":getattr(self, "neuron")()
            }
        
    
    def __call__(self, interval=False, **kwargs):
        
        # if some parameter differs from the default, it is passed as an optional argument
        param_src = self.params
        param_src["name"] = self.name
        param_src.update(kwargs)
        #print (param_src)
        
        rng_name = RNG.__distribution__[param_src["name"]][0]
        distr_name = RNG.__distribution__[param_src["name"]][1]
        param_names = RNG.__distribution__[param_src["name"]][2:]
        
        _rng = self._rng[rng_name]
        
        if param_src["name"] == "empirical":
            import numpy as np
            
            i = np.where(_rng.uniform(0, 1) <= param_src["cdf"])[0][0] # bin index

            if param_src["x"][i] == "somatic":
                return param_src["x"][i]
            else:
                if interval:
                    try:
                        dx = (param_src["x"][i+1] - param_src["x"][i]) / 2
                    except TypeError:
                        dx = (param_src["x"][i] - param_src["x"][i-1]) / 2
                    return param_src["x"][i] - dx, param_src["x"][i] + dx # return an interval corresponding to the bin
                else:
                    return param_src["x"][i] # single value
        X = getattr(_rng, distr_name)(*[ param_src[pname] for pname in param_names ])
        #print ("X:", X, distr_name, [ param_src[pname] for pname in param_names ])
        return X
        

class Distribution:
    __distribution__ = {
        "uniform":("a", "b"),
        "discunif":("a", "b"),
        "normal":("mean", "var"),
        "poisson":("mean"),
        "gamma":("k", "theta"),
        "empirical":("x", "cdf")
        }
    
           
    
    def __init__(self, seed, name):
        self.name = name
        self.product = None
        self.seed = seed
        self.params = Distribution.__distribution__[name]
        
        
    def make(self):
        if self.product is None:
            self.product = RNG(self.seed, self.name, **{ pname:getattr(self, pname)  for pname in self.params }) 
        return self.product
        
    
    def __call__(self, interval=False, **kwargs):
        return self.product(interval=interval, **kwargs)

    
class SimObject:
    def __init__(self, seed, name):
        self.name = name
        self.product = None
        self.make()
        
        
    def make(self):
        if self.product is None:
            self.product = []
            for x in p.__dict__.values():

                if type(x) == list:
                    tmp = []
                    for _x in x:
                        if isinstance(_x, type):
                            tmp.append(_x.make())
                    if len(tmp) == 0:
                        continue
                elif isinstance(x, type):
                    tmp = x.make()
                else:
                    continue

                self.product.append(tmp)
                
            if len(self.product) == 1:
                self.product = self.product[0]
        return self.product
        
    
    def __call__(self):
        return getattr(self.product, self.name)(*[getattr(self, pname) for pname in self.params[1:]])
    
    
class Synapse:
    def __init__(self, name):
        self.name = name
        self.product = None
        self.make()
        
    @property
    def tau(self):
        if self.name == "AmpaNmda":
            return getattr(self, self.name).ampatau
        else:
            return getattr(self, self.name).tau
    
    @tau.setter
    def tau(self, value):
        if self.name == "AmpaNmda":
            getattr(self, self.name).ampatau = value
        else:
            getattr(self, self.name).tau = value

    @property
    def tau1(self):
        return getattr(self, self.name).tau1
    
    @tau1.setter
    def tau1(self, value):
        getattr(self, self.name).tau1 = value

    @property
    def tau2(self):
        return getattr(self, self.name).tau2
    
    @tau2.setter
    def tau2(self, value):
        getattr(self, self.name).tau2 = value
        
    @property
    def erev(self):
        return getattr(self, self.name).e
    
    @erev.setter
    def erev(self, value):
        getattr(self, self.name).e = value
        
    @property
    def gsyn(self):
        return getattr(self, self.name).g_max
    
    @gsyn.setter
    def gsyn(self, value):
        getattr(self, self.name).g_max = value

    @property
    def gsyn_nmda(self):
        return getattr(self, self.name).gnmda_max
    
    @gsyn_nmda.setter
    def gsyn_nmda(self, value):
        getattr(self, self.name).gnmda_max = value

    @property
    def gsyn_ampa(self):
        return getattr(self, self.name).gampa_max
    
    @gsyn_ampa.setter
    def gsyn_ampa(self, value):
        getattr(self, self.name).gampa_max = value
    
    def make(self):
        if self.product is None:
            from neuron import h
            self.Section = h.Section()
            setattr(self, self.name, getattr(h, "MeMo_" + self.name)())

            getattr(self, self.name).loc(0.5, sec=self.Section)

            self.product = getattr(self, self.name) 
        return self.product
                


class Population:
    def __init__(self, name):
        self.name = name
        self.product = None
    
    def __getattr__(self, name):
        if not self.__dict__:
            setattr(self, name, None)
        return super().__getattr__(self, name)
    
    def make(self):
        if self.product is None:
            self.product = []
            for x in self.__dict__.values():
                if type(x) == list:
                    for obj in x:
                        obj.make()
                        self.product.append(obj)
        return self.product
    
    

class SynapseGroup(Population):
    def __init__(self, name):
        Population.__init__(self, name)
        
        
class SpikeTrainPopulation(Population):
    def __init__(self, name):
        Population.__init__(self, name)
        
        
class SpikeTrainToSynapse:
    def __init__(self):
        self.input = None
        self.output = None
        self.product = None
        
        
    def make(self):
        if self.product is None:
            from neuron import h
            
            self.input.make()
            self.output.make()
            
            self.Vector = h.Vector(self.input.product)
            self.VecStim = h.MeMo_VecStim()
            self.VecStim.play(self.Vector)
            self.NetCon = h.NetCon(self.VecStim, self.output.product)
            self.product = { "Vector":self.Vector, "VecStim":self.VecStim, "NetCon":self.NetCon }
        return self.product     
    
    
        
class SpikeTrainPopulationToSynapseGroup:
    def __init__(self):
        self.input = None
        self.output = None
        self.product = None
        
    def make(self):
        if self.product is None:
            from neuron import h
            
            self.input.make()
            self.output.make()
            
            self.product = []
            n = min([len(self.input.product), len(self.output.product)])
            for i in range(n):
                st2syn = SpikeTrainToSynapse()
                st2syn.input = self.input.product[i]
                st2syn.output = self.output.product[i]
                st2syn.make()
                self.product.append(st2syn)
            
        return self.product      


class SynapseToCell:
    def __init__(self):
        self.input = None
        self.output = None
        self.product = None
        self.distribution = None
        self.target_feature, self.section_type, self.min_value, self.max_value = None, None, None, None
        
        
    def make(self):
        if self.product is None:
            from neuron import h
            
            self.input.make()
            self.output.make()
            
            if self.distribution:
                self.distribution.make()
            
            if self.distribution.name == "empirical":
                while True:
                    X = self.distribution(interval=True)
                    if X == "somatic":
                        targets = self.output.get(section_type="somatic", optional_X=self.distribution(name="uniform", a=0, b=1))
                    else:
                        targets = self.output.get(target_feature=self.target_feature, min_value=X[0], max_value=X[1], section_type=self.section_type, 
                                                  optional_X=self.distribution(name="uniform", a=0, b=1))
                    if targets:
                        break
                segment = targets[0]
            else:
                targets = self.output.get(target_feature=self.target_feature, min_value=self.min_value, max_value=self.max_value, section_type=self.section_type,
                                          optional_X=self.distribution(name="uniform", a=0, b=1))
                segment = targets[0]
            
            
            self.input.product.loc(segment.x, sec=segment.sec)
            self.product = { self.input.name:self.input.product,
                            "Segment":{"Arc":segment.x,
                                       "Section":segment.sec}}
        return self.product   


class SynapseGroupToCell:
    def __init__(self):
        self.input = None
        self.output = None
        self.product = None
        self.distribution = None
        self.target_feature, self.section_type, self.min_value, self.max_value = None, None, None, None
        
    def make(self):
        if self.product is None:
            from neuron import h
            
            self.input.make()
            self.output.make()
            
            self.product = []
            for i in range(len(self.input.product)):
                syn2cell = SynapseToCell()
                if self.distribution:
                    syn2cell.distribution = self.distribution[i]
                    syn2cell.target_feature, syn2cell.section_type, syn2cell.min_value, syn2cell.max_value = self.target_feature, self.section_type, self.min_value, self.max_value
                syn2cell.input = self.input.product[i]
                syn2cell.output = self.output
                syn2cell.make()
                self.product.append(syn2cell)
            
        return self.product              
        
        

    
    
class Cell:
    def __init__(self, name):
        self.name = name
        self.product = None
        
    def make(self):
        if self.product is None:
            raise Warning("Cell model not translated")
        return self.product
