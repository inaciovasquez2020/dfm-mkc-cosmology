#!/usr/bin/env python3
"""Exact homothetic large-circle scaling of the *truncated* mixed Casimir model.

Demonstrates that an EFT hierarchy can be created by retuning L, winding q,
and Dirac m while holding the dimensionless spectral shape fixed. It ALSO
demonstrates that the omitted-boson radion instability survives any such
rescaling. No physical full-spectrum stability is claimed.
"""
from fractions import Fraction as F
from pathlib import Path
from runpy import run_path

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")
c=run_path(str(Path(__file__).with_name(
    "mixed_periodic_spectral_ds_certificate.py")))
a=run_path(str(Path(__file__).with_name(
    "mixed_spectral_completeness_cutoff_audit.py")))
V,V2,lam,zeta=(c[k] for k in ("V","V2","lam","zeta"))
plus,times=(c[k] for k in ("plus","times"))

# Base in M5=1 units:
# V0(x)=L0/x+(B/2)/x³+B G(x)/x^6,
# G(x)=4*S[5*x/(2*pi)]-zeta(5), B=3/(64*pi^6).
# For arbitrary radius R>0, define:
# b=R*x, m_R=5/(2*pi*R), A_R=B/(2*R³), L_R=L0/R^5.
# Then V_R(R*x)=V0(x)/R^6, exactly. Derivatives in physical b
# transform V'_R=R^-7 V0', V''_R=R^-8 V0''.
# mrad²=(2/3)b² V''_R ∝ R^-6; H_E²=V_R/3 ∝ R^-6;
# mKK,E²=b^-3 ∝ R^-3. Thus mKK/H ∝ R^(3/2).
# 5D local Jordan mass mKK/M5=1/R; Einstein-frame cutoff
# M5,E=R^-1/2 and mKK,E/M5,E=1/R.

for R in (F(1),F(2),F(7,3),F(10),F(100)):
    # Verify exact scaling of all three potential monomials for
    # independent dimensionless x and rational formal G(x).
    for x in (F(1,2),F(1),F(7,3)):
        for Gval in (F(-3),F(0),F(13,10)):
            B=F(1,10000) # formal coefficient, independent of R
            L0=F(17,100)*B
            A0=B/2
            baseline=L0/x+A0/x**3+B*Gval/x**6
            scaled=(L0/R**5)/(R*x)+(A0/R**3)/(R*x)**3+B*Gval/(R*x)**6
            assert scaled==baseline/R**6
    assert 1/R>0

R=F(100)
# At b*=R, in Jordan local 5D units, mKK/M5=1/R and
# mDirac/M5=5/(2*pi*R). With pi>3, mDirac/M5<5/(6R).
assert 1/R==F(1,100)
assert F(5,6)/R<F(1,100)
# mKK,H_E² ratio: 3 R^3/[B*(V0/B)].
# From exact full-spectral certificate, 0<V0/B<91/100 and
# B=3/(64*pi^6) <1/10000 (because pi>3).
ratio_KK_H_squared_lower=3*R**3/(F(91,100)*F(1,10000))
assert ratio_KK_H_squared_lower>100000**2

# The extra-free-boson curvature at any rescaled b*=R is
# V''_extra(R)/[B R^-8] = (V''_base/B)-30*zeta(5)<-28.
v2_extra=a["new_V2"]
assert v2_extra[1]<F(-28)
for R in (F(1),F(10),F(100),F(1000)):
    # mrad²_extra=(2/3)*(R)^2 * (B*R^-8)*v2_extra
    # = (2/3)*B R^-6*v2_extra: remains strictly negative.
    assert F(2,3)*v2_extra[1]/R**6<0

print("SHAPE_PRESERVING_SCALING := b*=R, m_Dirac=5/(2*pi*R)")
print("TUNING_REQUIRED := A_R=B/(2*R^3), Lambda_R=Lambda0/R^5")
print("TRUNCATED_ONE_LOOP_POTENTIAL_SCALING := V_R(R*x)=V0(x)/R^6")
print("RADION_SQUARED_MASS_AND_HUBBLE_SQUARED := SCALE_AS_R^-6")
print("EINSTEIN_FIRST_KK_SQUARED_MASS := SCALES_AS_R^-3")
print("R=100_FIRST_KK_JORDAN_M5_RATIO := 1/100")
print("R=100_DIRAC_JORDAN_M5_RATIO := LESS_THAN_1/100")
print("R=100_FIRST_KK_OVER_H := GREATER_THAN_100000")
print("RADIUS_RESCALING_REMOVES_GRAVITATIONAL_CUTOFF_OBJECTION := FORMAL_PARAMETRIC_REGIME")
print("EXTRA_MASSLESS_BOSON_RADION_CURVATURE := NEGATIVE_FOR_EVERY_R")
print("COMPLETED_CASIMIR_SPECTRUM_AND_PHYSICAL_STABILITY := OPEN")
