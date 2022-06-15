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
 
#define nrn_init _nrn_init__TC_HH
#define _nrn_initial _nrn_initial__TC_HH
#define nrn_cur _nrn_cur__TC_HH
#define _nrn_current _nrn_current__TC_HH
#define nrn_jacob _nrn_jacob__TC_HH
#define nrn_state _nrn_state__TC_HH
#define _net_receive _net_receive__TC_HH 
#define evaluate_fct evaluate_fct__TC_HH 
#define states states__TC_HH 
 
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
#define gna_max _p[0]
#define gnap_max _p[1]
#define gk_max _p[2]
#define vtraubna _p[3]
#define vtraubk _p[4]
#define ina _p[5]
#define ik _p[6]
#define m_inf _p[7]
#define h_inf _p[8]
#define mp_inf _p[9]
#define hp_inf _p[10]
#define hsp_inf _p[11]
#define n_inf _p[12]
#define tau_m _p[13]
#define tau_h _p[14]
#define tau_n _p[15]
#define tau_mp _p[16]
#define tau_hp _p[17]
#define tau_hsp _p[18]
#define output_nat _p[19]
#define output_nap _p[20]
#define output_k _p[21]
#define i_output_nat _p[22]
#define i_output_nap _p[23]
#define i_output_na _p[24]
#define i_output_k _p[25]
#define m _p[26]
#define h _p[27]
#define n _p[28]
#define mp _p[29]
#define hp _p[30]
#define hsp _p[31]
#define Dm _p[32]
#define Dh _p[33]
#define Dn _p[34]
#define Dmp _p[35]
#define Dhp _p[36]
#define Dhsp _p[37]
#define ena _p[38]
#define ek _p[39]
#define tcorr _p[40]
#define v _p[41]
#define _g _p[42]
#define _ion_ena	*_ppvar[0]._pval
#define _ion_ina	*_ppvar[1]._pval
#define _ion_dinadv	*_ppvar[2]._pval
#define _ion_ek	*_ppvar[3]._pval
#define _ion_ik	*_ppvar[4]._pval
#define _ion_dikdv	*_ppvar[5]._pval
 
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
 static void _hoc_evaluate_fct(void);
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
 "setdata_TC_HH", _hoc_setdata,
 "evaluate_fct_TC_HH", _hoc_evaluate_fct,
 0, 0
};
 /* declare global and static user variables */
#define shift shift_TC_HH
 double shift = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gna_max_TC_HH", "S/cm2",
 "gnap_max_TC_HH", "S/cm2",
 "gk_max_TC_HH", "S/cm2",
 "ina_TC_HH", "mA/cm2",
 "ik_TC_HH", "mA/cm2",
 0,0
};
 static double delta_t = 1;
 static double hsp0 = 0;
 static double hp0 = 0;
 static double h0 = 0;
 static double mp0 = 0;
 static double m0 = 0;
 static double n0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "shift_TC_HH", &shift_TC_HH,
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
 
