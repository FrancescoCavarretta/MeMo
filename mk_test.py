
if __name__ == '__main__':
    from parameters import Parameters
    import numpy as np
    gsyn = np.load('gsyn.old.npy', allow_pickle=True).tolist()
    par = Parameters(np.load('mkcell/hof_3sd_good.npy', allow_pickle=True).tolist(), 'test.npy')
    par.add(ntrial=1, g_mod=gsyn['CX']*0.5)
    par.close()
