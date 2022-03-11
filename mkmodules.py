def mk_mod_files():
  import os
  os.system("cp mkcell/mechanisms/*.mod modfiles")
  os.system("cp sim/compiler/neuron/mod/*.mod modfiles")
  os.system("nrnivmodl modfiles")
  os.system("rm -r modfiles")