#define _cvode_ieq _ppvar[6]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"TC_HH",
 "gna_max_TC_HH",
 "gnap_max_TC_HH",
 "gk_max_TC_HH",
 "vtraubna_TC_HH",
 "vtraubk_TC_HH",
 0,
 "ina_TC_HH",
 "ik_TC_HH",
 "m_inf_TC_HH",
 "h_inf_TC_HH",
 "mp_inf_TC_HH",
 "hp_inf_TC_HH",
 "hsp_inf_TC_HH",
 "n_inf_TC_HH",
 "tau_m_TC_HH",
 "tau_h_TC_HH",
 "tau_n_TC_HH",
 "tau_mp_TC_HH",
 "tau_hp_TC_HH",
 "tau_hsp_TC_HH",
 "output_nat_TC_HH",
 "output_nap_TC_HH",
 "output_k_TC_HH",
 "i_output_nat_TC_HH",
 "i_output_nap_TC_HH",
 "i_output_na_TC_HH",
 "i_output_k_TC_HH",
 0,
 "m_TC_HH",
 "h_TC_HH",
 "n_TC_HH",
 "mp_TC_HH",
 "hp_TC_HH",
 "hsp_TC_HH",
 0,
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 43, _prop);
 	/*initialize range parameters*/
 	gna_max = 0.1;
 	gnap_max = 0.1;
 	gk_max = 0.1;
 	vtraubna = -55.5;
 	vtraubk = -55.5;
 	_prop->param = _p;
 	_prop->param_size = 43;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 7, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
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

 void _TC_HH_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 43, 7);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 TC_HH /home/francesco/Desktop/MeMo/modfiles/TC_HH.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "Hippocampal HH channels";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int evaluate_fct(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[6], _dlist1[6];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   evaluate_fct ( _threadargscomma_ v ) ;
   Dm = ( m_inf - m ) / tau_m ;
   Dh = ( h_inf - h ) / tau_h ;
   Dmp = ( mp_inf - mp ) / tau_mp ;
   Dhp = ( hp_inf - hp ) / tau_hp ;
   Dhsp = ( hsp_inf - hsp ) / tau_hsp ;
   Dn = ( n_inf - n ) / tau_n ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 evaluate_fct ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_m )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_h )) ;
 Dmp = Dmp  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_mp )) ;
 Dhp = Dhp  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_hp )) ;
 Dhsp = Dhsp  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_hsp )) ;
 Dn = Dn  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tau_n )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) { {
   evaluate_fct ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_m)))*(- ( ( ( m_inf ) ) / tau_m ) / ( ( ( ( - 1.0 ) ) ) / tau_m ) - m) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_h)))*(- ( ( ( h_inf ) ) / tau_h ) / ( ( ( ( - 1.0 ) ) ) / tau_h ) - h) ;
    mp = mp + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_mp)))*(- ( ( ( mp_inf ) ) / tau_mp ) / ( ( ( ( - 1.0 ) ) ) / tau_mp ) - mp) ;
    hp = hp + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_hp)))*(- ( ( ( hp_inf ) ) / tau_hp ) / ( ( ( ( - 1.0 ) ) ) / tau_hp ) - hp) ;
    hsp = hsp + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_hsp)))*(- ( ( ( hsp_inf ) ) / tau_hsp ) / ( ( ( ( - 1.0 ) ) ) / tau_hsp ) - hsp) ;
    n = n + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tau_n)))*(- ( ( ( n_inf ) ) / tau_n ) / ( ( ( ( - 1.0 ) ) ) / tau_n ) - n) ;
   }
  return 0;
}
 
