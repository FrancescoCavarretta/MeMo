class Cell:
  
  def __del__(self):
      del self.bpo_cell
      del self.cell
      del self.section
      del self.product 
      
      self.bpo_cell = self.cell = self.section = self.product = None
    
  
  def load_params(self, filename):
    import numpy as np
    return sorted(np.load(filename, allow_pickle=True).tolist().items())


  def mk_cell_model(self, cellid, control):
    import mkcell
    import os

    param = self.load_params(os.path.join(os.path.dirname(__file__), 'mkcell', "hof_3sd_good_2nd.npy"))

    # select etype
    etype = "control" if control else "lesioned"

    # filter the etypes
    param = [ p for p in param if p[0][0] == etype ][cellid][1]['parameter']

    return mkcell.mk_cell_model(param, etype=etype)

  def __init__(self, name, cellid=0, lesioned_flag=False):
      self.name = name
      self.cellid = cellid
      self.product = None
      self.lesioned_flag = lesioned_flag
      

  def make(self):
    import numpy as np
    import pandas as pd

    if self.product is None:
      print ('cellid', self.cellid, 'lesioned_flag', self.lesioned_flag)
      self.bpo_cell = self.mk_cell_model(self.cellid, control=not self.lesioned_flag)
      self.cell = self.bpo_cell.icell
      self.morph_table, self.section = Cell.bpo2memo_cell(self.bpo_cell)
      self.product = { "Cell":self.section, "MorphologyTable":self.morph_table }
                
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
    import numpy as np
    
    section_collection = {}
    h.distance(sec=bpo_cell.icell.soma[0])
    tab = pd.DataFrame()
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
                               "len":segment.area() / (segment.diam * np.pi),
                               "dist":h.distance(segment.x, sec=section),
                               "order":Cell.branch_order(section, bpo_cell.icell.soma[0]),
                               "area":segment.area()},
                             ignore_index=True)
    tab = tab[tab.area > 0]
    tab["segment"] = tab["segment"].astype(float)
    tab["dist"] = tab["dist"].astype(float)
    tab["len"] = tab["len"].astype(float)
    tab["number"] = tab["number"].astype(int)
    tab["weights"] = tab["len"]
    return tab, section_collection        
          

  def get(self, target_feature=None, min_value=None, max_value=None, section_type="basal", optional_X=None, target_feature_distribution=None):
    import pandas as pd
    
    f = self.morph_table.copy()
        
    if section_type:
        if type(section_type) != list:
            section_type = [ section_type ]
            
        f = f[f.type.isin(section_type)]
        
    
    if target_feature:
      if min_value:
        f = f[f[target_feature] >= min_value]
       
      if max_value:
        f = f[f[target_feature] < max_value]
    
    if f.shape[0] == 0:
        return None
    
    if optional_X:
    
      if target_feature_distribution is None:
        f['weights_cdf'] = f['weights'].cumsum() / f['weights'].sum()
      else:
        f['weights_cdf'] = f[target_feature_distribution].cumsum() / f[target_feature_distribution].sum()
        
      f = f[f['weights_cdf'] >= optional_X].iloc[[0], :]

    return [self.section[x["type"]][x["number"]](x["segment"]) for k, x in f.iterrows()]


if __name__ == '__main__':
  c = Cell('Test')
  c.make()
  c.product['MorphologyTable'].to_csv('../analysis/density/morphology_table.csv')
  
