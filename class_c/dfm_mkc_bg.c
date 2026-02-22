#include <math.h>
#include "../include/dfm_mkc_bg.h"

static void densities(double z, const dfm_mkc_params* p, double* rho_m, double* rho_r, double* rho_L, double* rho_tot) {
  double zp1 = 1.0 + z;
  *rho_m = p->Om_m0 * p->H0 * p->H0 * zp1*zp1*zp1;
  *rho_r = p->Om_r0 * p->H0 * p->H0 * zp1*zp1*zp1*zp1;
  *rho_L = p->Om_L0 * p->H0 * p->H0;
  *rho_tot = (*rho_m) + (*rho_r) + (*rho_L);
}

int dfm_mkc_H_Phi_of_z(double z, const dfm_mkc_params* p, double* H, double* Phi) {
  double rho_m, rho_r, rho_L, rho_tot;
  densities(z, p, &rho_m, &rho_r, &rho_L, &rho_tot);

  double Om_Phi0 = 1.0 - (p->Om_m0 + p->Om_r0 + p->Om_L0);
  double Phi0 = p->H0 * p->H0 * Om_Phi0;

  double Phi_local = Phi0;

  double H2 = (8.0*M_PI/3.0) * rho_tot + Phi_local;
  if (H2 <= 0.0) return 1;

  *H = sqrt(H2);
  *Phi = Phi_local;
  return 0;
}
