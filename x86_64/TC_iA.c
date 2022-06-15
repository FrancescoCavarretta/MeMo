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
 
#define nrn_init _nrn_init__TC_iA
#define _nrn_initial _nrn_initial__TC_iA
#define nrn_cur _nrn_cur__TC_iA
#define _nrn_current _nrn_current__TC_iA
#define nrn_jacob _nrn_jacob__TC_iA
#define nrn_state _nrn_state__TC_iA
#define _net_receive _net_receive__TC_iA 
#define settables settables__TC_iA 
#define states states__TC_iA 
 
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
#define gk_max _p[0]
#define shift _p[1]
#define ik _p[2]
#define taoh1 _p[3]
#define taoh2 _p[4]
#define taom _p[5]
#define output _p[6]
#define i_output _p[7]
#define m1 _p[8]
#define m2 _p[9]
#define h1 _p[10]
#define h2 _p[11]
#define ek _p[12]
#define m1inf _p[13]
#define m2inf _p[14]
#define hinf _p[15]
#define tadj _p[16]
#define Dm1 _p[17]
#define Dm2 _p[18]
#define Dh1 _p[19]
#define Dh2 _p[20]
#define v _p[21]
#define _g _p[22]
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
 
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
 static void _hoc_settables(void);
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
 "setdata_TC_iA", _hoc_setdata,
 "settables_TC_iA", _hoc_settables,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gk_max_TC_iA", "S/cm2",
 "shift_TC_iA", "mV",
 "ik_TC_iA", "mA/cm2",
 "taoh1_TC_iA", "ms",
 "taoh2_TC_iA", "ms",
 "taom_TC_iA", "ms",
 0,0
};
 static double delta_t = 0.01;
 static double h20 = 0;
 static double h10 = 0;
 static double m20 = 0;
 static double m10 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
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
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"TC_iA",
 "gk_max_TC_iA",
 "shift_TC_iA",
 0,
 "ik_TC_iA",
 "taoh1_TC_iA",
 "taoh2_TC_iA",
 "taom_TC_iA",
 "output_TC_iA",
 "i_output_TC_iA",
 0,
 "m1_TC_iA",
 "m2_TC_iA",
 "h1_TC_iA",
 "h2_TC_iA",
 0,
 0};
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 23, _prop);
 	/*initialize range parameters*/
 	gk_max = 0.0055;
 	shift = 0;
 	_prop->param = _p;
 	_prop->param_size = 23;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
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

 void _TC_iA_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 23, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 TC_iA /home/francesco/Desktop/MeMo/modfiles/TC_iA.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "Fast Transient Potassium Current IA";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int settables(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[4], _dlist1[4];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   settables ( _threadargscomma_ v ) ;
   Dm1 = ( m1inf - m1 ) / taom ;
   Dm2 = ( m2inf - m2 ) / taom ;
   Dh1 = ( hinf - h1 ) / taoh1 ;
   Dh2 = ( hinf - h2 ) / taoh2 ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 settables ( _threadargscomma_ v ) ;
 Dm1 = Dm1  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taom )) ;
 Dm2 = Dm2  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taom )) ;
 Dh1 = Dh1  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taoh1 )) ;
 Dh2 = Dh2  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taoh2 )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) { {
   settables ( _threadargscomma_ v ) ;
    m1 = m1 + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taom)))*(- ( ( ( m1inf ) ) / taom ) / ( ( ( ( - 1.0 ) ) ) / taom ) - m1) ;
    m2 = m2 + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taom)))*(- ( ( ( m2inf ) ) / taom ) / ( ( ( ( - 1.0 ) ) ) / taom ) - m2) ;
    h1 = h1 + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taoh1)))*(- ( ( ( hinf ) ) / taoh1 ) / ( ( ( ( - 1.0 ) ) ) / taoh1 ) - h1) ;
    h2 = h2 + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taoh2)))*(- ( ( ( hinf ) ) / taoh2 ) / ( ( ( ( - 1.0 ) ) ) / taoh2 ) - h2) ;
   }
  return 0;
}
 
static int  settables ( _threadargsprotocomma_ double _lv ) {
   double _ltaodef ;
 m1inf = 1.0 / ( 1.0 + exp ( - ( _lv + 60.0 + shift ) / 8.5 ) ) ;
   m2inf = 1.0 / ( 1.0 + exp ( - ( _lv + 36.0 + shift ) / 20.0 ) ) ;
   hinf = 1.0 / ( 1.0 + exp ( ( _lv + 78.0 + shift ) / 6.0 ) ) ;
   taom = ( 0.37 + 1.0 / ( exp ( ( _lv + 35.8 + shift ) / 19.7 ) + exp ( - ( _lv + 79.7 + shift ) / 12.7 ) ) ) / tadj ;
   _ltaodef = ( 1.0 / ( exp ( ( _lv + 46.0 + shift ) / 5.0 ) + exp ( - ( _lv + 238.0 + shift ) / 37.5 ) ) ) / tadj ;
   if ( _lv < ( - 63.0 - shift ) ) {
     taoh1 = _ltaodef ;
     }
   else {
     taoh1 = ( 19.0 / tadj ) ;
     }
   if ( _lv < ( - 73.0 - shift ) ) {
     taoh2 = _ltaodef ;
     }
   else {
     taoh2 = ( 60.0 / tadj ) ;
     }
    return 0; }
 
