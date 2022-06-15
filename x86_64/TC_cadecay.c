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
 
#define nrn_init _nrn_init__TC_cad
#define _nrn_initial _nrn_initial__TC_cad
#define nrn_cur _nrn_cur__TC_cad
#define _nrn_current _nrn_current__TC_cad
#define nrn_jacob _nrn_jacob__TC_cad
#define nrn_state _nrn_state__TC_cad
#define _net_receive _net_receive__TC_cad 
#define state state__TC_cad 
 
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
#define delta_L1 _p[0]
#define taur_L1 _p[1]
#define cal1_inf _p[2]
#define delta_L2 _p[3]
#define taur_L2 _p[4]
#define cal2_inf _p[5]
#define delta_T _p[6]
#define taur_T _p[7]
#define cat_inf _p[8]
#define cal1i _p[9]
#define Dcal1i _p[10]
#define cal2i _p[11]
#define Dcal2i _p[12]
#define cati _p[13]
#define Dcati _p[14]
#define ical1 _p[15]
#define ical2 _p[16]
#define icat _p[17]
#define v _p[18]
#define _g _p[19]
#define _ion_ical1	*_ppvar[0]._pval
#define _ion_cal1i	*_ppvar[1]._pval
#define _style_cal1	*((int*)_ppvar[2]._pvoid)
#define _ion_ical2	*_ppvar[3]._pval
#define _ion_cal2i	*_ppvar[4]._pval
#define _style_cal2	*((int*)_ppvar[5]._pvoid)
#define _ion_icat	*_ppvar[6]._pval
#define _ion_cati	*_ppvar[7]._pval
#define _style_cat	*((int*)_ppvar[8]._pvoid)
 
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
 /* declaration of user functions */
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
 "setdata_TC_cad", _hoc_setdata,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "delta_L1_TC_cad", "/um",
 "taur_L1_TC_cad", "ms",
 "cal1_inf_TC_cad", "mM",
 "delta_L2_TC_cad", "/um",
 "taur_L2_TC_cad", "ms",
 "cal2_inf_TC_cad", "mM",
 "delta_T_TC_cad", "/um",
 "taur_T_TC_cad", "ms",
 "cat_inf_TC_cad", "mM",
 0,0
};
 static double cati0 = 0;
 static double cal2i0 = 0;
 static double cal1i0 = 0;
 static double delta_t = 0.01;
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
 
