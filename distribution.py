#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import model

class Distribution(model.Model):
    def __init__(self, name, **kwargs):
        """
            Models of Probability Distributions

        Parameters
        ----------
        name : str
            probability distribution name
        **kwargs : parameters of the distribution
        """
        model.Model.__init__(self, name, **kwargs)
        
        if self.name == "gamma":
            self.__linkattr__("var", "std", function="import math\nsqrt(std)")
        self.__linkattr__("var", "std", function="import math\nsqrt(std)")
            
    @property
    def var(self):
        return self.var
    

if __name__ == "__main__":
    d = Distribution("Gamma")
    d.var = 5