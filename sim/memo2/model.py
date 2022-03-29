class Model:           
    """
    Created on Wed Mar 23 2022
    @author: Francesco Cavarretta
       
    Abstract class representing a model archetype
    """
    
    def __init__(self, name, parent=None, children=None, **kwargs):
        """
        Initialize a model

        Parameters
        ----------
        name: model identifier
        **kwargs : parameters of the model
        """       
        
        self.name = name # each model should have a name
        self.parent = parent
        self.children = children
        

