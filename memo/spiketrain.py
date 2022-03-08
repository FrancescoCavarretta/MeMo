#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 09:37:14 2022

@author: francesco
"""

from .model import Model, ModelPopulation
from .distribution import Distribution

class SpikeTrain(Model):
    def __init__(self, name, **kwargs):    
        """
            It contains a model of spike trains.
            name: spike train identifier
            **kwargs : parameters of the spike train model.
        """
        
        Model.__init__(self, name, **kwargs)
        
        if self.name == "abbasi":
            self.distribution = Distribution("gamma")
            self.__linkattr__("regularity", "k", submodel="distribution")
            self.__linkattr__("regularity", "theta", submodel="distribution", function="theta=1.0/regularity")
            
            self.__linkattr__("mean_rate", "rate", function="rate=rate/rate.mean()*mean_rate")
        elif self.name == "poissonian":
            self.distribution = Distribution("poisson")
            
            self.__linkattr__("mean_rate", "mean", submodel="distribution")
        else:
            raise NameError(f"Unknown type of Spike Train {self.name}")
            
            
            
class SpikeTrainPopulation(ModelPopulation):
    def __init__(self, name, **kwargs):    
        """
            It contains a population of different spike train models.
            For each, we define the number of its instances.
            name: model group identifier
            **kwargs : parameters of the model.
            If the name begin with "n_[spiketrain]",
            it indicates a repetition of models [spiketrain]
        """
        ModelPopulation.__init__(self, name, **kwargs)  
            

    def __setattr__(self, attrname, value, *args):    
        """
            Perform a type checking before fixing the values
        """
        # two only exception, check it is a SpikeTrain
        if attrname != "name" and attrname != "__model_attrs__" and not attrname.startswith("n_"):  
            # contains Model only in other cases
            assert isinstance(value, SpikeTrain)  
        
        # set the attribute
        super().__setattr__(attrname, value, *args)

            
if __name__ == "__main__":
    import numpy as np
    st = SpikeTrain("abbasi", regularity=2.0, time=np.array([1,2,3,5,6]), rate=np.array([4,5,6,7,7]), mean_rate=3)
