/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__BK
#define _nrn_initial _nrn_initial__BK
#define nrn_cur _nrn_cur__BK
#define _nrn_current _nrn_current__BK
#define nrn_jacob _nrn_jacob__BK
#define nrn_state _nrn_state__BK
#define _net_receive _net_receive__BK 
#define rates rates__BK 
#define states states__BK 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define gbar _p[0]
#define i_output _p[1]
#define output _p[2]
#define minf _p[3]
#define mtau _p[4]
#define vhalf _p[5]
#define m _p[6]
#define ek _p[7]
#define ik _p[8]
#define cal2i _p[9]
#define q _p[10]
#define Dm _p[11]
#define v _p[12]
#define _g _p[13]
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
#define _ion_cal2i	*_ppvar[3]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_alpha(void);
 static void _hoc_beta(void);
 static void _hoc_rates(void);
 static void _hoc_sig(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_BK", _hoc_setdata,
 "alpha_BK", _hoc_alpha,
 "beta_BK", _hoc_beta,
 "rates_BK", _hoc_rates,
 "sig_BK", _hoc_sig,
 0, 0
};
#define alpha alpha_BK
#define beta beta_BK
#define sig sig_BK
 extern double alpha( _threadargsprotocomma_ double , double , double );
 extern double beta( _threadargsprotocomma_ double , double , double );
 extern double sig( _threadargsprotocomma_ double , double , double , double , double );
 /* declare global and static user variables */
#define mtau_min mtau_min_BK
 double mtau_min = 0.01;
#define q10 q10_BK
 double q10 = 2.5;
#define slope slope_BK
 double slope = 11.1;
#define shift shift_BK
 double shift = 0;
#define tau_factor tau_factor_BK
 double tau_factor = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "shift_BK", "mV",
 "tau_factor_BK", "ms",
 "slope_BK", "/mV",
 "gbar_BK", "S/cm2",
 "mtau_BK", "ms",
 "vhalf_BK", "mV",
 0,0
};
 static double delta_t = 0.01;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "shift_BK", &shift_BK,
 "tau_factor_BK", &tau_factor_BK,
 "q10_BK", &q10_BK,
 "slope_BK", &slope_BK,
 "mtau_min_BK", &mtau_min_BK,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[4]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"BK",
 "gbar_BK",
 0,
 "i_output_BK",
 "output_BK",
 "minf_BK",
 "mtau_BK",
 "vhalf_BK",
 0,
 "m_BK",
 0,
 0};
 static Symbol* _k_sym;
 static Symbol* _cal2_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 14, _prop);
 	/*initialize range parameters*/
 	gbar = 1e-06;
 	_prop->param = _p;
 	_prop->param_size = 14;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 prop_ion = need_memb(_cal2_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[3]._pval = &prop_ion->param[1]; /* cal2i */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _BK_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", 1.0);
 	ion_reg("cal2", 2.0);
 	_k_sym = hoc_lookup("k_ion");
 	_cal2_sym = hoc_lookup("cal2_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 14, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 BK /home/francesco/Desktop/MeMo/modfiles/BK.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsprotocomma_ double, double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[1], _dlist1[1];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargscomma_ v , cal2i ) ;
   Dm = ( minf - m ) / mtau ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 rates ( _threadargscomma_ v , cal2i ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / mtau )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) { {
   rates ( _threadargscomma_ v , cal2i ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / mtau)))*(- ( ( ( minf ) ) / mtau ) / ( ( ( ( - 1.0 ) ) ) / mtau ) - m) ;
   }
  return 0;
}
 
double sig ( _threadargsprotocomma_ double _lx , double _lfmax , double _lxh , double _lf0 , double _lk ) {
   double _lsig;
 _lsig = _lfmax / ( 1.0 + exp ( ( _lx - _lxh ) / _lk ) ) + _lf0 ;
   
return _lsig;
 }
 
static void _hoc_sig(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  sig ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) , *getarg(4) , *getarg(5) );
 hoc_retpushx(_r);
}
 
double alpha ( _threadargsprotocomma_ double _lv , double _lk , double _lB ) {
   double _lalpha;
 _lalpha = exp ( ( _lv - 30.0 ) / _lk ) * _lB ;
   
return _lalpha;
 }
 
