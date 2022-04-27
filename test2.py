import mkcell

import numpy
halloffame = sorted(list(numpy.load("mkcell/test_model_control_edyta_test_good.npy", allow_pickle=True).tolist().items()))
print (mkcell.param_dict(halloffame[0][1][0]))
