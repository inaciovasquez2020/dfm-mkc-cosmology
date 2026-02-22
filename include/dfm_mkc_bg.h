#ifndef DFM_MKC_BG_H
#define DFM_MKC_BG_H

typedef struct {
  double H0;
  double Om_m0;
  double Om_r0;
  double Om_L0;
  double alpha;
  double beta;
} dfm_mkc_params;

int dfm_mkc_H_Phi_of_z(double z, const dfm_mkc_params* p, double* H, double* Phi);

#endif
