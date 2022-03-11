class Model(type):


    def __new__(cls, name, bases, attrs, **kwargs):
        res_attrs = 
        return super(Model, cls).__new__(cls, name, bases, attrs)

        #now we're back to the standard `type` 
        #doing this will neuter most of the metaclass behavior, __init__ wont
        #be called.                         👇
        #return super(MyType, mcls).__new__(type, name, bases, attrs)

    #def __init__(cls, name, bases, attrs):
    #    print("  MyType.__init__.cls:%s." % (cls))

        #I can see attributes on Foo and Bar's namespaces
    #    print("    %s.cls_attrib:%s" % (cls.__name__, getattr(cls, "cls_attrib", None)))
    #    return super().__init__(name, bases, attrs)


class Synapse(metaclass=Model):
  attributes = { "gsyn":dict(types=(int, float, Model)),
                 "erev":dict(types=(int, float, Model)) }
  
