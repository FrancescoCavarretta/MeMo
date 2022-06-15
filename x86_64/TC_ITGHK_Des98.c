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
 
#define nrn_init _nrn_init__TC_iT_Des98
#define _nrn_initial _nrn_initial__TC_iT_Des98
#define nrn_cur _nrn_cur__TC_iT_Des98
#define _nrn_current _nrn_current__TC_iT_Des98
#define nrn_jacob _nrn_jacob__TC_iT_Des98
#define nrn_state _nrn_state__TC_iT_Des98
#define _net_receive _net_receive__TC_iT_Des98 
#define castate castate__TC_iT_Des98 
#define evaluate_fct evaluate_fct__TC_iT_Des98 
 
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
#define pcabar _p[0]
#define m_inf _p[1]
#define tau_m _p[2]
#define h_inf _p[3]
#define tau_h _p[4]
#define output _p[5]
#define i_output _p[6]
#define m _p[7]
#define h _p[8]
#define cati _p[9]
#define cato _p[10]
#define Dm _p[11]
#define Dh _p[12]
#define icat _p[13]
#define phi_m _p[14]
#define phi_h _p[15]
#define v _p[16]
#define _g _p[17]
#define _ion_cati	*_ppvar[0]._pval
#define _ion_cato	*_ppvar[1]._pval
#define _ion_icat	*_ppvar[2]._pval
#define _ion_dicatdv	*_ppvar[3]._pval
 
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
 static void _hoc_efun(void);
 static void _hoc_evaluate_fct(void);
 static void _hoc_ghk(void);
 static void _hoc_nongat(void);
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
 "setdata_TC_iT_Des98", _hoc_setdata,
 "efun_TC_iT_Des98", _hoc_efun,
 "evaluate_fct_TC_iT_Des98", _hoc_evaluate_fct,
 "ghk_TC_iT_Des98", _hoc_ghk,
 "nongat_TC_iT_Des98", _hoc_nongat,
 0, 0
};
#define efun efun_TC_iT_Des98
#define ghk ghk_TC_iT_Des98
#define nongat nongat_TC_iT_Des98
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double nongat( _threadargsprotocomma_ double , double , double );
 /* declare global and static user variables */
#define actshift actshift_TC_iT_Des98
 double actshift = 0;
#define kh kh_TC_iT_Des98
 double kh = 4;
#define km km_TC_iT_Des98
 double km = 6.2;
#define qh qh_TC_iT_Des98
 double qh = 2.5;
#define qm qm_TC_iT_Des98
 double qm = 2.5;
#define shift shift_TC_iT_Des98
 double shift = 2;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "shift_TC_iT_Des98", "mV",
 "actshift_TC_iT_Des98", "mV",
 "pcabar_TC_iT_Des98", "cm/s",
 "tau_m_TC_iT_Des98", "ms",
 "tau_h_TC_iT_Des98", "ms",
 0,0
};
 static double delta_t = 1;
 static double h0 = 0;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "shift_TC_iT_Des98", &shift_TC_iT_Des98,
 "actshift_TC_iT_Des98", &actshift_TC_iT_Des98,
 "qm_TC_iT_Des98", &qm_TC_iT_Des98,
 "qh_TC_iT_Des98", &qh_TC_iT_Des98,
 "km_TC_iT_Des98", &km_TC_iT_Des98,
 "kh_TC_iT_Des98", &kh_TC_iT_Des98,
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
"TC_iT_Des98",
 "pcabar_TC_iT_Des98",
 0,
 "m_inf_TC_iT_Des98",
 "tau_m_TC_iT_Des98",
 "h_inf_TC_iT_Des98",
 "tau_h_TC_iT_Des98",
 "output_TC_iT_Des98",
 "i_output_TC_iT_Des98",
 0,
 "m_TC_iT_Des98",
 "h_TC_iT_Des98",
 0,
 0};
 static Symbol* _cat_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 18, _prop);
 	/*initialize range parameters*/
 	pcabar = 0.0002;
 	_prop->param = _p;
 	_prop->param_size = 18;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_cat_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cati */
 	_ppvar[1]._pval = &prop_ion->param[2]; /* cato */
 	_ppvar[2]._pval = &prop_ion->param[3]; /* icat */
 	_ppvar[3]._pval = &prop_ion->param[4]; /* _ion_dicatdv */
 
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

 void _TC_ITGHK_Des98_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("cat", -10000.);
 	_cat_sym = hoc_lookup("cat_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 18, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "cat_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "cat_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "cat_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cat_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 TC_iT_Des98 /home/francesco/Desktop/MeMo/modfiles/TC_ITGHK_Des98.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 
#define FARADAY _nrnunit_FARADAY[_nrnunit_use_legacy_]
static double _nrnunit_FARADAY[2] = {0x1.78e555060882cp+16, 96485.3}; /* 96485.3321233100141 */
 
#define R _nrnunit_R[_nrnunit_use_legacy_]
static double _nrnunit_R[2] = {0x1.0a1013e8990bep+3, 8.3145}; /* 8.3144626181532395 */
static int _reset;
static char *modelname = "Low threshold calcium current";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int evaluate_fct(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int castate(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   evaluate_fct ( _threadargscomma_ v ) ;
   Dm = ( m_inf - m ) / tau_m ;
   Dh = ( h_inf - h ) / tau_h ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 evaluate_fct ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_m )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_h )) ;
  return 0;
}
 /*END CVODE*/
 static int castate (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) { {
   evaluate_fct ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_m)))*(- ( ( ( m_inf ) ) / tau_m ) / ( ( ( ( - 1.0 ) ) ) / tau_m ) - m) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_h)))*(- ( ( ( h_inf ) ) / tau_h ) / ( ( ( ( - 1.0 ) ) ) / tau_h ) - h) ;
   }
  return 0;
}
 
