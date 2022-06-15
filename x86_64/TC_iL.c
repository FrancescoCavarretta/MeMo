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
 
#define nrn_init _nrn_init__TC_iL
#define _nrn_initial _nrn_initial__TC_iL
#define nrn_cur _nrn_cur__TC_iL
#define _nrn_current _nrn_current__TC_iL
#define nrn_jacob _nrn_jacob__TC_iL
#define nrn_state _nrn_state__TC_iL
#define _net_receive _net_receive__TC_iL 
#define rates rates__TC_iL 
#define states states__TC_iL 
 
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
#define pcabar1 _p[0]
#define pcabar2 _p[1]
#define tau_m _p[2]
#define m_inf _p[3]
#define output _p[4]
#define i_output _p[5]
#define m _p[6]
#define cal1i _p[7]
#define cal1o _p[8]
#define cal2i _p[9]
#define cal2o _p[10]
#define Dm _p[11]
#define ical1 _p[12]
#define ical2 _p[13]
#define i_rec _p[14]
#define tcorr _p[15]
#define v _p[16]
#define _g _p[17]
#define _ion_cal1i	*_ppvar[0]._pval
#define _ion_cal1o	*_ppvar[1]._pval
#define _ion_ical1	*_ppvar[2]._pval
#define _ion_dical1dv	*_ppvar[3]._pval
#define _ion_cal2i	*_ppvar[4]._pval
#define _ion_cal2o	*_ppvar[5]._pval
#define _ion_ical2	*_ppvar[6]._pval
#define _ion_dical2dv	*_ppvar[7]._pval
 
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
 static void _hoc_ghk(void);
 static void _hoc_rates(void);
 static void _hoc_vtrap(void);
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
 "setdata_TC_iL", _hoc_setdata,
 "efun_TC_iL", _hoc_efun,
 "ghk_TC_iL", _hoc_ghk,
 "rates_TC_iL", _hoc_rates,
 "vtrap_TC_iL", _hoc_vtrap,
 0, 0
};
#define efun efun_TC_iL
#define ghk ghk_TC_iL
#define vtrap vtrap_TC_iL
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double vtrap( _threadargsprotocomma_ double , double );
 /* declare global and static user variables */
#define beta beta_TC_iL
 double beta = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "pcabar1_TC_iL", "cm/s",
 "pcabar2_TC_iL", "cm/s",
 "tau_m_TC_iL", "ms",
 0,0
};
 static double delta_t = 1;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "beta_TC_iL", &beta_TC_iL,
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
 
#define _cvode_ieq _ppvar[8]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"TC_iL",
 "pcabar1_TC_iL",
 "pcabar2_TC_iL",
 0,
 "tau_m_TC_iL",
 "m_inf_TC_iL",
 "output_TC_iL",
 "i_output_TC_iL",
 0,
 "m_TC_iL",
 0,
 0};
 static Symbol* _cal1_sym;
 static Symbol* _cal2_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 18, _prop);
 	/*initialize range parameters*/
 	pcabar1 = 0.0001;
 	pcabar2 = 0.0001;
 	_prop->param = _p;
 	_prop->param_size = 18;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 9, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_cal1_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cal1i */
 	_ppvar[1]._pval = &prop_ion->param[2]; /* cal1o */
 	_ppvar[2]._pval = &prop_ion->param[3]; /* ical1 */
 	_ppvar[3]._pval = &prop_ion->param[4]; /* _ion_dical1dv */
 prop_ion = need_memb(_cal2_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[4]._pval = &prop_ion->param[1]; /* cal2i */
 	_ppvar[5]._pval = &prop_ion->param[2]; /* cal2o */
 	_ppvar[6]._pval = &prop_ion->param[3]; /* ical2 */
 	_ppvar[7]._pval = &prop_ion->param[4]; /* _ion_dical2dv */
 
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

 void _TC_iL_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("cal1", -10000.);
 	ion_reg("cal2", -10000.);
 	_cal1_sym = hoc_lookup("cal1_ion");
 	_cal2_sym = hoc_lookup("cal2_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 18, 9);
  hoc_register_dparam_semantics(_mechtype, 0, "cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 TC_iL /home/francesco/Desktop/MeMo/modfiles/TC_iL.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 
#define FARADAY _nrnunit_FARADAY[_nrnunit_use_legacy_]
static double _nrnunit_FARADAY[2] = {0x1.78e555060882cp+16, 96485.3}; /* 96485.3321233100141 */
 static double R = 8.314;
static int _reset;
static char *modelname = "high threshold calcium current (L-current)";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[1], _dlist1[1];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargscomma_ v ) ;
   Dm = ( m_inf - m ) / tau_m ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 rates ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_m )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) { {
   rates ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_m)))*(- ( ( ( m_inf ) ) / tau_m ) / ( ( ( ( - 1.0 ) ) ) / tau_m ) - m) ;
   }
  return 0;
}
 
