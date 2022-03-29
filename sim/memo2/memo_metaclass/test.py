class Model(type):            
            
    def __iter__(self):
        """
        Iterate attributes and values
        -----------------------------
        return iterator of attributes and values
        """
        return [ (attrname, getattr(self, attrname)) for attrname in getattr(self, "__model_attrs") ].__iter__()
    
    
    """
    A metaclass allowing the definition of attributes,
    and edges between models for definition of relation between themselves.
    """
    def _mk_fget(attrname):
        """
        Create a new getter-function for an attribute
        attrname: attribute name
        ------------------------------------------
        return the getter function assigned to the attribute
        """
        def fget(self):
            return getattr(self, attrname)
        return fget
    
    
    # set function of the property
    def _mk_fset(attrname, vartypes):
        """
        Create a new setter-function for an attribute
        attrname: attribute name
        ------------------------------------------
        return the setter function assigned to the attribute
        """
        def fset(self, value):
            # color the graph node
            if not self.__colored:
                self.__colored = True
                
                # check types
                if not isinstance(value, vartypes):
                    raise TypeError(f"{value} not a valid type for {attrname[2:]}: it takes only {[vt.__name__ for vt in vartypes]} while was passed {type(value).__name__}")
                
                # set attributes
                setattr(self, attrname, value)
                
                # flush the attributes in a link
                if attrname[2:] in self.__edge:
                    for rel in self.__edge[attrname[2:]]:
                       rel._flush(self)
                        
                # remove the color
                self.__colored = False
                
        return fset
    
    
    def __new__(cls, name, bases, attrs):
         """
         Create attributes for the new class model
         name: name of the new class
         bases: superclasses
         attrs: attributes of the class
         -----------------------------------
         return the new class
         """
         
         res_attrs = {}
         
         if 'attributes' in attrs:                          
             for attrname, definition in attrs['attributes'].items():
                 # internal identifier of the property
                 _pvt_attrname = f"__{attrname}"
                
                 # initial value
                 res_attrs[_pvt_attrname] = definition["init_value"] if "init_value" in definition else 0.0
                 
                 # is a read_only property
                 is_read_only = definition["read_only"] if "read_only" in definition else False
                 
                 # set the property
                 _property_args = (cls._mk_fget(_pvt_attrname), )
                 if not is_read_only:                         
                     _property_args += (cls._mk_fset(_pvt_attrname, definition["type"]), )
                 
                 # set the property
                 res_attrs[attrname] = property(*_property_args)
                 
             # model attributes
             res_attrs["__model_attrs"] = list(attrs["attributes"].keys())
         
         # define the make_edge method
         res_attrs["_make_edge"] = cls._make_edge
         res_attrs["__iter__"] = cls.__iter__
         
         return super().__new__(cls, name, bases, res_attrs)
     
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls.__colored = False
        cls.__edge = {}
        
    
    def _make_edge(self, attrname, rel):
        """
        Makes a link between classes
        attrname : attribute name
        rel : linking object
        """
        # attribute must exist                
        assert attrname in self.__class__.__dict__ and \
            isinstance(rel, Link)
        
        if attrname not in self.__edge:
            # create the list
            # if the entry does not exist
            self.__edge[attrname] = []
            
        self.__edge[attrname].append(rel) # add the relation


class Link:
    """
    Link attributes between models
    """
    
    def __init__(self, model1, attrname1, model2, attrname2, function_attr1_to_attr2=None, function_attr2_to_attr1=None):
        """
        model1 : model #1
        attrname1 :  attribute of model #1 which should be linked
        model2 : model #2
        attrname2 :  attribute of model #1 which should be linked
        """
        assert isinstance(model1.__class__, Model) and isinstance(model2.__class__, Model)
        
        if function_attr1_to_attr2:
            assert callable(function_attr1_to_attr2) or type(function_attr1_to_attr2) == str
            
        if function_attr2_to_attr1:
            assert callable(function_attr2_to_attr1) or type(function_attr2_to_attr1) == str
            
        self.model1, self.attrname1, self.function_attr1_to_attr2 = model1, attrname1, function_attr1_to_attr2
        self.model2, self.attrname2, self.function_attr2_to_attr1 = model2, attrname2, function_attr2_to_attr1
        
        # make the edges
        self.model1._make_edge(self.attrname1, self)
        self.model2._make_edge(self.attrname2, self)
        
        
        
    def _flush(self, calling_model):
        """
        Flush the other model attributes.
        calling_model : model from which flush was called.
        """
        if calling_model == self.model1:
            model_dest, model_src, attrname_dest, attrname_src = self.model2, self.model1, self.attrname2, self.attrname1
            conversion_function = self.function_attr1_to_attr2
        elif calling_model == self.model2:            
            model_dest, model_src, attrname_dest, attrname_src = self.model1, self.model2, self.attrname1, self.attrname2
            conversion_function = self.function_attr2_to_attr1
        else:
            raise ValueError("Unknown model for this link")
            
        if conversion_function:
            if callable(conversion_function):
                # there is a conversion function to execute
                value = conversion_function(*([self] + [ getattr(model_src, varname) for varname in conversion_function.__code__.co_varnames[1:conversion_function.__code__.co_argcount] ]))
            elif type(conversion_function) == str:
                # run the code
                _locals = locals()
                
                # compy the local variable
                _locals.update({ var[0]:var[1] for var in model_src })
                    
                # run python script
                exec(conversion_function, globals(), _locals)
                
                # read the value
                value = _locals[attrname_dest]
                
                # clean
                del _locals
            else:
                raise TypeError("Conversion function cannot be executed")
        else:
            value = getattr(model_src, attrname_src)
            
        # set attribute value
        setattr(model_dest, attrname_dest, value)
        
        
if __name__ == "__main__":
    class Synapse1(metaclass=Model):
        attributes = { 
                'gsyn':{'type':(int, float), 'init_value':0.0},
                'erev':{'type':(int, float), 'init_value':0.0}
                }
        
    class Synapse2(metaclass=Model):
        attributes = { 
                'gsyn1':{'type':(int, float), 'init_value':0.0},
                'erev1':{'type':(int, float), 'init_value':0.0}
                }
        
    s1 = Synapse1()
    s2 = Synapse2()
    
    def f1(link, gsyn):
        return gsyn/20
    def f2(link, gsyn1):
        return gsyn1*10
    
    str_f1 = "gsyn1 = gsyn / 20"
    
    l = Link(s1, 'gsyn', s2, 'gsyn1', function_attr1_to_attr2=str_f1, function_attr2_to_attr1=f2)
    
    s1.gsyn = 5
    
    print (s1.gsyn, s2.gsyn1)