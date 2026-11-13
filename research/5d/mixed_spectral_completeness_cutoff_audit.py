#!/usr/bin/env python3
"""Independent exact audit of truncation fragility and 5D gravitational cutoff.

Imports the exact spectral interval *certificate* rather than estimating the
Casimir sums numerically. The additional massless real periodic boson is an
explicit independent free-field determinant sensitivity test, NOT a claim
about the actual mixed winding-scalar/graviphoton fluctuation spectrum.
"""
from fractions import Fraction as F
from pathlib import Path
from runpy import run_path

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

source=run_path(str(Path(__file__).with_name(
    "mixed_periodic_spectral_ds_certificate.py")))
V=source["V"]
V2=source["V2"]
lam=source["lam"]
zeta=source["zeta"]
times=source["times"]
plus=source["plus"]

# Candidate: V=Lambda/b+A/b³+B[4*S(mb)-zeta(5)]/b^6.
# Add just one further independent PERIODIC REAL MASSLESS SCALAR:
# Delta V=-B*zeta(5)/b^6. Refix Lambda (only) to enforce V'(1)=0,
# retaining A, m, spin multiplicities and b*=1 fixed.
# Delta Lambda/B=+6*zeta(5).
# Delta V(1)/B=+5*zeta(5).
# Delta V''(1)/B=-30*zeta(5).
new_lam=plus(lam,times(zeta,6))
new_V=plus(V,times(zeta,5))
new_V2=plus(V2,times(zeta,-30))
assert zeta[0]>F(1)
assert new_lam[0]>F(7)
assert new_V[0]>F(59,10)
assert new_V2[1]<F(-28)
assert new_V2[1]<0
assert V2[0]>F(0)                 # contrast: truncated witness stable
# With canonical phi=sqrt(3/2)log b, sign(m_phi^2)=sign(V'') at stationarity.
assert times(new_V2,F(2,3))[1]<0
print("ADDITIONAL_FREE_REAL_PERIODIC_MASSLESS_BOSON := -B*zeta(5)/b^6")
print("AFTER_REFIXING_BULK_LAMBDA_ONLY := V_OVER_B_POSITIVE_BUT_VPP_OVER_B_NEGATIVE")
print("NEW_VPP_OVER_B_UPPER_BOUND := LESS_THAN_-28")
print("TRUNCATED_SPECTRUM_MINIMUM_ROBUST_TO_ONE_EXTRA_BOSON := REFUTED")
print("WINDING_SCALAR_GRAVIPHOTON_MIXED_DETERMINANT := NOT_COMPUTED")

# 5D Einstein action M5³ R5/2 on circle radius R. M5=1, R=b*=1.
# In the JORDAN frame, the local first KK energy equals 1/R.
# M4²=2*pi*R*M5³; at reference radius M4/M5=sqrt(2*pi).
# The actual one-loop Dirac mass m=5/(2*pi*R).
# Use rigorous elementary inequalities 3<pi<22/7 to avoid floats:
# 35/44 < m/M5 < 5/6 at R=1.
assert F(35,44)<F(5,6)<1
assert 1==F(1) # m_KK/M5=1
assert F(6)<F(44,7) # bounds on M4²/M5², not on KK cutoff
print("REFERENCE_PHYSICAL_RADIUS_R_TIMES_M5 := 1")
print("JORDAN_FIRST_KK_MASS_OVER_M5 := 1")
print("DIRAC_MASS_OVER_M5 := BETWEEN_35/44_AND_5/6")
print("4D_PLANCK_SQUARED_OVER_M5_SQUARED := BETWEEN_6_AND_44/7")
print("PARAMETRIC_KK_BELOW_5D_GRAVITATIONAL_SCALE := NOT_ESTABLISHED")
print("COMPLETE_5D_ONE_LOOP_POTENTIAL := NOT_COMPUTED")
print("COUPLED_KK_GHOST_HYPERBOLICITY_AND_CHRONOS := OPEN")
