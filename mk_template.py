
 
def mk_template(baseline_firing_rate, behav_delta_rate, tinit, tstop, behav_tinit, behav_tstop, behav_invl, dt, filter_name):
  import numpy as np
  
  t = np.linspace(0.0, tstop, num=int(tstop / dt + 1) )
  base_r = np.full(t.size, baseline_firing_rate, dtype=float)

  if type(filter_name) == tuple:
    filter_name, filter_param = filter_name
    
  if filter_name == 'double_exp':
    behav_tau1, behav_tau2 = filter_param
    t_max = np.log(behav_tau1 / behav_tau2) * (behav_tau1 * behav_tau2) / (behav_tau1 - behav_tau2)
    behav_r_max = ( -np.exp(t_max / -behav_tau1) + np.exp(t_max / -behav_tau2) ) 
    behav_r = behav_delta_rate * ( -np.exp(t / -behav_tau1) + np.exp(t / -behav_tau2) ) / behav_r_max
    del t_max, behav_r_max, behav_tau1, behav_tau2
  elif filter_name == 'gaussian':
    behav_mu, behav_sig, n = filter_param
    behav_r = behav_delta_rate * np.exp(-np.power((t - behav_mu) / behav_sig, n))
    del behav_mu, behav_sig, n 
    


  bt = behav_tinit
  while bt < behav_tstop:
    idx = np.argwhere(t >= bt)[0][0]
    base_r[idx:] += behav_r[:(base_r.size - idx)]
      
    
    bt += behav_invl
    
  return t, base_r



if __name__ == '__main__':
  import matplotlib.pyplot as plt
  import numpy as np
  plt.plot(*mk_template(15.0, -15.0, 0.0, 16000.0, 6000.0, 16000.0, 5000.0, 1.5, ('double_exp', (10.0, 150.0))), label='MOD')
  plt.plot(*mk_template(30.0, -15.0, 0.0, 16000.0, 6000.0 - 35.0, 16000.0, 5000.0, 1.5, ('gaussian', (60.0, 30.0, 4))), label='DRV')
  
  plt.xlim([6000-40.0, 6000+100.0])
  plt.ylim([-35, 10])
  plt.legend()
  plt.show()


  t, r = mk_template(15.0, -15.0, 0.0, 16000.0, 6000.0, 16000.0, 5000.0, 1.5, ('double_exp', (10.0, 300.0)))
  np.save('mod_template.npy', {'time':t, 'rate':r}, allow_pickle=True)
  t, r = mk_template(30.0, -25.0, 0.0, 16000.0, 6000.0, 16000.0, 5000.0, 1.5, ('double_exp', (10.0, 300.0)))
  np.save('drv_template.npy', {'time':t, 'rate':r}, allow_pickle=True)
