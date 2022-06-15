
 
def mk_template(baseline_firing_rate, behav_delta_rate, behav_tau1, behav_tau2, tinit, tstop, behav_tinit, behav_tstop, behav_invl, dt):
  import numpy as np
  
  t = np.linspace(0.0, tstop, num=int(tstop / dt + 1) )
  base_r = np.full(t.size, baseline_firing_rate, dtype=float)

  t_max = np.log(behav_tau1 / behav_tau2) * (behav_tau1 * behav_tau2) / (behav_tau1 - behav_tau2)
  behav_r_max = ( -np.exp(t_max / -behav_tau1) + np.exp(t_max / -behav_tau2) ) 
  behav_r = behav_delta_rate * ( -np.exp(t / -behav_tau1) + np.exp(t / -behav_tau2) ) / behav_r_max


  bt = behav_tinit
  while bt < behav_tstop:
    idx = np.argwhere(t >= bt)[0][0]
    base_r[idx:] += behav_r[:(base_r.size - idx)]
      
    
    bt += behav_invl
    
  return t, base_r



if __name__ == '__main__':
  import matplotlib.pyplot as plt
  plt.plot(*mk_template(50.0, -30.0, 100.0, 1000.0, 0.0, 16000.0, 6000.0, 16000.0, 5000.0, 1.5))
  plt.plot(*mk_template(50.0, -30.0, 200.0, 1000.0, 0.0, 16000.0, 6000.0, 16000.0, 5000.0, 1.5))
  plt.plot(*mk_template(50.0, -30.0, 500.0, 750.0, 0.0, 16000.0, 6000.0, 16000.0, 5000.0, 1.5))
  plt.show()
