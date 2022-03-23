#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .model import Model

class Link:
    def __init__(self, input, output, distribution=None, **kwargs):
        
        """
        Connect two Models

        Parameters
        ----------
        input : TYPE
            input model, providing data to the output model
        output : TYPE
            output model, receiving data generated by the input model
        func : TYPE, optional
            Function connecting variables (default None)

        """
        
        # initialize the properties
        self.__input = None
        self.__output = None
        self.__distribution = distribution

        if "target" in kwargs:
            self.target_feature, self.section_type, self.min_value, self.max_value = kwargs["target"]
            assert self.target_feature == "diam" or self.target_feature == "dist" or self.target_feature == "order"
        
        # set the properties
        self.input, self.output = \
            input, output

        
    @property
    def distribution(self): 
        """
        Returns
        -------
            input model of the link
        """
        return self.__distribution
    
    
    @distribution.setter
    def distribution(self, m):
        """
        Parameters
        ----------
        m : Model
            Model of input
        """
        assert isinstance(m, Model)
        self.__distribution =  m
        
        
    @property
    def input(self):
        """
        Returns
        -------
            input model of the link
        """
        return self.__input
    
    
    @input.setter
    def input(self, m):
        """
        Parameters
        ----------
        m : Model
            Model of input
        """
        assert isinstance(m, Model)
        self.__input =  m
        
        
    @property
    def output(self):        
        """
        Returns
        -------
        output model of the link
        """
        return self.__output
    
    
    @output.setter
    def output(self, m):
        """
        Parameters
        ----------
        m : Model
            Model of output
        """
        assert isinstance(m, Model)
        self.__output =  m
          

if __name__ == "__main__":
    from model import Model
    m1 = Model("m1")
    m2 = Model("m2")
    l = Link(m1, m2)
    m1.test1 = 2
    m2.test2 = 44
    
    def myfunc(input, output):
        output.test2 = input.test1
        
    l.function = myfunc
        
    print (m1.test1, m2.test2)
