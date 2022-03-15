_mod_file_list = []
_mod_dest_dir = "./modfiles"


def register_modules(dirname):
  '''
    Add a directory containing mod files which should be compiled

    dirname: directory name
  '''
  
  import os
  import queue
  global _mod_file_list
  
  if not os.path.exists(dirname):
    # if the directory do not even exist, do not add it, just shot a warning
    raise Warning(f"Directory {dirname} does not exist")
  else:
    qdir = queue.Queue()
    qdir.put(dirname)
    # check the subdirectories, if required
    while not qdir.empty():
      cur_dirname = qdir.get()
      if os.path.isdir(cur_dirname):
        # if it is a directory, add the subdirectories, including files
        for x in os.listdir(cur_dirname):
          qdir.put(os.path.join(cur_dirname, x))
          
      elif os.path.splitext(cur_dirname)[1].lower() == ".mod":
          # check the ext. and add if it is a mod
          _mod_file_list.append(cur_dirname)
          
      
  
def neuron_modules(func):
  def _func():
    """
    This decorator compile the mod files, execute the function, then remove the modfiles
    """
    import os
    import shutil
    global _mod_file_list
    import uuid
    import neuron
    
    # generate a directory that does not exist
    mod_dirname = str(uuid.uuid4())
    while os.path.exists(mod_dirname):
      mod_dirname = str(uuid.uuid4())
      
    register_modules(os.getcwd()) # add modfiles in the directory

    # copy files to a local directory
    try:
      os.mkdir(mod_dirname) 
      for x in _mod_file_list:
        shutil.copy(x, mod_dirname)
        
      os.system(f"nrnivmodl {mod_dirname}")
      neuron.load_mechanisms(os.getcwd()) # load neuron mechanisms
      
      func() # run
      
    except:
      pass
    finally:
      shutil.rmtree(mod_dirname) # remove modfiles
      shutil.rmtree("x86_64") # remove compiled files

  return _func
