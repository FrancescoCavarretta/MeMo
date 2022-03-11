: TITLE CACC current for bladder small DRG neuron soma model

: Author: Darshan Mandge (darshanmandge@iitb.ac.in)
: Computational Neurophysiology Lab
: Indian Institute of Technology Bombay, India 

: For details refer: 
: A biophysically detailed computational model of bladder small DRG neuron soma 
: Darshan Mandge and Rohit Manchanda, PLOS Computational Biology (2018)

NEURON {
	SUFFIX cacc
	:USEION cl READ ecl WRITE icl VALENCE -1
	NONSPECIFIC_CURRENT i
	USEION cal2 READ cal2i VALENCE 2
	RANGE i
	RANGE gbar, ninf, ntau, vhalf, sf1, EC50, hc
        RANGE ecl


        
        RANGE i_output, output
}

UNITS {
	(molar) = (1/liter)
	(mM)	= (millimolar)
	(uM)	= (micromolar)
	(S)  	= (siemens)
	(mA) 	= (milliamp)
	(mV) 	= (millivolt)
}

PARAMETER {
        gbar = 1e-6 (S/cm2)
        ntau_min=30 (ms)
        ntau_max=120 (ms)
        EC50_shift=0 (mM)
        ecl=-77 (mV)
}

ASSIGNED {
        v       (mV)
        i		(mA/cm2)



        i_output
        output


        
		ninf
		ntau 	(ms)
		cal2i	(mM)
		celsius	(degC)
		EC50 	(mM)
		hc 		(1)
}

STATE {
        n
}
 
BREAKPOINT {
        SOLVE states METHOD cnexp



        output    = n
        i_output  = gbar*output*(v-ecl)
        
        

		i = i_output
}
 
INITIAL {
		rates(v, cal2i)
		n = ninf


                
        output    = n
        i_output  = gbar*output*(v-ecl)
                
		i = i_output

}

DERIVATIVE states {  
        rates(v, cal2i)
        n' = (ninf-n)/ntau
}
 
PROCEDURE rates(v(mV), cai (mM)) { LOCAL s, z
		 
		 UNITSOFF
        :"n" CACC activation
                if (v < -20) {
                  s=1
                } else if(v > 20) {
                  s=0
                } else {
                  s = 1/(1+exp((v-1)/1))
                }
		hc   = 1.95+0.35*s
		EC50 = (3.65+1.35*s)*1e-3
		
		ninf = (1/(1+(EC50/cai)^hc))

                z = (cai-0.0038)/0.00011
                if(z > 700) {
                  s = 0
                } else {
                  s = 1/(1+exp(z))
                }
		ntau = ntau_min+(ntau_max-ntau_min)*s
}


 
UNITSON 





