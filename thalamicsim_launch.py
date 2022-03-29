if __name__ == '__main__':
    import os
    import ipyparallel as ipp
    n_mod_ctl = 346
    
    
    params = []
    
    for pr in ["", "--6ohda"]:
        
        for p_var_mod in [ -0.2, -0.1, 0.0, 0.1, 0.2 ]:
            n_mod = int(round((1+p_var_mod) * n_mod_ctl))

            for n_rtn_fiber_factor in [ 0, 2, 4, 6 ]:
                    n_rtn = int(round(n_rtn_fiber_factor * 8.5 / 17 * 7))
                    
                    for n_bg_fiber_factor in [ 0, 1, 2, 3, 4, 5 ]:
                        n_bg = int(round(n_bg_fiber_factor * 8.5))
                        
                        for p_driver in [ 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3 ]:
                            n_drv = int(round(p_driver * n_mod_ctl))
                            
                            for g_drv in [ 0.0033, 0.0122 ]:
                        
                                for i in range(10):
                                    for j in range(10):
                                        filename = 'output-cellid=%d-seed=%d-tstop=10s-n_drv=%d-n_mod=%d-n_bg=%d-n_rtn=%d-g_drv=%g' % (i, j, n_drv, n_mod, n_bg, n_rtn, g_drv)
                                        if len(pr):
                                            filename += '-6ohda'
                                        filename += '.npy'
                                        cmd = f'python3 thalamicsim.py {pr} --cellid {i} --seed {j} --tstop 10000 --filename {filename}'
                                        cmd += f' --drv_n={n_drv} --mod_n={n_mod} --bg_n={n_bg} --rtn_n={n_rtn} --drv_g={g_drv}'
                                        
                                        params.append(cmd)

    
    
    # create client & views
    rc = ipp.Client(profile=os.getenv('IPYTHON_PROFILE'))
    dv = rc[:]
    v = rc.load_balanced_view()
    amr = v.map(os.system, params, ordered=False)
    for i, r in enumerate(amr):
      print("slept", i, r)

    rc.wait()
