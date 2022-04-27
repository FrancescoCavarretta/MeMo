#!/usr/bin/env python
# coding: utf-8

def param_dict(param_array, recipes=None, etype="control_BK_short_AP"):
  import os
  import json
  import numpy as np
  
  from . import CellEvalSetup

  if recipes is None:
    with open(os.path.join(os.path.dirname(__file__), '.', 'config/recipes.json')) as f:
      recipe = json.load(f)
  return CellEvalSetup.evaluator.create(etype).param_dict(np.array(param_array).astype(float))

def mk_cell_model(param_array, recipes=None, etype="control_BK_short_AP", cvode_active=True):
  from . import CellEvalSetup
  from bluepyopt.ephys.simulators import NrnSimulator
      
  c = CellEvalSetup.template.create(recipe, etype)
  c.freeze(param_dict(param_array, recipes=recipes, etype=etype))
  c.instantiate(sim=NrnSimulator(cvode_active=cvode_active))
  return c