static int  evaluate_fct ( _threadargsprotocomma_ double _lv ) {
   double _la , _lb , _lv2 , _lv3 , _lv4 ;
 _lv2 = _lv - vtraubna + shift ;
   _lv3 = _lv - vtraubk + shift ;
   _lv4 = _lv - vtraubna + 15.0 + shift ;
   if ( _lv2  == 13.0  || _lv2  == 40.0  || _lv3  == 15.0  || _lv4  == 13.0  || _lv4  == 40.0 ) {
     _lv = _lv + 0.0001 ;
     }
   _la = 0.32 * ( 13.0 - _lv2 ) / ( exp ( ( 13.0 - _lv2 ) / 4.0 ) - 1.0 ) ;
   _lb = 0.28 * ( _lv2 - 40.0 ) / ( exp ( ( _lv2 - 40.0 ) / 5.0 ) - 1.0 ) ;
   tau_m = 1.0 / ( _la + _lb ) / tcorr ;
   m_inf = _la / ( _la + _lb ) ;
   _la = 0.128 * exp ( ( 17.0 - _lv2 ) / 18.0 ) ;
   _lb = 4.0 / ( 1.0 + exp ( ( 40.0 - _lv2 ) / 5.0 ) ) ;
   tau_h = 1.0 / ( _la + _lb ) / tcorr ;
   h_inf = _la / ( _la + _lb ) ;
   _la = 0.032 * ( 15.0 - _lv3 ) / ( exp ( ( 15.0 - _lv3 ) / 5.0 ) - 1.0 ) ;
   _lb = 0.5 * exp ( ( 10.0 - _lv3 ) / 40.0 ) ;
   tau_n = 1.0 / ( _la + _lb ) / tcorr ;
   n_inf = _la / ( _la + _lb ) ;
   if ( _lv4  == 13.0  || _lv4  == 40.0  || _lv4  == 15.0 ) {
     _lv = _lv + 0.0001 ;
     }
   _la = 0.32 * ( 13.0 - _lv4 ) / ( exp ( ( 13.0 - _lv4 ) / ( 1.5 * 4.0 ) ) - 1.0 ) ;
   _lb = 0.28 * ( _lv4 - 40.0 ) / ( exp ( ( _lv4 - 40.0 ) / ( 1.5 * 5.0 ) ) - 1.0 ) ;
   tau_mp = 1.0 / ( _la + _lb ) / tcorr ;
   mp_inf = _la / ( _la + _lb ) ;
   _la = 0.128 * exp ( ( 17.0 - _lv4 ) / 18.0 ) ;
   _lb = 4.0 / ( 1.0 + exp ( ( 40.0 - _lv4 ) / 5.0 ) ) ;
   tau_hp = 1.0 / ( _la + _lb ) / tcorr ;
   hp_inf = _la / ( _la + _lb ) ;
   _la = 0.128 * exp ( ( 17.0 - _lv4 ) / 18.0 ) ;
   _lb = 4.0 / ( 1.0 + exp ( ( 40.0 - _lv4 ) / 5.0 ) ) ;
   tau_hsp = 1.0 / ( _la + _lb ) / tcorr ;
   hsp_inf = _la / ( _la + _lb ) ;
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
 
static int _ode_count(int _type){ return 6;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ena = _ion_ena;
  ek = _ion_ek;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
   }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 6; ++_i) {
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
  ena = _ion_ena;
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_k_sym, _ppvar, 3, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 4, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 5, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  hsp = hsp0;
  hp = hp0;
  h = h0;
  mp = mp0;
  m = m0;
  n = n0;
 {
   tcorr = pow( 3.0 , ( ( celsius - 36.0 ) / 10.0 ) ) ;
   evaluate_fct ( _threadargscomma_ v ) ;
   m = m_inf ;
   h = h_inf ;
   mp = mp_inf ;
   hp = hp_inf ;
   hsp = hsp_inf ;
   n = n_inf ;
   output_nat = gna_max * m * m * m * h ;
   output_nap = gnap_max * mp * mp * mp * hp ;
   output_k = gk_max * n * n * n * n ;
   i_output_nat = output_nat * ( v - ena ) ;
   i_output_nap = output_nap * ( v - ena ) ;
   i_output_na = i_output_nat + i_output_nap ;
   i_output_k = output_k * ( v - ek ) ;
   ina = i_output_na ;
   ik = i_output_k ;
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
  ena = _ion_ena;
  ek = _ion_ek;
 initmodel(_p, _ppvar, _thread, _nt);
  }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   output_nat = gna_max * m * m * m * h ;
   output_nap = gnap_max * mp * mp * mp * hp ;
   output_k = gk_max * n * n * n * n ;
   i_output_nat = output_nat * ( v - ena ) ;
   i_output_nap = output_nap * ( v - ena ) ;
   i_output_na = i_output_nat + i_output_nap ;
   i_output_k = output_k * ( v - ek ) ;
   ina = i_output_na ;
   ik = i_output_k ;
   }
 _current += ina;
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
  ena = _ion_ena;
  ek = _ion_ek;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
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
  ena = _ion_ena;
  ek = _ion_ek;
 {   states(_p, _ppvar, _thread, _nt);
  }  }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
 _slist1[1] = &(h) - _p;  _dlist1[1] = &(Dh) - _p;
 _slist1[2] = &(mp) - _p;  _dlist1[2] = &(Dmp) - _p;
 _slist1[3] = &(hp) - _p;  _dlist1[3] = &(Dhp) - _p;
 _slist1[4] = &(hsp) - _p;  _dlist1[4] = &(Dhsp) - _p;
 _slist1[5] = &(n) - _p;  _dlist1[5] = &(Dn) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/francesco/Desktop/MeMo/modfiles/TC_HH.mod";
