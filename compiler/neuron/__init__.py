#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SpikeTrain:
    def abbasi(self, distribution, time, rate, refractory_period):
        UnGamma=None
        Precision=10
        max_frequency=None
        min_frequency=None
        
        import numpy as np
        
        """ let's test the consistency of the configuration """
        if max_frequency is None:
            max_frequency = 1.0/refractory_period
        
        if min_frequency is None:
            min_frequency = 1e-5
          
        assert min_frequency < max_frequency
        assert max_frequency <= 1.0/refractory_period
          
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
        while I < len(frequency):
            # gamrnd = matlab fn for random arrays from gamma distribution. 
            # Given arguments get a mean firing rate of 1
            X = distribution() #np.random.gamma(Reg, scale=1.0/Reg)
            
            
            J = I
            for z in range(Precision):
                MeanRate = np.mean(frequency[I:(J+1)]) # calculate mean rate over expected mean interval
                CurrentISI = X*RateToISI(MeanRate)  
                J = min([ len(frequency)-1, I+int(round(CurrentISI/TimeBinSz)) ])  # calculate the interval boundary
    
              
            
            if UnGamma:
                # for cases where templates have sudden large
                # increases in rate, which leads to very slow catchup performance wiht
                # default algorithm.  If algorithmflag==2 then the current interval is
                # examied for rate changes of factor > ungam, and if one is found, the
                # maximal rate for the original interval is determined.  Then the
                # original interval is shortened to the time where the rate exceeds
                # ungam, and a 2nd interval for the new max rate is added.
                MaxRate = np.max(frequency[I:(J+1)])
                if MaxRate > UnGamma*frequency[I]:
                    CurrentISI = X*RateToISI(MaxRate)
            
            
            ISIs.append(CurrentISI)
            I += int(round(CurrentISI/TimeBinSz))
        
        
        # spike times
        SpikeTimes = np.cumsum(ISIs)
        SpikeTimes = SpikeTimes[SpikeTimes <= time[-1]]
        return SpikeTimes

    
    def poissonian(self, distribution, tstop):
        import numpy as np
            
        SpikeTimes = np.array([0.])
        
        while SpikeTimes[-1] < tstop:
            while True:
                try:
                    CurrentISI = 1.0 / distribution()
                    break
                except ZeroDivisionError:
                    pass
            SpikeTimes = np.concatenate((SpikeTimes, [SpikeTimes[-1] + CurrentISI]))
        
        return SpikeTimes
    
    
    
    def __init__(self, name):
        self.product = None
        
        self.generation_function = getattr(self, name)
        for x in self.generation_function.__code__.co_varnames[1:self.generation_function.__code__.co_argcount]:
            setattr(self, x, None)
            
    def make(self):
        if self.product is None:
            self.product = self.generation_function(*[getattr(self, x) for x in self.generation_function.__code__.co_varnames[1:self.generation_function.__code__.co_argcount]])
        return self.product
        
        
        

    

class Distribution:
    __distribution__ = {
        "uniform":("neuron", "a", "b"),
        "discunif":("neuron", "a", "b"),
        "normal":("neuron", "mean", "var"),
        "poisson":("neuron", "mean"),
        "gamma":("numpy", "k", "theta")
        }
    
    
    def neuron(self):
        import neuron as nrn    
        rng = nrn.h.Random()
        rng.Random123(*self.seed)
        return rng
    
    def numpy(self):
        import numpy as np
        return np.random.Generator(np.random.Philox(*self.seed))
        
    
    def __init__(self, seed, name):
        self.name = name
        params = Distribution.__distribution__[name]
        self.seed = seed
        self.product = getattr(self, params[0])()
        self.params = params[1:]
        
        for _param in self.params:
            setattr(self, _param, None)
    
    def make(self):
        return self.product
            
    def __call__(self):
        return getattr(self.product, self.name)(*[getattr(self, pname) for pname in self.params])
    
    
    
    
class Synapse:
    def __init__(self, name):
        from neuron import h
        self.name = name
        self.Section = h.Section()
        self.Exp2Syn = h.Exp2Syn()
        self.NetCon = h.NetCon(None, None)
        self.Exp2Syn.loc(0.5, sec=self.Section)
        self.NetCon.setpost(self.Exp2Syn)
        self.product = { "Exp2Syn":self.Exp2Syn, "NetCon":self.NetCon }
        
    @property
    def erev(self):
        return self.Exp2Syn.e
    
    @erev.setter
    def erev(self, value):
        self.Exp2Syn.e = value
        
    @property
    def gsyn(self):
        return self.NetCon.weight[0]
    
    @gsyn.setter
    def gsyn(self, value):
        self.NetCon.weight[0] = value
        
    def make(self):
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
        if self.product:
            return self.product
        self.product = []
        for x in self.__dict__.values():
            if type(x) == list:
                for obj in x:
                    self.product.append(obj.make())
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
        from neuron import h
        
        self.input.make()
        self.output.make()
        
        
        vec = h.Vector(self.input.product)
        self.product = (vec, )
        return self.product
        #vs = h.VecStim()
        #vs.play(vec)
        #self.output.NetCon.setpre(vs)
        #self.product = (vec, vs)
        #return self.product     
    
    
        
class SpikeTrainPopulationToSynapseGroup:
    def __init__(self):
        self.input = None
        self.output = None
        self.product = None
        
    def make(self):
        from neuron import h
        
        self.input.make()
        self.output.make()
        
        self.product = []
        n = min([len(self.input.product), len(self.output.product)])
        for i in range(n):
            st2syn = SpikeTrainToSynapse()
            st2syn.input = self.input.product[i]
            st2syn.output = self.output.product[i]
            self.product.append(st2syn)
            
        return self.product      