#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Model:
    """
    Created on Wed Mar  2 20:14:03 2022
    @author: Francesco Cavarretta
       
    Abstract class representing a model archetype
    """
    
    def __init__(self, name, **kwargs):
        """
        Initialize a model

        Parameters
        ----------
        name: model identifier
        **kwargs : parameters of the model
        """
        
        # store the parameter names
        self.__model_attrs__ = {}
        
        # each model should have a name
        self.name = name
        
        # create parameters
        for varname, varvalue in kwargs.items():
            # check the parameters does not exist to not overwrite any
            # class attribute
            if varname not in self.__dict__:
                setattr(self, varname, varvalue)
                self.__model_attrs__[varname] = []
                
        
    def __str__(self):
        '''
        Returns
        -------
        Model name
        '''
        return self.name
            
    def __setattr__(self, name, value):
        """
        Change the value of an attribute.
        If it is linked to lower level models,
        it updates their parameters alongside.

        Parameters
        ----------
        name : Str
            Attribute name
        value : Str
            Value of the attribute
        """
        
        # check whether it is new
        new_attrs_flag = not hasattr(self, name)
        
        # update the attribute
        super().__setattr__(name, value)
        
        # if it is "__model_attrs__, just return
        if name == "__model_attrs__":
            return
        
        # create the entry
        if new_attrs_flag and name not in self.__model_attrs__:
            self.__model_attrs__[name] = []
        
        # if the attribute is an attribute of the model
        for linkinfo in self.__model_attrs__[name]:
            if len(linkinfo) == 2:
                modelname, attrdest = linkinfo
            elif len(linkinfo) == 3:
                modelname, attrdest, func = linkinfo
                
                try:
                    if isinstance(func, str):
                        # interpret the string, 
                        # which is a chunk of python code
                        
                        # run the code
                        _locals = locals()
                        
                        # compy the local variable
                        for varname in self.__model_attrs__:
                            _locals[varname] = getattr(self, varname)
                            
                        # run python script
                        exec(func, globals(), _locals)
                        
                        # read the value
                        value = _locals["return_value"]
                    elif callable(func):
                        # it is a function
                        # read the parameters of the function
                        value = func(*[
                            getattr(self, varname) for varname in func.__code__.co_varnames
                            ])
                        
                    else:
                        raise ValueError(f"The link for variable {name} was not properly defined (2)")
                except:
                    raise Exception(f"The link for variable {name} was not properly defined: an error occurred while running its map function")
                    
            else:
                raise ValueError(f"The link for variable {name} was not properly defined (1)")
            
            # update the value
            setattr(getattr(self, modelname), attrdest, value)
                
                
                
    def __linkattr__(self, attrsrc, submodel, attrdest, func=None):
        """
            Link attributes between two models 
            from the parent model to the child model
            
            Parameters
            attrsrc: attribute name of the parentmodel
            modelname: name of the destination model
            attrdest: name of the attribute in the destination model
        """
        
        # source attribute existing
        assert attrsrc in self.__model_attrs__
        
        # the parameter should be a model
        assert submodel in self.__model_attrs__
        
        # retrieve the model
        submodel_dest = getattr(self, submodel)
        
        # which have also that attribute
        assert isinstance(submodel_dest, Model) and \
            hasattr(submodel_dest, attrdest)
    
        if func:  
            # otherwise it runs and interpret a function
            # function can be also a string
            self.__model_attrs__[attrsrc].append((submodel, attrdest, func))
            
        else:
            # if func is None, the link just copy the value of a parameter
            # into another
            self.__model_attrs__[attrsrc].append((submodel, attrdest))
        
        # update the attribute in the model
        self.__setattr__(attrsrc, getattr(self, attrsrc))
        

    def copy(self, deep=True):
        """
            Create a soft copy of the object
            deep: If true, it returns a deep copy (default True),
            creating also new instances of the children models,
            otherwise a soft copy, 
            which continue to reference the same children models

        Returns
        -------
        Copy of the Model Object
        """        
        import copy
        return (copy.deepcopy if deep else copy.copy)(self)
    
    def __call__(self, deep=True):
        """
            Create a copy of the Model
            deep: If true, it returns a deep copy (default True)

        Returns
        -------
        Copy of the Model Object

        """
        return self.copy(deep=deep)
    
    
if __name__ == "__main__":
    m1 = Model("test1")
    m2 = Model("test2")
    m2.test2 = 2
    m1.test1 = 5
    m1.model2 = m2
    
    print (m1.test1, m2.test2)
        
    def myfunc(test1):
        return test1/2
        
    m1.__linkattr__("test1", "model2", "test2", func=myfunc)

    print (m1.test1, m2.test2)
    
    m1.test1 = 77
    
    print (m1.test1, m2.test2)


    m1_copy = m1.copy()
    
    m1_deep_copy = m1.copy(deep=True)
    
    m1_copy.test1 = 44.0
    m1_deep_copy.test1 = 96.0
    
    print (m1.test1, m2.test2)
    print (m1_copy.test1, m2.test2)
    print (m1_deep_copy.test1, m2.test2, m1_deep_copy.model2.test2)
    