#define _cvode_ieq _ppvar[9]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"TC_cad",
 "delta_L1_TC_cad",
 "taur_L1_TC_cad",
 "cal1_inf_TC_cad",
 "delta_L2_TC_cad",
 "taur_L2_TC_cad",
 "cal2_inf_TC_cad",
 "delta_T_TC_cad",
 "taur_T_TC_cad",
 "cat_inf_TC_cad",
 0,
 0,
 0,
 0};
 static Symbol* _cal1_sym;
 static Symbol* _cal2_sym;
 static Symbol* _cat_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 20, _prop);
 	/*initialize range parameters*/
 	delta_L1 = 0.5;
 	taur_L1 = 5;
 	cal1_inf = 5e-05;
 	delta_L2 = 0.5;
 	taur_L2 = 5;
 	cal2_inf = 5e-05;
 	delta_T = 0.5;
 	taur_T = 5;
 	cat_inf = 5e-05;
 	_prop->param = _p;
 	_prop->param_size = 20;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 10, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_cal1_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[0]._pval = &prop_ion->param[3]; /* ical1 */
 	_ppvar[1]._pval = &prop_ion->param[1]; /* cal1i */
 	_ppvar[2]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for cal1 */
 prop_ion = need_memb(_cal2_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[3]._pval = &prop_ion->param[3]; /* ical2 */
 	_ppvar[4]._pval = &prop_ion->param[1]; /* cal2i */
 	_ppvar[5]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for cal2 */
 prop_ion = need_memb(_cat_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[6]._pval = &prop_ion->param[3]; /* icat */
 	_ppvar[7]._pval = &prop_ion->param[1]; /* cati */
 	_ppvar[8]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for cat */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _thread_mem_init(Datum*);
 static void _thread_cleanup(Datum*);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _TC_cadecay_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("cal1", 2.0);
 	ion_reg("cal2", 2.0);
 	ion_reg("cat", 2.0);
 	_cal1_sym = hoc_lookup("cal1_ion");
 	_cal2_sym = hoc_lookup("cal2_ion");
 	_cat_sym = hoc_lookup("cat_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 5);
  _extcall_thread = (Datum*)ecalloc(4, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 20, 10);
  hoc_register_dparam_semantics(_mechtype, 0, "cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "#cal1_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "#cal2_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cat_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "cat_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "#cat_ion");
  hoc_register_dparam_semantics(_mechtype, 9, "cvodeieq");
 	nrn_writes_conc(_mechtype, 0);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 TC_cad /home/francesco/Desktop/MeMo/modfiles/TC_cadecay.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 
#define FARADAY _nrnunit_FARADAY[_nrnunit_use_legacy_]
static double _nrnunit_FARADAY[2] = {0x1.78e555060882cp+16, 96485.3}; /* 96485.3321233100141 */
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
#define _deriv1_advance _thread[0]._i
#define _dith1 1
#define _recurse _thread[2]._i
#define _newtonspace1 _thread[3]._pvoid
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist2[3];
  static int _slist1[3], _dlist1[3];
 static int state(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   double _ldrive_channel ;
 _ldrive_channel = - 10000.0 * ( ical1 * delta_L1 / ( 2.0 * FARADAY ) ) ;
   if ( _ldrive_channel <= 0. ) {
     _ldrive_channel = 0. ;
     }
   Dcal1i = _ldrive_channel - ( cal1i - cal1_inf ) / taur_L1 ;
   _ldrive_channel = - 10000.0 * ( ical2 * delta_L2 / ( 2.0 * FARADAY ) ) ;
   if ( _ldrive_channel <= 0. ) {
     _ldrive_channel = 0. ;
     }
   Dcal2i = _ldrive_channel - ( cal2i - cal2_inf ) / taur_L2 ;
   _ldrive_channel = - 10000.0 * ( icat * delta_T / ( 2.0 * FARADAY ) ) ;
   if ( _ldrive_channel <= 0. ) {
     _ldrive_channel = 0. ;
     }
   Dcati = _ldrive_channel - ( cati - cat_inf ) / taur_T ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 double _ldrive_channel ;
 _ldrive_channel = - 10000.0 * ( ical1 * delta_L1 / ( 2.0 * FARADAY ) ) ;
 if ( _ldrive_channel <= 0. ) {
   _ldrive_channel = 0. ;
   }
 Dcal1i = Dcal1i  / (1. - dt*( ( - ( ( 1.0 ) ) / taur_L1 ) )) ;
 _ldrive_channel = - 10000.0 * ( ical2 * delta_L2 / ( 2.0 * FARADAY ) ) ;
 if ( _ldrive_channel <= 0. ) {
   _ldrive_channel = 0. ;
   }
 Dcal2i = Dcal2i  / (1. - dt*( ( - ( ( 1.0 ) ) / taur_L2 ) )) ;
 _ldrive_channel = - 10000.0 * ( icat * delta_T / ( 2.0 * FARADAY ) ) ;
 if ( _ldrive_channel <= 0. ) {
   _ldrive_channel = 0. ;
   }
 Dcati = Dcati  / (1. - dt*( ( - ( ( 1.0 ) ) / taur_T ) )) ;
  return 0;
}
 /*END CVODE*/
 
static int state (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset=0; int error = 0;
 { double* _savstate1 = _thread[_dith1]._pval;
 double* _dlist2 = _thread[_dith1]._pval + 3;
 int _counte = -1;
 if (!_recurse) {
 _recurse = 1;
 {int _id; for(_id=0; _id < 3; _id++) { _savstate1[_id] = _p[_slist1[_id]];}}
 error = nrn_newton_thread(_newtonspace1, 3,_slist2, _p, state, _dlist2, _ppvar, _thread, _nt);
 _recurse = 0; if(error) {abort_run(error);}}
 {
   double _ldrive_channel ;
 _ldrive_channel = - 10000.0 * ( ical1 * delta_L1 / ( 2.0 * FARADAY ) ) ;
   if ( _ldrive_channel <= 0. ) {
     _ldrive_channel = 0. ;
     }
   Dcal1i = _ldrive_channel - ( cal1i - cal1_inf ) / taur_L1 ;
   _ldrive_channel = - 10000.0 * ( ical2 * delta_L2 / ( 2.0 * FARADAY ) ) ;
   if ( _ldrive_channel <= 0. ) {
     _ldrive_channel = 0. ;
     }
   Dcal2i = _ldrive_channel - ( cal2i - cal2_inf ) / taur_L2 ;
   _ldrive_channel = - 10000.0 * ( icat * delta_T / ( 2.0 * FARADAY ) ) ;
   if ( _ldrive_channel <= 0. ) {
     _ldrive_channel = 0. ;
     }
   Dcati = _ldrive_channel - ( cati - cat_inf ) / taur_T ;
   {int _id; for(_id=0; _id < 3; _id++) {
if (_deriv1_advance) {
 _dlist2[++_counte] = _p[_dlist1[_id]] - (_p[_slist1[_id]] - _savstate1[_id])/dt;
 }else{
_dlist2[++_counte] = _p[_slist1[_id]] - _savstate1[_id];}}}
 } }
 return _reset;}
 
static int _ode_count(int _type){ return 3;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ical1 = _ion_ical1;
  cal1i = _ion_cal1i;
  ical2 = _ion_ical2;
  cal2i = _ion_cal2i;
  icat = _ion_icat;
  cati = _ion_cati;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  _ion_cal1i = cal1i;
  _ion_cal2i = cal2i;
  _ion_cati = cati;
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 3; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 	_pv[0] = &(_ion_cal1i);
 	_pv[1] = &(_ion_cal2i);
 	_pv[2] = &(_ion_cati);
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
  ical1 = _ion_ical1;
  cal1i = _ion_cal1i;
  ical2 = _ion_ical2;
  cal2i = _ion_cal2i;
  icat = _ion_icat;
  cati = _ion_cati;
 _ode_matsol_instance1(_threadargs_);
 }}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[_dith1]._pval = (double*)ecalloc(6, sizeof(double));
   _newtonspace1 = nrn_cons_newtonspace(3);
 }
 
static void _thread_cleanup(Datum* _thread) {
   free((void*)(_thread[_dith1]._pval));
   nrn_destroy_newtonspace(_newtonspace1);
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_cal1_sym, _ppvar, 0, 3);
   nrn_update_ion_pointer(_cal1_sym, _ppvar, 1, 1);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 3, 3);
   nrn_update_ion_pointer(_cal2_sym, _ppvar, 4, 1);
   nrn_update_ion_pointer(_cat_sym, _ppvar, 6, 3);
   nrn_update_ion_pointer(_cat_sym, _ppvar, 7, 1);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
 {
   cal1i = cal1_inf ;
   cal2i = cal2_inf ;
   cati = cat_inf ;
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
  ical1 = _ion_ical1;
  cal1i = _ion_cal1i;
  ical2 = _ion_ical2;
  cal2i = _ion_cal2i;
  icat = _ion_icat;
  cati = _ion_cati;
 initmodel(_p, _ppvar, _thread, _nt);
  _ion_cal1i = cal1i;
  nrn_wrote_conc(_cal1_sym, (&(_ion_cal1i)) - 1, _style_cal1);
  _ion_cal2i = cal2i;
  nrn_wrote_conc(_cal2_sym, (&(_ion_cal2i)) - 1, _style_cal2);
  _ion_cati = cati;
  nrn_wrote_conc(_cat_sym, (&(_ion_cati)) - 1, _style_cat);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{
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
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
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
  ical1 = _ion_ical1;
  cal1i = _ion_cal1i;
  ical2 = _ion_ical2;
  cal2i = _ion_cal2i;
  icat = _ion_icat;
  cati = _ion_cati;
 {  _deriv1_advance = 1;
 derivimplicit_thread(3, _slist1, _dlist1, _p, state, _ppvar, _thread, _nt);
_deriv1_advance = 0;
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 3; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 } {
   }
  _ion_cal1i = cal1i;
  _ion_cal2i = cal2i;
  _ion_cati = cati;
}}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(cal1i) - _p;  _dlist1[0] = &(Dcal1i) - _p;
 _slist1[1] = &(cal2i) - _p;  _dlist1[1] = &(Dcal2i) - _p;
 _slist1[2] = &(cati) - _p;  _dlist1[2] = &(Dcati) - _p;
 _slist2[0] = &(cati) - _p;
 _slist2[1] = &(cal2i) - _p;
 _slist2[2] = &(cal1i) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/francesco/Desktop/MeMo/modfiles/TC_cadecay.mod";
static const char* nmodl_file_text = 
  ": calcium microdomains\n"
  ": Francesco Cavarretta Aug. 19th 2020\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX TC_cad\n"
  "        \n"
  "	USEION cal1 READ ical1 WRITE cal1i VALENCE 2\n"
  "        USEION cal2 READ ical2 WRITE cal2i VALENCE 2\n"
  "        :USEION cal3 READ ical3 WRITE cal3i VALENCE 2\n"
  "	USEION cat READ icat  WRITE cati  VALENCE 2\n"
  "        \n"
  "        :RANGE delta_L3, taur_L3, cal3_inf, delta_L1, taur_L1, cal1_inf,  delta_L2, taur_L2, cal2_inf,  delta_T, taur_T, cat_inf\n"
  "        RANGE delta_L1, taur_L1, cal1_inf,  delta_L2, taur_L2, cal2_inf,  delta_T, taur_T, cat_inf\n"
  "\n"
  "\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "\n"
  "	(mM)	= (milli/liter)\n"
  "	(um)	= (micron)\n"
  "	(mA)	= (milliamp)\n"
  "	(msM)	= (ms mM)\n"
  "	FARADAY = (faraday) (coulombs)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	:depth	= .1	 (um)		: depth of shell\n"
  "	:gamma   = 0.05 	 (1)		: EI: percent of free calcium (not buffered)\n"
  "        \n"
  "        delta_L1   = 0.5    (/um)\n"
  "        taur_L1    = 5      (ms)  : rate of calcium removal\n"
  "        cal1_inf   = 5e-5   (mM)  : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "		\n"
  "        delta_L2   = 0.5    (/um)\n"
  "        taur_L2    = 5      (ms)  : rate of calcium removal\n"
  "        cal2_inf   = 5e-5   (mM)  : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "        \n"
  "        delta_T    = 0.5    (/um)\n"
  "        taur_T     = 5      (ms)  : rate of calcium removal\n"
  "        cat_inf    = 5e-5   (mM)  : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "\n"
  "        :delta_L3   = 0.5    (/um)\n"
  "        :taur_L3    = 5      (ms)  : rate of calcium removal\n"
  "        :cal3_inf   = 5e-5   (mM)  : Value from Amarillo et al., J Neurophysiol, 2014\n"
  "\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	cal1i		(mM) \n"
  "	cal2i		(mM) \n"
  "	:cal3i		(mM) \n"
  "	cati		(mM) \n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	cal1i = cal1_inf\n"
  "	cal2i = cal2_inf\n"
  "	cati  = cat_inf\n"
  "	:cal3i = cal3_inf\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ical1		(mA/cm2)\n"
  "	ical2		(mA/cm2)\n"
  "	:ical3		(mA/cm2)\n"
  "	icat		(mA/cm2)\n"
  "}\n"
  "	\n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD derivimplicit\n"
  "	\n"
  "}\n"
  "\n"
  "DERIVATIVE state { LOCAL drive_channel\n"
  "        : delta = gamma/depth\n"
  "        drive_channel = -10000*(ical1 * delta_L1/(2*FARADAY))\n"
  "        if (drive_channel <= 0.) { drive_channel = 0. }	: cannot pump inward\n"
  "        cal1i' =  drive_channel - (cal1i-cal1_inf)/taur_L1\n"
  "\n"
  "                   \n"
  "        drive_channel = -10000*(ical2 * delta_L2/(2*FARADAY))\n"
  "        if (drive_channel <= 0.) { drive_channel = 0. }	: cannot pump inward\n"
  "        cal2i' = drive_channel - (cal2i-cal2_inf)/taur_L2\n"
  "\n"
  "                   \n"
  "        drive_channel = -10000*(icat * delta_T/(2*FARADAY))\n"
  "        if (drive_channel <= 0.) { drive_channel = 0. }	: cannot pump inward\n"
  "        cati'  = drive_channel - (cati-cat_inf)/taur_T\n"
  "                   \n"
  "        :cal3i' = -10000*(ical3 * delta_L3/(2*FARADAY)) - (cal3i-cal3_inf)/taur_L3\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
