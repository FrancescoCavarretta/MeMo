TITLE simple NMDA receptors

: Hines combined AMPA and NMDA and spike dependent plasticity

: Modified from the original AMPA.mod, M.Migliore Jan 2003
: A weight of 0.0035 gives a peak conductance of 1nS in 0Mg

COMMENT
-----------------------------------------------------------------------------

	Simple model for glutamate AMPA receptors
	=========================================

  - FIRST-ORDER KINETICS, FIT TO WHOLE-CELL RECORDINGS

    Whole-cell recorded postsynaptic currents mediated by AMPA/Kainate
    receptors (Xiang et al., J. Neurophysiol. 71: 2552-2556, 1994) were used
    to estimate the parameters of the present model; the fit was performed
    using a simplex algorithm (see Destexhe et al., J. Computational Neurosci.
    1: 195-230, 1994).

  - SHORT PULSES OF TRANSMITTER (0.3 ms, 0.5 mM)

    The simplified model was obtained from a detailed synaptic model that 
    included the release of transmitter in adjacent terminals, its lateral 
    diffusion and uptake, and its binding on postsynaptic receptors (Destexhe
    and Sejnowski, 1995).  Short pulses of transmitter with first-order
    kinetics were found to be the best fast alternative to represent the more
    detailed models.

  - ANALYTIC EXPRESSION

    The first-order model can be solved analytically, leading to a very fast
    mechanism for simulating synapses, since no differential equation must be
    solved (see references below).



References

   Destexhe, A., Mainen, Z.F. and Sejnowski, T.J.  An efficient method for
   computing synaptic conductances based on a kinetic model of receptor binding
   Neural Computation 6: 10-14, 1994.  

   Destexhe, A., Mainen, Z.F. and Sejnowski, T.J. Synthesis of models for
   excitable membranes, synaptic transmission and neuromodulation using a 
   common kinetic formalism, Journal of Computational Neuroscience 1: 
   195-230, 1994.


-----------------------------------------------------------------------------
ENDCOMMENT



NEURON {
	POINT_PROCESS MeMo_AmpaNmda
        
	NONSPECIFIC_CURRENT i
        
        RANGE mg, inmda, iampa, gnmda, gampa, gnmda_max, gampa_max, Ron, Roff, Rnmda_max, Rnmda, synon, r0, e
        
	RANGE Cdur, Alpha, Beta, Rinf, Rtau, ampatau

        RANGE q10_ampa, temp0_ampa, q10_nmda, temp0_nmda, tadj_ampa, tadj_nmda, ampatau_in
        
        RANGE gnmda, gampa, i, inmda, iampa, g
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(umho) = (micromho)
	(mM) = (milli/liter)
}

PARAMETER {

        
	Cdur	= 1		(ms)	: transmitter duration (rising phase)
        
	Alpha	= 0.35		(/ms)	: forward (binding) rate
	Beta	= 0.035		(/ms)	: backward (unbinding) rate
        
	e	= 0	(mV)		: reversal potential
	mg	= 1    (mM)		: external magnesium concentration

        
        gnmda_max = 0.0 (umho)
        

        
        gampa_max = 0.0 (umho)
	ampatau = 3 (ms)

        
        q10_ampa = 2.1
        temp0_ampa = 27
        q10_nmda = 1.75
        temp0_nmda = 27        

}


ASSIGNED {
	v		(mV)		: postsynaptic voltage
	i 		(nA)		: total current = iampa+inmda
        
	inmda 		(nA)		: current = gnmda*(v - E)
	iampa 		(nA)		: current = gampa*(v - E)

        
	Rinf				: steady state channels open
	Rtau		(ms)		: time constant of channel binding
	synon
        Rnmda
        Rnmda_max

        r0

        tadj_ampa
        tadj_nmda
        ampatau_in
}

STATE {
       Ron
       Roff

       gampa 		
       gnmda 	
       g		
}

INITIAL {
	PROTECT Rinf = Alpha / (Alpha + Beta)
	PROTECT Rtau = 1 / (Alpha + Beta)
        r0 = 0
	synon = 0
	gampa = 0
        gnmda = 0
        
        g = 0
        
        Rnmda = 0
        Rnmda_max = exp(-3*Cdur/Rtau) * Rinf
        tadj_ampa=q10_ampa^((celsius-temp0_ampa)/10)
        tadj_nmda=q10_nmda^((celsius-temp0_nmda)/10)
        
        ampatau_in=ampatau/tadj_ampa
}

BREAKPOINT {
	SOLVE release METHOD cnexp
        Rnmda = mgblock(v)*(Ron + Roff) / Rnmda_max 
	gnmda = Rnmda*gnmda_max 
        
	inmda = gnmda * (v - e)
	iampa = gampa * (v - e)
	g = gnmda + gampa
	i = iampa + inmda
}

DERIVATIVE release {
	Ron' = (synon*Rinf - Ron)/Rtau :/ tadj_nmda
	Roff' = -Beta*Roff :/ tadj_nmda
        
	gampa' = -gampa/ampatau_in
}

: following supports both saturation from single input and
: summation from multiple inputs
: if spike occurs during CDur then new off time is t + CDur
: ie. transmitter concatenates but does not summate
: Note: automatic initialization of all reference args to 0 except first


FUNCTION mgblock(v(mV)) {
	TABLE 
	DEPEND mg
	FROM -140 TO 80 WITH 1000

	: from Jahr & Stevens

	mgblock = 1 / (1 + exp(0.062 (/mV) * -v) * (mg / 3.57 (mM)))
}


NET_RECEIVE(weight, s, w, tlast (ms), r0, t0 (ms)) {

	INITIAL {
		r0 = 0
		t0 = -1e9 (ms)
	}
        
	: flag is an implicit argument of NET_RECEIVE and  normally 0
        if (flag == 0) { : a spike, so turn on if not already in a Cdur pulse

                         
                
                         
		r0 = r0*exp(-Beta*(t - t0))
		t0 = t
                         
		synon = synon + 1
		Ron = Ron + r0
		Roff = Roff - r0
                         
		: come again in Cdur with flag = current value of w+1
		net_send(Cdur, 1)

                gampa = gampa + gampa_max       : ampa conductance         
        } else { : turn off what was added Cdur ago
		r0 = Rinf + (r0 - Rinf) * exp(-(t - t0)/Rtau)
		t0 = t
               
		synon = synon - 1
		Ron = Ron - r0
		Roff = Roff + r0
	}
}







