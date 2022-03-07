#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import model

class Distribution(model.Model):
    __DISTRLINKS__ = {
        "gamma":{
            ("k", "theta"):dict(var="var=k*(theta**2)", 
                                    mean="mean=k*theta"),
            ("mean", "var"):dict(k="k=(mean**2)/var",
                                 theta="theta=var/mean"),
            ("mean", "std"): ("mean", "var")
        },
        "poisson":{
            "l":dict(var="var=l", mean="mean=l"),
            "mean":dict(l="l=mean"),
            "var":dict(l="l=var"),
            "std":"var"
        },
        "uniform":{
            ("a", "b"):dict(mean="mean=(a+b)/2", var="var=1/12*(b-a)**2"),
            ("mean", "var"):dict(b="b=sqrt(3*var)+2*mean", a="a=2*mean-b"),
            ("mean", "std"):("mean", "var")
        },
        "normal":{
            ("mean", "var"):dict(),
            ("mean", "std"):("mean", "var")
        }
    }
    
    
    def get_param_links(distr_name):
        """
        Return the parameter links for that distribution
        If the map has multiple parameters as a source, the key is a key in alphabetic order.
        Parameters
        ----------
        distr_name : str
            distribution name

        Returns
        -------
        links

        """
        import copy
        
        # get the parameters
        try:
            ret = {}
            for key, values in Distribution.__DISTRLINKS__[distr_name].items():
                if type(key) == tuple:
                    key = tuple(sorted(key))
                
                ret.update({key:copy.deepcopy(values)})
            return ret
        except KeyError:
            raise ValueError(f"Distribution {distr_name} not known")
            
            
    def __init__(self, name, **kwargs):
        """
        Models of Probability Distributions

        Parameters
        ----------
        name : str
            probability distribution name
        **kwargs : parameters of the distribution
        """

        # map the attributes
        def set_map_attrs(attrsrc, distrlinks):
            
            def next_link(attrsrc):
                # convert to a set
                if type(attrsrc) == tuple:
                    attrsrc = tuple(sorted(attrsrc))
                
                # retrive the maps for the attributes
                return distrlinks[attrsrc]
            
            # iterate untile we find the first definition
            attrdest_dict = next_link(attrsrc)
            
            while type(attrdest_dict) != dict:
                attrsrc = attrdest_dict
                attrdest_dict = next_link(attrdest_dict)
                
                
            # create the map for each attribute
            for attrdest, function in attrdest_dict.items():
                self.__linkattr__(attrsrc, attrdest, function=function)
                
                
        # initialize
        model.Model.__init__(self, name, **kwargs)
        
      
 
        
        # distribution links
        distrlinks = Distribution.get_param_links(self.name)
        # if not a str or tuple, it is a key
        # we start by mapping the parameters passed as an argument
        try:        
            set_map_attrs(tuple(kwargs.keys()), distrlinks)
        except KeyError:
            raise ValueError(f"Combination of parameters not recognized for the distribution {self.name} not known: {kwargs.keys()} {distrlinks}")
        
        
        # link variance and standard deviation        
        # variance and std. dev. should be always defined 
        # if "std" was an argument, we need to map std->var first
        if "std" in kwargs:  
            self.__linkattr__("std", "var", function="var=std**2")  
            self.__linkattr__("var", "std", function="import math\nstd=math.sqrt(var)")  
        else:
            self.__linkattr__("var", "std", function="import math\nstd=math.sqrt(var)") 
            self.__linkattr__("std", "var", function="var=std**2")   
        
        # map the other parameters
        for attrsrc in list(distrlinks.keys()):
            set_map_attrs(attrsrc, distrlinks)
        
 

if __name__ == "__main__":
    d1 = Distribution("gamma", k=1, theta=2)
    d2 = Distribution("gamma", mean=1, var=2)