static void _hoc_settables(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 settables ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 4;}
 
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
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 4; ++_i) {
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
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  h2 = h20;
  h1 = h10;
  m2 = m20;
  m1 = m10;
 {
   tadj = pow( 2.8 , ( ( celsius - 23.0 ) / 10.0 ) ) ;
   settables ( _threadargscomma_ v ) ;
   m1 = m1inf ;
   m2 = m2inf ;
   h1 = hinf ;
   h2 = hinf ;
   output = gk_max * ( 0.6 * h1 * pow( m1 , 4.0 ) + 0.4 * h2 * pow( m2 , 4.0 ) ) ;
   i_output = output * ( v - ek ) ;
   ik = i_output ;
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
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   output = gk_max * ( 0.6 * h1 * pow( m1 , 4.0 ) + 0.4 * h2 * pow( m2 , 4.0 ) ) ;
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
 {   states(_p, _ppvar, _thread, _nt);
  } }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m1) - _p;  _dlist1[0] = &(Dm1) - _p;
 _slist1[1] = &(m2) - _p;  _dlist1[1] = &(Dm2) - _p;
 _slist1[2] = &(h1) - _p;  _dlist1[2] = &(Dh1) - _p;
 _slist1[3] = &(h2) - _p;  _dlist1[3] = &(Dh2) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/francesco/Desktop/MeMo/modfiles/TC_iA.mod";
static const char* nmodl_file_text = 
  "TITLE Fast Transient Potassium Current IA\n"
  "\n"
  ":   Huguenard and Prince, 1991\n"
  ":   The junction potential was considered\n"
  "\n"
  "\n"
  "UNITS {\n"
  "    (mV) = (millivolt)\n"
  "    (mA) = (milliamp)\n"
  "    (S)  = (siemens)\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "    SUFFIX TC_iA\n"
  "    USEION k READ ek WRITE ik\n"
  "    RANGE gk_max, ik, taom, taoh1, taoh2\n"
  "    RANGE shift\n"
  "\n"
  "\n"
  "\n"
  "    \n"
  "    RANGE output, i_output\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "    gk_max  = 5.5e-3 (S/cm2)	: Default maximum conductance\n"
  "    celsius\n"
  "    shift   = 0 (mV)\n"
  "}\n"
  "\n"
  "ASSIGNED { \n"
  "    v     (mV)\n"
  "    ek    (mV)\n"
  "    ik    (mA/cm2)\n"
  "    m1inf \n"
  "    m2inf\n"
  "    hinf\n"
  "    taoh1 (ms)\n"
  "    taoh2 (ms)\n"
  "    taom  (ms)\n"
  "    tadj\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "    \n"
  "    output\n"
  "    i_output\n"
  "}\n"
  "\n"
  "STATE {\n"
  "    m1 m2 h1 h2\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "    SOLVE states METHOD cnexp\n"
  "\n"
  "\n"
  "    \n"
  "    \n"
  "    output   = gk_max * (0.6*h1*m1^4+0.4*h2*m2^4)\n"
  "    i_output = output*(v-ek)\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "    ik = i_output\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "    tadj = 2.8 ^ ((celsius-23)/10)\n"
  "    settables(v)\n"
  "    m1 = m1inf\n"
  "    m2 = m2inf\n"
  "    h1 = hinf\n"
  "    h2 = hinf\n"
  "\n"
  "\n"
  "    \n"
  "    output   = gk_max * (0.6*h1*m1^4+0.4*h2*m2^4)\n"
  "    i_output = output*(v-ek)\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "    ik = i_output\n"
  "}\n"
  "\n"
  "DERIVATIVE states {  \n"
  "    settables(v)      \n"
  "    m1' = (m1inf-m1)/taom\n"
  "    m2' = (m2inf-m2)/taom\n"
  "    h1' = (hinf-h1)/taoh1\n"
  "    h2' = (hinf-h2)/taoh2\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "PROCEDURE settables(v (mV)) { \n"
  "    LOCAL taodef\n"
  "\n"
  "    m1inf = 1/(1+exp(-(v+60+shift)/8.5))\n"
  "    m2inf = 1/(1+exp(-(v+36+shift)/20))\n"
  "    hinf  = 1/(1+exp((v+78+shift)/6))\n"
  "\n"
  "    taom  = (0.37 + 1/(exp((v+35.8+shift)/19.7)+exp(-(v+79.7+shift)/12.7))) / tadj\n"
  "    \n"
  "    taodef = (1/(exp((v+46+shift)/5)+exp(-(v+238+shift)/37.5))) / tadj\n"
  "    if (v<(-63-shift)) {taoh1 = taodef} else {taoh1 = (19 / tadj)}\n"
  "    if (v<(-73-shift)) {taoh2 = taodef} else {taoh2 = (60 / tadj)}\n"
  "\n"
  "}\n"
  "\n"
  "UNITSON\n"
  ;
#endif
