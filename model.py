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
                self.__model_attrs__[varname] = {}
                
        
    def __str__(self):
        '''
        Returns
        -------
        Model name
        '''
        return self.name
            
    def __setattr__(self, name, value, *args):
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
        
        # base of the eventual recursion
        # name is fixed at the initialization so it does not make problems
        if len(args) > 0:
            # check the recursion
            if (self.name + "." + name) in args:
                return  
            
        # list of set attributes
        args += ((self.name + "." + name), )
                
        # create the entry
        if new_attrs_flag and name not in self.__model_attrs__:
            self.__model_attrs__[name] = {}      
        
        # if the attribute is an attribute of the model
        for attrdest_ref, function in self.__model_attrs__[name].items():
            
            # define the outputmodel
            if type(attrdest_ref) == tuple:
                # then it is an attribute of the submodel
                output_model, attrdest = attrdest_ref
            else:
                output_model = self
                attrdest = attrdest_ref
                
            # if there is a map function
            if function:
                try:
                    if isinstance(function, str):
                        # interpret the string, 
                        # which is a chunk of python code
                        
                        # run the code
                        _locals = locals()
                        
                        # compy the local variable
                        for varname in self.__model_attrs__:
                            _locals[varname] = getattr(self, varname)
                            
                        # run python script
                        exec(function, globals(), _locals)
                        
                        # read the value
                        value = _locals[attrdest]
                    elif callable(function):
                        # it is a function
                        # read the parameters of the function
                        value = function(*[
                            getattr(self, varname) for varname in function.__code__.co_varnames
                            ])
                        
                    else:
                        raise ValueError(f"The link for variable {name} was not properly defined (2)")
                except:
                    raise Exception(f"The link for variable {name} was not properly defined: an error occurred while running its map function")

            
            # update the value
            # there is a risk of recursion at this point
            # rink of infinite recursion
            # ---> setattr(output_model, attrdest, value) <---
            output_model.__setattr__(attrdest, value, *args)
                      
                
    def __linkattr__(self, attrsrc, attrdest, **kwargs):
        """
            Link attributes between two models 
            from the parent model to the child model
            
            Parameters
            attrsrc: attribute(s) name(s) of the parentmodel
            attrdest: name of the attribute in the destination model
            
            kwargs: it can contain two only parameters for now
            modelname: name of the destination model
            func: function of mapping
        """
        # standardize to something iterable
        if type(attrsrc) == str:
            attrsrc = (attrsrc, )
            
        # it can be either a link between variables of between models
        if len(kwargs) > 0:
            # there are not others parameters than "submodel" or "function"
            assert len(set(kwargs.keys()).difference(["submodel", "function"])) == 0
            
        # perform two checks
        if "submodel" in kwargs:       
            # retrieve the model
            submodel = getattr(self, kwargs["submodel"])
            
            # which should have also that attribute
            assert isinstance(submodel, Model) and \
                hasattr(submodel, attrdest)
        else:
            submodel = None
            

        if "function" in kwargs:     
            function = kwargs["function"]
            
            # which should have also that attribute
            assert callable(function) or isinstance(function, str)
        else:
            function = None
            
            
        # reformat attrdest if needed
        if submodel:
            attrdest = (submodel, attrdest)
            
        # create the link(s)
        for _attrsrc in attrsrc:
            # source attribute existing
            assert _attrsrc in self.__model_attrs__
        
            # add the link
            self.__model_attrs__[_attrsrc][attrdest] = function            
            
            # update the attribute in the model
            self.__setattr__(_attrsrc, getattr(self, _attrsrc))
        

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
    



class ModelPopulation(Model):
    """
        It contains a population of different models.
        For each, we define the number of its instances.
        name: model group identifier
        **kwargs : parameters of the model.
        If the name begin with "n_[modelname]",
        it indicates a repetition of models [modelname]
    """
    def __init__(self, name, **kwargs):        
        # check whether the number of instance were fixed
        # otherwise create the variable n_[modelname]
        # and n_[modelname] needs to be create after the model vars
        from collections import OrderedDict 
        
        kwargs = OrderedDict(dict())
        for k in kwargs.keys():
            if k.startswith("n_"):
                kwargs.move_to_end(k)
                
        Model.__init__(self, name, **kwargs) 
        

                

    def __setattr__(self, attrname, value, *args):
        """
            Perform a type checking before fixing the values
        """        

        # set the attributes
        super().__setattr__(attrname, value, *args)
        
        # two only exception
        if attrname != "name" and attrname != "__model_attrs__":
            # type checking
            if attrname.startswith("n_"):     
                # we can fix numbers only for n_[modelname] or Models describing the number
                assert attrname[2:] in self.__model_attrs__ and (type(value) == int or isinstance(value, Model))
            else:
                # contains Model only in other cases
                assert isinstance(value, Model)        
                
            # set n instances
            nattrname = "n_" + attrname
            if not hasattr(self, nattrname):
                super().__setattr__(nattrname, 1, *args)
            
        
        
            
            
            

if __name__ == "__main__":
    m1 = Model("test1")
    m2 = Model("test2")
    m2.test2 = 2
    m1.test1 = 5
    
    m1.model2 = m2
    
    print (m1.test1, m2.test2)
        
    def myfunc(test1):
        return test1/2
        
    m1.__linkattr__("test1", "test2", submodel="model2", function=myfunc)
    #m1.__linkattr__("test1", "test2", submodel="model2", function="test2=test1*5")

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
    
    m3 = Model("test3")
    m3.test1 = 9
    m3.test2 = 10
    m3.__linkattr__("test1", "test2", function="test2=test1*2")
    print (m3.test1, m3.test2)
    
    mp = ModelPopulation('testpop', n_m1=5, m1=m1, m2=m2, m3=m3)