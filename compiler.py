import memo
import memo.model as model
import memo.link as link
import memo.microcircuit as microcircuit
import memo.distribution as distribution


# set of random object which requires a seed assignment
_random_object = set()
_random_object.add(memo.distribution.Distribution)





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
    if x in models:
        return models[x]
    elif x in links:
        return links[x]
    
    else:        
        so = {"object":x}     
        
        if isinstance(x, model.Model):
            models[x] = so
        elif isinstance(x, link.Link):
            links[x] = so
        else:
            raise Exception()
            
        if type(x) in _random_object:
            so["seed"] = seedgen()
            
        if hasattr(x, "input"):
            so["input"] = _mk_simobject(x.input, seedgen, models, links)
            so["input"]["output"] = so
            
        if hasattr(x, "output"):
            so["output"] = _mk_simobject(x.output, seedgen, models, links)
            so["output"]["input"] = so

        return so
        

def mk_simulation(circuit, seedgen):
    models = {}
    links = {}
    
    for m in circuit.models:
        if m not in models:
            _mk_simobject(m, seedgen, models, links)
            
    for l in circuit.links:
        if l not in links:
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
    print (mk_simulation(mc1, seedgen))
    
    