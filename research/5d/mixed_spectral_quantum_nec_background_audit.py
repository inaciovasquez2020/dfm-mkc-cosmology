#!/usr/bin/env python3
"""Exact necessary circle-null Casimir stress at the candidate radion minimum.

At homogeneous stationary b=1, define V_Cas,E(b)=B G(b)/b^6,
W_J(b)=b^2 V_Cas,E(b) (Jordan reduced vacuum potential per unit circle
coordinate volume). 5D stress for a symmetry-preserving quantum effective
source has rho_C=W_J/b, p_w,C=-W_J', hence rho_C+p_w,C=
W_J/b-W_J'=-b V_Cas,E-b² V'_Cas,E. This is a reduced
stress-response identity, NOT the full covariant quantum effective action.
"""
from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path
if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

s=run_path(str(Path(__file__).with_name("mixed_periodic_spectral_ds_certificate.py")))
G,G1,V,lam=(s[k] for k in ("G","G1","V","lam"))
plus,times=(s[k] for k in ("plus","times"))
# At b=1, winding A=B/2; q²=4A=2B.
# Circle-null winding source (rho+p_w)_wind/B=q²/(2B)=1.
winding_null=(Q(1),Q(1))
# Casimir Einstein potential V_Cas/B=b^-6 G(b).
# W_J/B=b² V_Cas/B=b^-4 G(b); at b=1:
# rho_C/B=G, pw_C/B=4G-G1.
casimir_null=plus(times(G,5),times(G1,-1))
full_null=plus(winding_null,casimir_null)
# Positive 4D Einstein-frame de Sitter vacuum has H_E²=V/3.
# 5D Ric_5(u+e_w,u+e_w)=-3 b H_E²=-b V=-V at b=1.
einstein_null=times(V,-1)
assert full_null[0]==einstein_null[0]
assert full_null[1]==einstein_null[1]
assert -Q(191,100)<casimir_null[0]<=casimir_null[1]<-Q(19,10)
assert full_null[1]<0
# Physical/reduced convention check. Let L be the coordinate-circle length
# (L=2*pi physically); physical V4=L*Vnorm, physical M4²=L
# for M5³=1 at b*=1. Therefore H²=V4/(3*M4²)=Vnorm/3.
# Jordan W4=L*Wnorm, and dividing 4D energy / circle length to
# form the LOCAL five-dimensional stress removes exactly the same L.
# The same convention applies to winding and bulk Lambda, not just Casimir.
# Pure algebra: test arbitrary rational L; valid identically at L=2*pi.
for L in (Q(1,7),Q(1),Q(7,3),Q(100)):
    physical_V=times(V,L)
    normalized_H2=times(physical_V,Q(1,3)/L)
    assert normalized_H2==times(V,Q(1,3))
    full_5d_null=plus(winding_null,casimir_null)
    physical_reduced_null=times(full_5d_null,L)
    assert times(physical_reduced_null,Q(1)/L)==full_5d_null
# Real periodic scalar coefficient after integrating the full circle
# is B4=3/(64*pi^6). Dividing the entire action by 2*pi yields
# Bnorm=3/(128*pi^7). The numeric bounds are on stress / Bnorm.
assert Q(3,128*3**7)<Q(1,10000)
print("CIRCLE_LENGTH_FACTOR := CANCELS_IN_FRIEDMANN_AND_LOCAL_STRESS")
print("NORMALIZED_B := B4/(2*pi)=3/(128*pi^7)")
# Explicit classical off-shell residual with Casimir removed:
# Ric(V,V)-(T_winding+T_Lambda)(V,V)
# =(-V/B)-1 = casimir_null/B !=0.
assert casimir_null[1]<-Q(19,10)
# Jordan reduced W_C reproduces the necessary circle-null stress
# at b=1, but this determines only background response to b and gJ.
# It does not fix second variation for w-dependent metric/axion
# perturbations, nonlocal kernels, gauge ghosts or renormalization.
print("CERTIFIED_CIRCLE_NULL_CASIMIR_STRESS_PER_B := BETWEEN_-191/100_AND_-19/10")
print("WINDING_CIRCLE_NULL_STRESS_PER_B := +1")
print("TOTAL_CIRCLE_NULL_STRESS_PER_B := -V_OVER_B")
print("STATIONARY_REDUCED_CASIMIR_STRESS_RESPONSE := CONSISTENT")
print("CLASSICAL_EINSTEIN_WINDING_ONLY_ON_DS_BACKGROUND := OFF_SHELL")
print("QUANTUM_NULL_ENERGY_VIOLATION_IN_CIRCLE_CHANNEL := NECESSARY")
print("COMPLETE_5D_COVARIANT_EFFECTIVE_ACTION_SECOND_VARIATION := NOT_CONSTRUCTED")
print("FULL_NONZERO_KK_GAUGE_FIXED_HESSIAN := OPEN")