static const char* nmodl_file_text = 
  "TITLE Hippocampal HH channels\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX TC_HH\n"
  "	USEION na READ ena WRITE ina\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gna_max, gk_max, gnap_max, vtraubna, vtraubk\n"
  "	RANGE m_inf, h_inf, n_inf, mp_inf, hp_inf, hsp_inf\n"
  "	RANGE tau_m, tau_h, tau_n, tau_mp, tau_hp, tau_hsp\n"
  "	RANGE ina, ik\n"
  "\n"
  "        : ------ analysis ------\n"
  "        RANGE output_nat, output_nap, output_k, i_output_nat, i_output_nap, i_output_na, i_output_k\n"
  "        \n"
  "        GLOBAL shift\n"
  "}\n"
  "\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	(S)  = (siemens)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	gna_max	= 1.0e-1 	(S/cm2) \n"
  "	gnap_max	= 1.0e-1 	(S/cm2) \n"
  "	gk_max	= 1.0e-1 	(S/cm2) \n"
  "\n"
  "	celsius         (degC)\n"
  "	dt              (ms)\n"
  "	v               (mV)\n"
  "	vtraubna = -55.5   : Average of original value and Amarillo et al., J Neurophysiol 112:393-410, 2014\n"
  "        vtraubk  = -55.5   : Average of original value and Amarillo et al., J Neurophysiol 112:393-410, 2014\n"
  "        shift    = 0\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m h n mp hp hsp\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ina	(mA/cm2)\n"
  "	ik	(mA/cm2)\n"
  "	ena	(mV)\n"
  "	ek	(mV)\n"
  "	m_inf\n"
  "	h_inf\n"
  "	mp_inf\n"
  "	hp_inf\n"
  "	hsp_inf\n"
  "	n_inf\n"
  "	tau_m\n"
  "	tau_h\n"
  "	tau_n\n"
  "	tau_mp\n"
  "	tau_hp\n"
  "	tau_hsp\n"
  "	tcorr\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "        output_nat\n"
  "        output_nap\n"
  "        output_k\n"
  "        i_output_nat\n"
  "        i_output_nap\n"
  "        i_output_na\n"
  "        i_output_k\n"
  "}\n"
  "\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD cnexp\n"
  "\n"
  "        output_nat = gna_max  * m*m*m*h\n"
  "        output_nap = gnap_max * mp*mp*mp*hp : mp*mp*mp*(0.04*hp+0.96*hsp)\n"
  "        output_k   = gk_max   * n*n*n*n \n"
  "        i_output_nat  = output_nat*(v - ena)\n"
  "        i_output_nap  = output_nap*(v - ena)\n"
  "        i_output_na   = i_output_nat + i_output_nap\n"
  "        i_output_k    = output_k * (v - ek)\n"
  "        \n"
  "	ina   =  i_output_na :gna_max * m*m*m*h * (v - ena) + gnap_max * (mp*mp*mp*(0.04*hp + 0.96*hsp)) * (v - ena)\n"
  "	ik    = i_output_k   :gk_max  * n*n*n*n * (v - ek)\n"
  "}\n"
  "\n"
  "\n"
  "DERIVATIVE states {   : exact Hodgkin-Huxley equations\n"
  "	evaluate_fct(v)\n"
  "	m' = (m_inf - m) / tau_m\n"
  "	h' = (h_inf - h) / tau_h\n"
  "	mp' = (mp_inf - mp) / tau_mp\n"
  "	hp' = (hp_inf - hp) / tau_hp\n"
  "	hsp' = (hsp_inf - hsp) / tau_hsp\n"
  "	n' = (n_inf - n) / tau_n\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "UNITSOFF\n"
  "INITIAL {\n"
  "	tcorr = 3.0 ^ ((celsius-36)/ 10 )\n"
  "        evaluate_fct(v)\n"
  "	m = m_inf\n"
  "	h = h_inf\n"
  "	mp = mp_inf\n"
  "	hp = hp_inf\n"
  "	hsp = hsp_inf\n"
  "	n = n_inf\n"
  "\n"
  "        output_nat = gna_max  * m*m*m*h\n"
  "        output_nap = gnap_max * mp*mp*mp*hp    : mp*mp*mp*(0.04*hp+0.96*hsp)\n"
  "        output_k   = gk_max   * n*n*n*n \n"
  "        i_output_nat  = output_nat *(v - ena)\n"
  "        i_output_nap  = output_nap *(v - ena)\n"
  "        i_output_na   = i_output_nat + i_output_nap\n"
  "        i_output_k    = output_k * (v - ek)\n"
  "        \n"
  "	ina   =  i_output_na  :gna_max * m*m*m*h * (v - ena) + gnap_max * (mp*mp*mp*hp) * (v - ena) : * (mp*mp*mp*(0.04*hp + 0.96*hsp)) * (v - ena)\n"
  "	ik    =  i_output_k   :gk_max  * n*n*n*n * (v - ek)\n"
  "}\n"
  "\n"
  "PROCEDURE evaluate_fct(v(mV)) { LOCAL a,b,v2, v3, v4\n"
  "\n"
  "	v2 = v - vtraubna + shift : convert to traub convention\n"
  "	v3 = v - vtraubk + shift  : EI: shift only K\n"
  "	v4 = v - vtraubna + 15 + shift: convert to traub convention\n"
  "                                \n"
  "	if(v2 == 13 || v2 == 40 || v3 == 15 || v4 == 13 || v4 == 40){\n"
  "    	v = v+0.0001\n"
  "        }\n"
  "\n"
  "	a = 0.32 * (13-v2) / ( exp((13-v2)/4) - 1)\n"
  "	b = 0.28 * (v2-40) / ( exp((v2-40)/5) - 1)\n"
  "	tau_m = 1 / (a + b) / tcorr\n"
  "	m_inf = a / (a + b)\n"
  "\n"
  "	a = 0.128 * exp((17-v2)/18)\n"
  "	b = 4 / ( 1 + exp((40-v2)/5) )\n"
  "	tau_h = 1 / (a + b) / tcorr\n"
  "	h_inf = a / (a + b)\n"
  "\n"
  "\n"
  "	a = 0.032 * (15-v3) / ( exp((15-v3)/5) - 1)\n"
  "	b = 0.5 * exp((10-v3)/40)\n"
  "	tau_n = 1 / (a + b) / tcorr\n"
  "	n_inf = a / (a + b)\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "	if(v4 == 13 || v4 == 40 || v4 == 15 ){\n"
  "          v = v+0.0001\n"
  "        }\n"
  "\n"
  "	a = 0.32 * (13-v4) / ( exp((13-v4)/(1.5*4)) - 1) :*6\n"
  "	b = 0.28 * (v4-40) / ( exp((v4-40)/(1.5*5)) - 1) :*6\n"
  "	tau_mp = 1 / (a + b) / tcorr\n"
  "	mp_inf = a / (a + b)\n"
  "\n"
  "                                \n"
  "        a = 0.128 * exp((17-v4)/18) \n"
  "        b = 4 / ( 1 + exp((40-v4)/5) )\n"
  "	tau_hp = 1 / (a + b) / tcorr\n"
  "        hp_inf = a / (a + b)\n"
  "\n"
  "                                \n"
  "        a = 0.128 * exp((17-v4)/18) :/15\n"
  "        b = 4 / ( 1 + exp((40-v4)/5) ) :/15\n"
  "	tau_hsp = 1 / (a + b) / tcorr\n"
  "        hsp_inf = a / (a + b)\n"
  "                                \n"
  "}\n"
  "\n"
  "UNITSON\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
