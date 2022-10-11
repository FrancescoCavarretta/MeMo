#!/usr/bin/env python
# coding: utf-8

def mk_cell_model(params, recipes=None, etype="control", cvode_active=True):
  import os
  import json
  
  from . import CellEvalSetup
  from bluepyopt.ephys.simulators import NrnSimulator
  from bluepyopt.ephys import models

  if recipes is None:
    with open(os.path.join(os.path.dirname(__file__), '.', 'config/recipes.json')) as f:
      recipe = json.load(f)
  c = CellEvalSetup.template.create(recipe, etype)
  c.freeze(params)
  c.instantiate(sim=NrnSimulator(cvode_active=cvode_active))
  return c


if __name__ == "__main__":
  import numpy
  halloffame = numpy.load("control.npy", allow_pickle=True).tolist()
  i = 0
  key = sorted(list(halloffame))[0]
  c = mk_cell_model(halloffame[key][0])