static void _hoc_alpha(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  alpha ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
double beta ( _threadargsprotocomma_ double _lv , double _lk , double _lB ) {
   double _lbeta;
 if ( fabs ( ( _lv - 30.0 ) / _lk ) < 1e-5 ) {
     _lbeta = 1.0 ;
     }
   else {
     _lbeta = - 1.0 / ( exp ( - ( _lv - 30.0 ) / _lk ) - 1.0 ) * ( _lv - 30.0 ) / _lk ;
     }
   _lbeta = _lbeta * _lB ;
   
return _lbeta;
 }
 
static void _hoc_beta(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  beta ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
static int  rates ( _threadargsprotocomma_ double _lv , double _lcai ) {
   double _lca_conc_log , _lmm , _lqq , _lx0 , _lx1 , _ly0 , _ly1 , _lBa , _lBb , _la , _lb , _lvsh ;
 _lvsh = _lv + shift ;
   _lca_conc_log = log10 ( _lcai ) + 3.0 ;
   _lBa = pow( 10.0 , sig ( _threadargscomma_ _lca_conc_log , 2.53905005 , 0.78384945 , - 1.27772552 , 2.04819518 ) ) ;
   _lBb = pow( 10.0 , sig ( _threadargscomma_ _lca_conc_log , 4.07686975 , 0.87144064 , - 3.34336997 , - 0.2950530 ) ) ;
   _la = alpha ( _threadargscomma_ _lvsh , - 57.82912341 , _lBa ) ;
   _lb = beta ( _threadargscomma_ _lvsh , 26.38506155 , _lBb ) ;
   mtau = tau_factor / ( _la + _lb ) ;
   if ( mtau < mtau_min ) {
     mtau = mtau_min ;
     }
   mtau = mtau / q ;
   if ( _lca_conc_log < - 0.9 ) {
     vhalf = 152.0 ;
     }
   else if ( _lca_conc_log >= 3.2 ) {
     vhalf = - 47.7 ;
     }
   else {
     _ly0 = 152.0 ;
     _ly1 = - 47.7 ;
     _lx0 = - 0.9 ;
     _lx1 = 3.2 ;
     _lmm = ( _ly1 - _ly0 ) / ( _lx1 - _lx0 ) ;
     _lqq = - _lx0 * ( _ly1 - _ly0 ) / ( _lx1 - _lx0 ) + _ly0 ;
     vhalf = _lmm * _lca_conc_log + _lqq ;
     }
   minf = 1.0 / ( 1.0 + exp ( - ( _lvsh - vhalf ) / slope ) ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 1;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
  cal2i = _ion_cal2i;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 1; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
  cal2i = _ion_cal2i;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 3, 1);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  m = m0;
 {
   rates ( _threadargscomma_ v , cal2i ) ;
   m = minf ;
   output = m * gbar ;
   i_output = output * ( v - ek ) ;
   ik = i_output ;
   q = pow( q10 , ( ( celsius - 23.0 ) / 10.0 ) ) ;
   }
 
}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  ek = _ion_ek;
  cal2i = _ion_cal2i;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   output = m * gbar ;
   i_output = output * ( v - ek ) ;
   ik = i_output ;
   }
 _current += ik;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  ek = _ion_ek;
  cal2i = _ion_cal2i;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  ek = _ion_ek;
  cal2i = _ion_cal2i;
 {   states(_p, _ppvar, _thread, _nt);
  } }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/francesco/Desktop/MeMo/modfiles/BK.mod";
