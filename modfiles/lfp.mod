NEURON {
	SUFFIX lfp
	POINTER i_membrane
	RANGE amp, filt
	
}

PARAMETER {
  filt = 1.0
}


ASSIGNED {
        i_membrane
	amp

}

BREAKPOINT { 
	amp =   i_membrane * filt * 1e-1  

}
