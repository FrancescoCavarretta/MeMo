#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _ampanmda_reg(void);
extern void _BK_reg(void);
extern void _exp2syn_reg(void);
extern void _expsyn_reg(void);
extern void _gabaa_reg(void);
extern void _iM_reg(void);
extern void _SK_E2_reg(void);
extern void _TC_cadecay_reg(void);
extern void _TC_HH_reg(void);
extern void _TC_iA_reg(void);
extern void _TC_iD_reg(void);
extern void _TC_Ih_Bud97_reg(void);
extern void _TC_iL_reg(void);
extern void _TC_ITGHK_Des98_reg(void);
extern void _vecstim_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"modfiles/ampanmda.mod\"");
    fprintf(stderr," \"modfiles/BK.mod\"");
    fprintf(stderr," \"modfiles/exp2syn.mod\"");
    fprintf(stderr," \"modfiles/expsyn.mod\"");
    fprintf(stderr," \"modfiles/gabaa.mod\"");
    fprintf(stderr," \"modfiles/iM.mod\"");
    fprintf(stderr," \"modfiles/SK_E2.mod\"");
    fprintf(stderr," \"modfiles/TC_cadecay.mod\"");
    fprintf(stderr," \"modfiles/TC_HH.mod\"");
    fprintf(stderr," \"modfiles/TC_iA.mod\"");
    fprintf(stderr," \"modfiles/TC_iD.mod\"");
    fprintf(stderr," \"modfiles/TC_Ih_Bud97.mod\"");
    fprintf(stderr," \"modfiles/TC_iL.mod\"");
    fprintf(stderr," \"modfiles/TC_ITGHK_Des98.mod\"");
    fprintf(stderr," \"modfiles/vecstim.mod\"");
    fprintf(stderr, "\n");
  }
  _ampanmda_reg();
  _BK_reg();
  _exp2syn_reg();
  _expsyn_reg();
  _gabaa_reg();
  _iM_reg();
  _SK_E2_reg();
  _TC_cadecay_reg();
  _TC_HH_reg();
  _TC_iA_reg();
  _TC_iD_reg();
  _TC_Ih_Bud97_reg();
  _TC_iL_reg();
  _TC_ITGHK_Des98_reg();
  _vecstim_reg();
}

#if defined(__cplusplus)
}
#endif