double ghk ( _threadargsprotocomma_ double _lv , double _lci , double _lco ) {
   double _lghk;
 double _lz , _leci , _leco ;
 _lz = _lv * ( .001 ) * 2.0 * FARADAY / ( R * ( celsius + 273.15 ) ) ;
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
 
static int  rates ( _threadargsprotocomma_ double _lv ) {
   double _la , _lb ;
 _la = 1.6 / ( 1.0 + exp ( - 0.072 * ( _lv - 5.0 ) ) ) ;
   _lb = 0.02 * vtrap ( _threadargscomma_ - ( _lv - 1.31 ) , 5.36 ) ;
   tau_m = 1.0 / ( _la + _lb ) / tcorr ;
   m_inf = 1.0 / ( 1.0 + exp ( ( _lv + 10.0 ) / - 10.0 ) ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double vtrap ( _threadargsprotocomma_ double _lx , double _lc ) {
   double _lvtrap;
 if ( fabs ( _lx / _lc ) < 1e-6 ) {
     _lvtrap = _lc + _lx / 2.0 ;
     }
   else {
     _lvtrap = _lx / ( 1.0 - exp ( - _lx / _lc ) ) ;
     }
   
return _lvtrap;
 }
 
static void _hoc_vtrap(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  vtrap ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
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
  cal1i = _ion_cal1i;
  cal1o = _ion_cal1o;
  cal2i = _ion_cal2i;
  cal2o = _ion_cal2o;
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
  cal1i = _ion_cal1i;
  cal1o = _ion_cal1o;
  cal2i = _ion_cal2i;
  cal2o = _ion_cal2o;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_cal1_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_cal1_sym, _ppvar, 1, 2);
   nrn_update_ion_pointer(_cal1_sym, _ppvar, 2, 3);
   nrn_update_ion_pointer(_cal1_sym, _ppvar, 3, 4);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 4, 1);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 5, 2);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 6, 3);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 7, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  m = m0;
 {
   tcorr = pow( 3.0 , ( ( celsius - 23.5 ) / 10.0 ) ) ;
   rates ( _threadargscomma_ v ) ;
   m = m_inf ;
   output = ( pcabar1 + pcabar2 ) * m * m ;
   ical1 = pcabar1 * m * m * ghk ( _threadargscomma_ v , cal1i , cal1o ) ;
   ical2 = pcabar2 * m * m * ghk ( _threadargscomma_ v , cal2i , cal2o ) ;
   i_output = ical1 + ical2 ;
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
  cal1i = _ion_cal1i;
  cal1o = _ion_cal1o;
  cal2i = _ion_cal2i;
  cal2o = _ion_cal2o;
 initmodel(_p, _ppvar, _thread, _nt);
  }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   output = ( pcabar1 + pcabar2 ) * m * m ;
   ical1 = pcabar1 * m * m * ghk ( _threadargscomma_ v , cal1i , cal1o ) ;
   ical2 = pcabar2 * m * m * ghk ( _threadargscomma_ v , cal2i , cal2o ) ;
   i_output = ical1 + ical2 ;
   }
 _current += ical1;
 _current += ical2;

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
  cal1i = _ion_cal1i;
  cal1o = _ion_cal1o;
  cal2i = _ion_cal2i;
  cal2o = _ion_cal2o;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dical2;
 double _dical1;
  _dical1 = ical1;
  _dical2 = ical2;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dical1dv += (_dical1 - ical1)/.001 ;
  _ion_dical2dv += (_dical2 - ical2)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ical1 += ical1 ;
  _ion_ical2 += ical2 ;
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
  cal1i = _ion_cal1i;
  cal1o = _ion_cal1o;
  cal2i = _ion_cal2i;
  cal2o = _ion_cal2o;
 {   states(_p, _ppvar, _thread, _nt);
  }  }}

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
static const char* nmodl_filename = "/home/francesco/Desktop/MeMo/modfiles/TC_iL.mod";
static const char* nmodl_file_text = 
  "TITLE high threshold calcium current (L-current)\n"
  "\n"
  ": 2019: From ModelDB, accession: 3808\n"
  ": Based on the model by McCormick & Huguenard, J Neurophysiol, 1992\n"
  ": and errata in https://huguenardlab.stanford.edu/reprints/Errata_thalamic_cell_models.pdf\n"
  ": Modified cai by Elisabetta Iavarone @ Blue Brain Project\n"
  ": See PARAMETER section for references \n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX TC_iL\n"
  "	USEION cal1 READ cal1i,cal1o WRITE ical1\n"
  "        USEION cal2 READ cal2i,cal2o WRITE ical2\n"
  "        :USEION cal3 READ cal3i,cal3o WRITE ical3\n"
  "        :RANGE pcabar1, pcabar2, pcabar3, m_inf, tau_m\n"
  "        RANGE pcabar1, pcabar2, m_inf, tau_m\n"
  "        GLOBAL beta\n"
  "\n"
  "\n"
  "\n"
  "        RANGE output, i_output\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA)	= (milliamp)\n"
  "	(mV)	= (millivolt)\n"
  "	(molar) = (1/liter)\n"
  "	(mM)	= (millimolar)\n"
  "        FARADAY = (faraday) (coulomb)\n"
  "        R       = 8.314 (volt-coul/degC)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	v			(mV)\n"
  "	celsius			(degC)\n"
  "        dt              	(ms)\n"
  "	cal1i  = 0.5E-4    	(mM) : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "	cal1o  = 2		(mM)\n"
  "	cal2i  = 0.5E-4    	(mM) : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "	cal2o  = 2		(mM)\n"
  "	:cal3i  = 0.5E-4    	(mM) : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "	:cal3o  = 2		(mM)\n"
  "	pcabar1= 1e-4	        (cm/s)\n"
  "	pcabar2= 1e-4	        (cm/s)\n"
  "	:pcabar3= 1e-4	        (cm/s)\n"
  "        beta  = 1\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ical1		(mA/cm2)\n"
  "	ical2		(mA/cm2)\n"
  "	:ical3		(mA/cm2)\n"
  "	i_rec		(mA/cm2)	\n"
  "	tau_m		(ms)\n"
  "	m_inf \n"
  "	tcorr\n"
  "\n"
  "\n"
  "\n"
  "        output\n"
  "        i_output\n"
  "}\n"
  "\n"
  "BREAKPOINT { \n"
  "	SOLVE states METHOD cnexp\n"
  "\n"
  "\n"
  "        :output   = (pcabar1+pcabar2+pcabar3)*m*m\n"
  "\n"
  "        output   = (pcabar1+pcabar2)*m*m\n"
  "\n"
  "        \n"
  "	ical1 = pcabar1 * m*m * ghk(v,cal1i,cal1o)\n"
  "	ical2 = pcabar2 * m*m * ghk(v,cal2i,cal2o)\n"
  "	:ical3 = pcabar3 * m*m * ghk(v,cal3i,cal3o)\n"
  "	\n"
  "        :i_output =ical1+ical2+ical3\n"
  "        i_output =ical1+ical2\n"
  "}\n"
  "\n"
  "DERIVATIVE states {\n"
  "       rates(v)\n"
  "\n"
  "       m'= (m_inf-m) / tau_m \n"
  "}\n"
  "  \n"
  "INITIAL {\n"
  "	tcorr = 3^((celsius-23.5)/10)\n"
  "	rates(v)\n"
  "	m = m_inf\n"
  "\n"
  "\n"
  "\n"
  "        :output   = (pcabar1+pcabar2+pcabar3)*m*m\n"
  "        output   = (pcabar1+pcabar2)*m*m\n"
  "        \n"
  "	ical1 = pcabar1 * m*m * ghk(v,cal1i,cal1o)\n"
  "	ical2 = pcabar2 * m*m * ghk(v,cal2i,cal2o)\n"
  "	:ical3 = pcabar3 * m*m * ghk(v,cal3i,cal3o)\n"
  "	\n"
  "        :i_output =ical1+ical2+ical3\n"
  "        i_output =ical1+ical2\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "FUNCTION ghk( v(mV), ci(mM), co(mM))  (millicoul/cm3) {\n"
  "        LOCAL z, eci, eco\n"
  "        z = v * (.001) * 2 *FARADAY / (R*(celsius+273.15))\n"
  "	eco = co*efun(z)\n"
  "	eci = ci*efun(-z)\n"
  "	:high cao charge moves inward\n"
  "	:negative potential charge moves inward\n"
  "	ghk = (.001)*2*FARADAY*(eci - eco)\n"
  "}\n"
  "\n"
  "FUNCTION efun(z) {\n"
  "	 if (fabs(z) < 1e-4) {\n"
  "	    efun = 1 - z/2\n"
  "	 }else{\n"
  "	    efun = z/(exp(z) - 1)\n"
  "         }\n"
  "}\n"
  "\n"
  "PROCEDURE rates(v(mV)) { LOCAL a,b\n"
  "	a = 1.6 / (1+ exp(-0.072*(v-5)))\n"
  "	b = 0.02 * vtrap( -(v-1.31), 5.36)\n"
  "\n"
  "	tau_m = 1/(a+b) / tcorr\n"
  "	m_inf = 1/(1+exp((v+10)/-10))\n"
  "}\n"
  "\n"
  "FUNCTION vtrap(x,c) { \n"
  "	: Traps for 0 in denominator of rate equations\n"
  "        if (fabs(x/c) < 1e-6) {\n"
  "          vtrap = c + x/2 }\n"
  "        else {\n"
  "          vtrap = x / (1-exp(-x/c)) }\n"
  "}\n"
  "UNITSON\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
