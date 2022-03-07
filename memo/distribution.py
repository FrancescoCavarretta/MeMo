#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .model import Model

class Distribution(Model):
    __DISTRLINKS__ = {
        "gamma":{
            ("k", "theta"):dict(var="var=k*(theta**2)", 
                                    mean="mean=k*theta"),
            ("mean", "var"):dict(k="k=(mean**2)/var",
                                 theta="theta=var/mean"),
            ("mean", "std"): ("mean", "var"),
            None:dict(k=1, theta=1)
        },
        "poisson":{
            "l":dict(var="var=l", mean="mean=l"),
            "mean":dict(l="l=mean"),
            "var":dict(l="l=var"),
            "std":"var",
            None:dict(mean=1)
        },
        "uniform":{
            ("a", "b"):dict(mean="mean=(a+b)/2", var="var=1/12*(b-a)**2"),
            ("mean", "var"):dict(b="b=sqrt(3*var)+2*mean", a="a=2*mean-b"),
            ("mean", "std"):("mean", "var"),
            None:dict(a=0, b=1)
        },
        "normal":{
            ("mean", "var"):dict(),
            ("mean", "std"):("mean", "var"),
            None:dict(mean=0, std=1)
        }
    }
    
    
    def get_standard_params(distr_name):
        """
        Return the parameters making the standard distribution
        Parameters
        ----------
        distr_name : str
            distribution name

        Returns
        -------
        standard params
        """
        # get the parameters
        try:
            return Distribution.__DISTRLINKS__[distr_name][None]
        except KeyError:
            raise ValueError(f"Distribution {distr_name} not known")
            
            
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
                if key:
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
                
                # link variance and standard deviation        
                # variance and std. dev. should be always defined 
                # if "std" was an argument, we need to map std->var first
                if hasattr(self, "std"):   
                    self.__linkattr__("std", "var", function="var=std**2")   
                    self.__linkattr__("var", "std", function="import math\nstd=math.sqrt(var)") 
                elif hasattr(self, "var"):
                    self.__linkattr__("var", "std", function="import math\nstd=math.sqrt(var)")
                    self.__linkattr__("std", "var", function="var=std**2")  
                
                
                
        # if no additional parameter, set  the standard parameters
        if len(kwargs) == 0:
            kwargs = Distribution.get_standard_params(name)
                
        # initialize
        Model.__init__(self, name, **kwargs)
        
        # distribution links
        distrlinks = Distribution.get_param_links(self.name)
        # if not a str or tuple, it is a key
        # we start by mapping the parameters passed as an argument
        try:        
            param_names = tuple(kwargs.keys())
            if len(kwargs) == 1:
                param_names = param_names[0]
            set_map_attrs(param_names, distrlinks)
        except KeyError:
            raise ValueError(f"Combination of parameters not recognized for the distribution {self.name} not known: {kwargs.keys()} {distrlinks}")
        
        
        # map the other parameters
        for attrsrc in list(distrlinks.keys()):
            set_map_attrs(attrsrc, distrlinks)
            
 

if __name__ == "__main__":
    d1 = Distribution("gamma", k=1, theta=2)
    d2 = Distribution("gamma", mean=1, var=2)
    d3 = Distribution("normal")
    d3 = Distribution("poisson")