static int  evaluate_fct ( _threadargsprotocomma_ double _lv ) {
   m_inf = 1.0 / ( 1.0 + exp ( - ( _lv + shift + actshift + 57.0 ) / km ) ) ;
   h_inf = 1.0 / ( 1.0 + exp ( ( _lv + shift + 81.0 ) / kh ) ) ;
   tau_m = ( 0.612 + 1.0 / ( exp ( - ( _lv + shift + actshift + 132.0 ) / 16.7 ) + exp ( ( _lv + shift + actshift + 16.8 ) / 18.2 ) ) ) / phi_m ;
   if ( ( _lv + shift ) < - 80.0 ) {
     tau_h = exp ( ( _lv + shift + 467.0 ) / 66.6 ) / phi_h ;
     }
   else {
     tau_h = ( 28.0 + exp ( - ( _lv + shift + 22.0 ) / 10.5 ) ) / phi_h ;
     }
    return 0; }
 
static void _hoc_evaluate_fct(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 evaluate_fct ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double ghk ( _threadargsprotocomma_ double _lv , double _lci , double _lco ) {
   double _lghk;
 double _lz , _leci , _leco ;
 _lz = ( 1e-3 ) * 2.0 * FARADAY * _lv / ( R * ( celsius + 273.15 ) ) ;
   _leco = _lco * efun ( _threadargscomma_ _lz ) ;
   _leci = _lci * efun ( _threadargscomma_ - _lz ) ;
   _lghk = ( .001 ) * 2.0 * FARADAY * ( _leci - _leco ) ;
   
return _lghk;
 }
 
static void _hoc_ghk(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  ghk ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
double efun ( _threadargsprotocomma_ double _lz ) {
   double _lefun;
 if ( fabs ( _lz ) < 1e-4 ) {
     _lefun = 1.0 - _lz / 2.0 ;
     }
   else {
     _lefun = _lz / ( exp ( _lz ) - 1.0 ) ;
     }
   
return _lefun;
 }
 
static void _hoc_efun(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  efun ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double nongat ( _threadargsprotocomma_ double _lv , double _lcati , double _lcato ) {
   double _lnongat;
 _lnongat = pcabar * ghk ( _threadargscomma_ _lv , _lcati , _lcato ) ;
   
return _lnongat;
 }
 
static void _hoc_nongat(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  nongat ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cati = _ion_cati;
  cato = _ion_cato;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
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
  cati = _ion_cati;
  cato = _ion_cato;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_cat_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_cat_sym, _ppvar, 1, 2);
   nrn_update_ion_pointer(_cat_sym, _ppvar, 2, 3);
   nrn_update_ion_pointer(_cat_sym, _ppvar, 3, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  h = h0;
  m = m0;
 {
   phi_m = pow( qm , ( ( celsius - 24.0 ) / 10.0 ) ) ;
   phi_h = pow( qh , ( ( celsius - 24.0 ) / 10.0 ) ) ;
   evaluate_fct ( _threadargscomma_ v ) ;
   m = m_inf ;
   h = h_inf ;
   output = pcabar * m * m * h ;
   i_output = output * ghk ( _threadargscomma_ v , cati , cato ) ;
   icat = i_output ;
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
  cati = _ion_cati;
  cato = _ion_cato;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   output = pcabar * m * m * h ;
   i_output = output * ghk ( _threadargscomma_ v , cati , cato ) ;
   icat = i_output ;
   }
 _current += icat;

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
  cati = _ion_cati;
  cato = _ion_cato;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dicat;
  _dicat = icat;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dicatdv += (_dicat - icat)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_icat += icat ;
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
  cati = _ion_cati;
  cato = _ion_cato;
 {   castate(_p, _ppvar, _thread, _nt);
  } }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
 _slist1[1] = &(h) - _p;  _dlist1[1] = &(Dh) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/francesco/Desktop/MeMo/modfiles/TC_ITGHK_Des98.mod";
static const char* nmodl_file_text = 
  "TITLE Low threshold calcium current\n"
  ":\n"
  ":   Ca++ current responsible for low threshold spikes (LTS)\n"
  ":   Differential equations\n"
  ":\n"
  ":   Model of Huguenard & McCormick, J Neurophysiol 68: 1373-1383, 1992.\n"
  ":   The kinetics is described by Goldman-Hodgkin-Katz equations,\n"
  ":   using a m2h format, according to the voltage-clamp data\n"
  ":   (whole cell patch clamp) of Huguenard & Prince, J. Neurosci. \n"
  ":   12: 3804-3817, 1992.\n"
  ":\n"
  ":   This model is described in detail in:\n"
  ":   Destexhe A, Neubig M, Ulrich D and Huguenard JR.  \n"
  ":   Dendritic low-threshold calcium currents in thalamic relay cells.  \n"
  ":   Journal of Neuroscience 18: 3574-3588, 1998.\n"
  ":   (a postscript version of this paper, including figures, is available on\n"
  ":   the Internet at http://cns.fmed.ulaval.ca)\n"
  ":\n"
  ":    - shift parameter for screening charge\n"
  ":    - empirical correction for contamination by inactivation (Huguenard)\n"
  ":    - GHK equations\n"
  ":\n"
  ":\n"
  ":   Written by Alain Destexhe, Laval University, 1995\n"
  ":\n"
  "\n"
  ": 2019: From ModelDB, accession no. 279\n"
  ": Modified qm and qh by Elisabetta Iavarone @ Blue Brain Project\n"
  ": See PARAMETER section for references\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX TC_iT_Des98\n"
  "	USEION cat READ cati, cato WRITE icat\n"
  "	RANGE pcabar, m_inf, tau_m, h_inf, tau_h\n"
  "	GLOBAL qm, qh, km, kh, shift, actshift\n"
  "\n"
  "\n"
  "\n"
  "        RANGE output, i_output\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(molar) = (1/liter)\n"
  "	(mV) =	(millivolt)\n"
  "	(mA) =	(milliamp)\n"
  "	(mM) =	(millimolar)\n"
  "\n"
  "	FARADAY = (faraday) (coulomb)\n"
  "	R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	v		(mV)\n"
  "	:celsius	= 36	(degC)\n"
  "	celsius 	(degC)  : EI\n"
  "	pcabar	=.2e-3	(cm/s)	: Maximum Permeability\n"
  "	shift	= 2 	(mV)	: corresponds to 2mM ext Ca++\n"
  "	actshift = 0 	(mV)	: shift of activation curve (towards hyperpol)\n"
  "	cati	= 2.4e-4 (mM)	: adjusted for eca2=120 mV\n"
  "	cato	= 2	(mM)\n"
  "	qm      = 2.5		: Amarillo et al., J Neurophysiol, 2014\n"
  "	qh      = 2.5           : Amarillo et al., J Neurophysiol, 2014\n"
  "        km      = 6.2\n"
  "        kh      = 4.0\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m h\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	icat	(mA/cm2)\n"
  "	m_inf\n"
  "	tau_m	(ms)\n"
  "	h_inf\n"
  "	tau_h	(ms)\n"
  "	phi_m\n"
  "	phi_h\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "        output\n"
  "        i_output\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE castate METHOD cnexp\n"
  "\n"
  "        \n"
  "        output   = pcabar*m*m*h\n"
  "        i_output = output*ghk(v, cati, cato)\n"
  "\n"
  "        \n"
  "	icat     = i_output\n"
  "}\n"
  "\n"
  "DERIVATIVE castate {\n"
  "	evaluate_fct(v)\n"
  "\n"
  "	m' = (m_inf - m) / tau_m\n"
  "	h' = (h_inf - h) / tau_h\n"
  "}\n"
  "\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "INITIAL {\n"
  "	phi_m = qm ^ ((celsius-24)/10)\n"
  "	phi_h = qh ^ ((celsius-24)/10)\n"
  "\n"
  "	evaluate_fct(v)\n"
  "\n"
  "	m = m_inf\n"
  "	h = h_inf\n"
  "\n"
  "\n"
  "        output   = pcabar*m*m*h\n"
  "        i_output = output*ghk(v, cati, cato)\n"
  "\n"
  "\n"
  "        icat     = i_output\n"
  "}\n"
  "\n"
  "PROCEDURE evaluate_fct(v(mV)) {\n"
  ":\n"
  ":   The kinetic functions are taken as described in the model of \n"
  ":   Huguenard & McCormick, and corresponds to a temperature of 23-25 deg.\n"
  ":   Transformation to 36 deg assuming Q10 of 5 and 3 for m and h\n"
  ":   (as in Coulter et al., J Physiol 414: 587, 1989).\n"
  ":\n"
  ":   The activation functions were estimated by John Huguenard.\n"
  ":   The V_1/2 were of -57 and -81 in the vclamp simulations, \n"
  ":   and -60 and -84 in the current clamp simulations.\n"
  ":\n"
  ":   The activation function were empirically corrected in order to account\n"
  ":   for the contamination of inactivation.  Therefore the simulations \n"
  ":   using these values reproduce more closely the voltage clamp experiments.\n"
  ":   (cfr. Huguenard & McCormick, J Neurophysiol, 1992).\n"
  ":\n"
  "\n"
  "	m_inf = 1.0 / ( 1 + exp(-(v+shift+actshift+57)/km) )\n"
  "	h_inf = 1.0 / ( 1 + exp((v+shift+81)/kh) )\n"
  "\n"
  "	tau_m = ( 0.612 + 1.0 / ( exp(-(v+shift+actshift+132)/16.7) + exp((v+shift+actshift+16.8)/18.2) ) ) / phi_m\n"
  "	if( (v+shift) < -80) {\n"
  "		tau_h = exp((v+shift+467)/66.6) / phi_h\n"
  "	} else {\n"
  "		tau_h = ( 28 + exp(-(v+shift+22)/10.5) ) / phi_h\n"
  "	}\n"
  "\n"
  "	: EI compare with tau_h on ModelDB, no. 3817\n"
  "}\n"
  "\n"
  "FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) {\n"
  "	LOCAL z, eci, eco\n"
  "	z = (1e-3)*2*FARADAY*v/(R*(celsius+273.15))\n"
  "	eco = co*efun(z)\n"
  "	eci = ci*efun(-z)\n"
  "	:high cao charge moves inward\n"
  "	:negative potential charge moves inward\n"
  "	ghk = (.001)*2*FARADAY*(eci - eco)\n"
  "}\n"
  "\n"
  "FUNCTION efun(z) {\n"
  "	if (fabs(z) < 1e-4) {\n"
  "		efun = 1 - z/2\n"
  "	}else{\n"
  "		efun = z/(exp(z) - 1)\n"
  "	}\n"
  "}\n"
  "FUNCTION nongat(v,cati,cato) {	: non gated current\n"
  "	nongat = pcabar * ghk(v, cati, cato)\n"
  "}\n"
  "UNITSON\n"
  ;
#endif
