import memo
import memo.model as model
import memo.link as link
import memo.microcircuit as microcircuit
import memo.distribution as distribution


# set of random object which requires a seed assignment
_random_objects = set()
_random_objects.add(memo.distribution.Distribution)





class SeedGenerator:
    """
        Generate a sequence of seeds
    """
    def __init__(self, seed=1):
        """
            Generate a sequence of seeds assigned to object forming a simulation
        Parameters
        ----------
        seed : int or list (default is 1)
        """
        
        if type(seed) == tuple:        
            # if it is a tuple, convert to list
            self.seed = list(seed)
        elif type(seed) == int:
            # if an integer, generalize to a list
            self.seed = [seed]
        elif type(seed) == list:
            self.seed = seed + []
        else:
            raise ValueError("Seed format not valid")


    def get(self):
        """
        Return a seed

        Returns
        -------
        integer or tuple, depending on the seed format
        """
        for i in range(len(self.seed)):
            self.seed[i] += 1       
        return self.seed[0] if len(self.seed) == 1 else tuple(self.seed)
    
    
    def __call__(self):
        """
        Return a seed

        Returns
        -------
        integer or tuple, depending on the seed format
        """
        return self.get()
    

def _mk_simobject(x, seedgen, models, links):
    """
    Pre-compile an object, organizing the meta-model/meta-data in a structure
    and assigning the seeds for those which are translated to a random object.

    Parameters
    ----------
    x : Model, ModelPopulation, Link
        Model or Link to compile
    seedgen : SeedGenerator
        generator of seeds
    models : map/dict
        Collection of pre-compiled models, retrievable by the hash of the model object
    links : TYPE
        Collection of pre-compiled links, retrievable by the hash of the model object

    Returns
    -------
    map
    Pre-compiled model or link
    """
    # the model or link might have been packged already
    
    if x in models:
        return models[x]
    elif x in links:
        return links[x]
    else:        
        ret = { 
            "object":x,
            }
        
        if isinstance(x, link.Link):
            # it is a link
            ret["is_link"] = True
            
            # link input and output models
            ret["input"]  = _mk_simobject(x.input, seedgen, models, links)
            ret["output"] = _mk_simobject(x.output, seedgen, models, links)
            ret["input_link"]  = ret
            ret["output_link"] = ret
            
            # add the link
            links[x] = ret
        elif isinstance(x, link.Model):
            ret["is_link"] = False
            
            # add the model
            models[x] = ret
        else:
            raise ValueError(f"It can convert only Model or Link objects: {x}")
            
            
        # check whether it requires a seed assignment
        if type(x) in _random_objects:
            ret["seed"] = seedgen()
            
        # compile the submodels
        ret["submodels"] = {}
        
        # be careful here, as ModelPopulation is a subclass of Model
        if isinstance(x, model.Model):
            if isinstance(x, model.ModelPopulation):
                # if it is a ModelPopulation there may be multiple instances of a given model
                for mname in x.itersubmodels():
                    n = getattr(x, "n_" + mname)
                    ret["submodels"][mname] = [_mk_simobject(getattr(x.copy(), mname), seedgen, models, links) for i in range(n)]
            else:
                # otherwise we assume there is a single instance for a model
                for mname in x.itersubmodels():
                    ret["submodels"][mname] = _mk_simobject(getattr(x, mname), seedgen, models, links)
            
        return ret
        



        

def precompile(circuit, seed):
    """
    Pre-compile a model of brain circuit
    """
    models = {}
    links = {}
    
    seedgen = SeedGenerator(seed)
    
    for m in circuit.models:
        _mk_simobject(m, seedgen, models, links)
            
    for l in circuit.links:
        _mk_simobject(l, seedgen, models, links)
    
    return { "models":models, "links":links }
                
                
                
if __name__ == "__main__":
    import memo.spiketrain as st
    import memo.distribution as ds
    import memo.microcircuit as mc
    import memo.link as ln
    mc1 = mc.MicroCircuit("Test")
    s1=st.SpikeTrain("poissonian", mean_rate=55.0)
    s2=st.SpikeTrain("poissonian", mean_rate=9.0)
        
        
    l = ln.Link(s1, s2)
    mc1.add(s1)
    mc1.add(s2)
    mc1.add(l)
    seedgen = SeedGenerator(1)
    r = mk_simulation(mc1, seedgen)
    
    