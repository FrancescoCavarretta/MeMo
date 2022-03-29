import sim.memo.model as model
import sim.memo.link as link
import sim.memo.neuron as nrn
import sim.memo.spiketrain as stn
import sim.memo.distribution as distr

import sim.compiler.precompiler as precompiler
import sim.compiler as compiler
import sim.compiler.neuron as base
import sim.compiler.neuron.util.recorder as rec

import sim.memo.microcircuit as mc

import sim.memo.neuron as nrn

import sim.nwbio as nwbio

from sim.compiler.neuron.modules import neuron_modules

from neuron import h

import pandas as pd

import numpy as np


import matplotlib.pyplot as plt

import sys

lesioned_flag = '--6ohda' in sys.argv


    

class Cell:
    
  def __del__(self):
      del self.bpo_cell
      del self.cell
      del self.section
      del self.product 
      
      self.bpo_cell = self.cell = self.section = self.product = None
      
    
  __control__ = not lesioned_flag
  def load_params(self, filename):
    import numpy as np
    return sorted(np.load(filename, allow_pickle=True).tolist().items())


  def mk_cell_model(self, cellid, control=False):
    import mkcell
    import os
    
    filename = "test_model_" + ("control" if control else "lesioned") + "_edyta_test_good.npy"
    param = self.load_params(os.path.join(os.path.dirname(__file__), 'mkcell', filename))[cellid][1][0]
    etype=("control" if control else "lesioned") + "_BK_short_AP"

    return mkcell.mk_cell_model(param, etype=etype)

  def __init__(self, name, cellid=1):
    import numpy as np
    import pandas as pd
    
    self.name = name
    self.bpo_cell = self.mk_cell_model(cellid, control=Cell.__control__)
    self.cell = self.bpo_cell.icell
    self.morph_table, self.section = Cell.bpo2memo_cell(self.bpo_cell)
    self.product = { "Cell":self.section, "MorphologyTable":self.morph_table }
    
    
    
  def make(self):            
      return self.product
      

  def branch_order(sec, soma_sec):
    from neuron import h
    order = 0
    sref = h.SectionRef(sec=sec)
    while sref.sec != soma_sec:
      sref = h.SectionRef(sec=sref.parent)
      order += 1
    return order

  def bpo2memo_cell(bpo_cell):
    from neuron import h
    import pandas as pd
    
    section_collection = {}
    h.distance(sec=bpo_cell.icell.soma[0])
    tab = pd.DataFrame(columns=["type", "segment", "name", "number", "diam", "len", "dist"])
    for section_type in bpo_cell.seclist_names:
      section_collection[section_type] = {}
      if section_type != "all":
        for section in getattr(bpo_cell.icell, section_type):
          section_number = int(h.secname(sec=section).split("[")[-1].replace("]", ""))
          section_collection[section_type][section_number] = section
          for segment in section.allseg():
            tab = tab.append({ "type":section_type,
                               "segment":segment.x,
                               "name":section,
                               "number":section_number,
                               "diam":segment.diam,
                               "len":section.L / section.nseg,
                               "dist":h.distance(segment.x, sec=section),
                               "order":Cell.branch_order(section, bpo_cell.icell.soma[0])},
                             ignore_index=True)
            
    tab["segment"] = tab["segment"].astype(float)
    tab["dist"] = tab["dist"].astype(float)
    tab["len"] = tab["len"].astype(float)
    tab["number"] = tab["number"].astype(int)
    tab["weights"] = tab["len"] / tab["len"].min()
    return tab, section_collection        
          

  def get(self, target_feature=None, min_value=None, max_value=None, section_type="basal", optional_X=None):
    import pandas as pd
    
    f = self.morph_table
    if section_type:
        if type(section_type) != list:
            section_type = [ section_type ]
        _f = pd.DataFrame()
        for _st in section_type:
            _f = _f.append(f[f["type"] == _st])
        f = _f
        del _f, _st 
    
    if target_feature:
      if min_value:
        f = f[f[target_feature] >= min_value]
       
      if max_value:
        f = f[f[target_feature] < max_value]

    f = f[[ 'type', 'number', 'segment', 'weights' ]]
    
    if f.shape[0] == 0:
        return None
    
    if optional_X:
        f['weights_cdf'] = (f['weights'] / f['weights'].sum()).cumsum()
        f = f.loc[ f[f['weights_cdf'] >= optional_X].index[:1], ['type', 'number', 'segment']]
    return [self.section[x["type"]][x["number"]](x["segment"]) for k, x in f.iterrows()]



if __name__ == "__main__":
    from neuron import h
    h.load_file("nrngui.hoc")
    
    cell = Cell("VM")
    
    
##    # 200 ms increase/decrease
##    # F-I curve for variations and background
##    @neuron_modules
##    def run(tstop=100.0, filename="test.nwb", color="blue", v_init=-78.):
##      r = precompiler.precompile(mcirc, (0, 5))
##      compiler.compile(r, base)
##      
##      rr = rec.Recorder(r["models"][i2t.cell]["real_simobj"].section["somatic"][0](0.5))
##      h.load_file("stdgui.hoc")
##      h.tstop = tstop
##      h.finitialize(v_init)
##      h.run(tstop)
##      data = rr.get()
##      
##      fw = nwbio.FileWriter(filename, "thalamic_test", "thalamic_test_id")
##      cw = fw.get_cell_writer("test_cell")
##      cw.add(data[:, 0], data[:, 1])
##      fw.close()
##    
##      fr = nwbio.FileReader(filename)
##      xdata, ydata = fr.read("sim_ephys_data_0")
##      plt.plot(xdata, ydata, color=color)
##      #plt.ylim([-85,30])
##      plt.show()
##    
##    
##    run()
    