static const char* nmodl_file_text = 
  "NEURON {\n"
  "	SUFFIX BK\n"
  "	USEION k READ ek WRITE ik VALENCE 1\n"
  "	USEION cal2 READ cal2i VALENCE 2\n"
  "	RANGE gbar, minf, mtau\n"
  "        RANGE vhalf\n"
  "        GLOBAL shift\n"
  "        GLOBAL tau_factor\n"
  "\n"
  "        RANGE i_output, output\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(molar) = (1/liter)\n"
  "	(mM)	= (millimolar)\n"
  "	(uM)	= (micromolar)\n"
  "	(S)  	= (siemens)\n"
  "	(mA) 	= (milliamp)\n"
  "	(mV) 	= (millivolt)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "        gbar = 1e-6 (S/cm2)\n"
  "        shift = 0 (mV)\n"
  "        tau_factor = 1 (ms)\n"
  "        q10    = 2.5\n"
  "        slope = 11.1 (/mV)\n"
  "        mtau_min = 0.01\n"
  "        \n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "        v       (mV)\n"
  "\n"
  "        ek (mV)\n"
  "        ik (mA/cm2)\n"
  "\n"
  "        i_output\n"
  "        output\n"
  "\n"
  "\n"
  "        \n"
  "		minf\n"
  "		mtau 	(ms)\n"
  "		cal2i	(mM)\n"
  "		celsius	(degC)\n"
  "		vhalf	(mV)\n"
  "\n"
  "        q\n"
  "}\n"
  "\n"
  "STATE {\n"
  "        m \n"
  "}\n"
  " \n"
  "BREAKPOINT {\n"
  "        SOLVE states METHOD cnexp\n"
  "        output    = m*gbar\n"
  "        i_output  = output*(v-ek)\n"
  "	ik = i_output\n"
  "}\n"
  " \n"
  "INITIAL {\n"
  "		rates(v, cal2i)\n"
  "		m = minf\n"
  "                output    = m*gbar\n"
  "                i_output  = output*(v-ek)\n"
  "		ik = i_output\n"
  "                q = q10 ^ ((celsius - 23) / 10)\n"
  "\n"
  "}\n"
  "\n"
  "DERIVATIVE states {  \n"
  "        rates(v, cal2i)\n"
  "        m' = (minf-m)/mtau\n"
  "}\n"
  "\n"
  "FUNCTION sig(x, fmax, xh, f0, k) {\n"
  "  sig = fmax / ( 1 + exp( (x - xh) / k ) ) + f0\n"
  "}\n"
  "\n"
  "FUNCTION alpha(v, k, B) {\n"
  "  alpha = exp((v - 30) / k) * B\n"
  "}\n"
  "\n"
  "FUNCTION beta(v, k, B) {\n"
  "  if (fabs((v - 30)/k) < 1e-5) {\n"
  "    beta = 1\n"
  "  } else {\n"
  "    beta = -1.0 / ( exp(-(v - 30) / k) - 1) * (v - 30) / k\n"
  "  }\n"
  "  beta = beta * B\n"
  "}\n"
  "\n"
  "\n"
  "PROCEDURE rates(v(mV), cai (mM)) { LOCAL ca_conc_log, mm, qq, x0, x1, y0, y1, Ba, Bb, a, b, vsh\n"
  "              vsh = v + shift\n"
  "                                   \n"
  "              ca_conc_log = log10(cai) + 3.0            \n"
  "\n"
  "              Ba = 10 ^ sig(ca_conc_log, 2.53905005,  0.78384945, -1.27772552,  2.04819518)\n"
  "              Bb = 10 ^ sig(ca_conc_log, 4.07686975,  0.87144064, -3.34336997,  -0.2950530)\n"
  "              a  = alpha(vsh, -57.82912341, Ba)\n"
  "              b  = beta(vsh, 26.38506155, Bb)\n"
  "                                   \n"
  "              : definition of tau from the literature                              \n"
  "              mtau = tau_factor / (a + b)\n"
  "\n"
  "              if(mtau < mtau_min) {\n"
  "                mtau = mtau_min\n"
  "              }\n"
  "                                   \n"
  "              mtau = mtau / q\n"
  "                                   \n"
  "\n"
  "              : Bold line in Figure 2D\n"
  "              if (ca_conc_log < -0.9) {\n"
  "                vhalf = 152.0\n"
  "              } else if (ca_conc_log >= 3.2) {\n"
  "                vhalf = -47.7\n"
  "              } else {\n"
  "                 y0 = 152.0\n"
  "                 y1 = -47.7\n"
  "                 x0 = -0.9\n"
  "                 x1 = 3.2\n"
  "                 mm = (y1 - y0) / (x1 - x0)\n"
  "                 qq = - x0 * (y1 - y0) / (x1 - x0) + y0 \n"
  "                 vhalf = mm * ca_conc_log + qq\n"
  "              }\n"
  "              \n"
  "              minf = 1 / (1 + exp(-(vsh - vhalf)/slope))\n"
  "}\n"
  "\n"
  "\n"
  " \n"
  "UNITSON \n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
