#!/usr/bin/env python
# coding: utf-8

def param_dict(param_array, etype="control_BK_short_AP"):
  import numpy as np
  from . import CellEvalSetup
  return CellEvalSetup.evaluator.create(etype).param_dict(np.array(param_array).astype(float))

def mk_cell_model(param_array, recipe=None, etype="control_BK_short_AP", cvode_active=True):
  from . import CellEvalSetup
  from bluepyopt.ephys.simulators import NrnSimulator
  import os
  import json

  if recipe is None:
    with open(os.path.join(os.path.dirname(__file__), '.', 'config/recipes.json')) as f:
      recipe = json.load(f)  
      
  c = CellEvalSetup.template.create(recipe, etype)
  c.freeze(param_dict(param_array, etype=etype))
  c.instantiate(sim=NrnSimulator(cvode_active=cvode_active))
  return c



