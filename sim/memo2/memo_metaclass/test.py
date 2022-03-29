class MetaModel(type):
    def __new__(cls, name, bases, attrs):
         """
         Create attributes for the new class
         name: name of the new class
         bases: superclasses
         attrs: attributes of the class
         -----------------------------------
         return the new class
         """
         
         res_attrs = {}
         
         if 'attributes' in attrs:             
             # get function of the property
             def mk_fget(attrname):
                 def fget(self):
                     return getattr(self, attrname)
                 return fget
             
             # set function of the property
             def mk_fset(attrname, vartypes):
                 def fset(self, value):
                     # color the graph node
                     if not self.__colored:
                         self.__colored = True
                         
                         # check types
                         if not isinstance(value, vartypes):
                             raise TypeError(f"{value} not a valid type for {attrname[2:]}: it takes only {[vt.__name__ for vt in vartypes]} while was passed {type(value).__name__}")
                         
                     
                         # flush the attributes in a link
                         if attrname in self.__edge:
                             for rel in self.__edge[attrname]:
                                 rel.flush(self)
                                 
                         # remove the color
                         self.__colored = False
                         
                         # set attributes
                         setattr(self, attrname, value)
                         
                 return fset
             
             for attrname, definition in attrs['attributes'].items():
                 # internal identifier of the property
                 _pvt_attrname = f"__{attrname}"
                
                 # initial value
                 res_attrs[_pvt_attrname] = definition["init_value"] if "init_value" in definition else 0.0
                 
                 # is a read_only property
                 is_read_only = definition["read_only"] if "read_only" in definition else False
                 
                 # set the property
                 _property_args = (mk_fget(_pvt_attrname), )
                 if not is_read_only:                         
                     _property_args += (mk_fset(_pvt_attrname, definition["type"]), )
                 
                 # set the property
                 res_attrs[attrname] = property(*_property_args)
                 
         return super().__new__(cls, name, bases, res_attrs)
     
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls.__colored = False
        cls.__edge = {}
        
        
    def make_edge(self, attrname, rel):
        self.__edge[attrname] = rel



        
        

class Synapse1(metaclass=MetaModel):
    attributes = { 
            'gsyn':{'type':(int, float), 'init_value':0.0},
            'erev':{'type':(int, float), 'init_value':0.0}
            }
s1 = Synapse1()
#s1.gsyn