#!/usr/bin/env python3
"""Exact all-time-interval Kaluza--Klein/Hubble separation guard.

Background from PR #340. Assumes a unit coordinate circle w~w+2pi, a minimally
coupled massless 5D spectator scalar, and the standard zero-mode Einstein frame
g_E=b*g_J. This is a necessary hierarchy test, not a complete EFT/KK stability
analysis. Entire interval is certified using rational exponential bounds.
"""
from fractions import Fraction as F

if not __debug__:
    raise SystemExit("INCOMPLETE: assertion checks disabled")

r=F(1,100)
# a(t)=exp(t-3t²/5), b(t)=exp(-t/10+t²/2)
# H_J=a_dot/a=1-6t/5, F_c=b_dot/b=-1/10+t.
# H_E=(H_J+F_c/2)/sqrt(b) = (19/20-7t/10)/sqrt(b).
# A 5D massless spectator mode exp(i n w) has Jordan mass |n|/b;
# after Einstein conformal rescaling, m_n,E=|n|/b^(3/2).
# Thus m_1,E/H_E=1/[b*(19/20-7t/10)].

# For |t|<=r, |log b|=|-t/10+t²/2|<= r/10+r²/2.
u=r/10+r*r/2
assert u==F(21,20000) and F(0)<u<F(1)
# For |x|<=u<1: exp(x)>=1-u and exp(x)<=1/(1-u).
# Proof: exp(-u)>=1-u and exp(u)<=sum_{n>=0}u^n=1/(1-u).
b_lo=1-u
b_hi=1/(1-u)
Hhat_lo=F(19,20)-F(7,10)*r
Hhat_hi=F(19,20)+F(7,10)*r
assert Hhat_lo==F(943,1000)
assert Hhat_hi==F(957,1000)
assert b_lo>0 and Hhat_lo>0
ratio_lo=1/(b_hi*Hhat_hi)
ratio_hi=1/(b_lo*Hhat_lo)
assert ratio_lo==F(19979,19140)
assert ratio_hi==F(20000000,18840197)
assert ratio_lo>F(1)
assert ratio_hi<F(107,100)
assert F(1)/F(19,20)==F(20,19)
# log a_E(t)=19*t/20-7*t*t/20, hence across [-r,r]:
# Delta N_E=log[a_E(r)/a_E(-r)]=19*r/10=19/1000 e-folds.
efolds=F(19,10)*r
assert efolds==F(19,1000) and efolds<F(1,50)

# For all w-Fourier indices n, the mass/Hubble ratio scales |n|.
# n=1 does not decouple parametrically: ratio lies near one.
for n in (1,2,3,10):
    assert n*ratio_lo<=n*ratio_hi
assert ratio_hi<F(2)
print("INTERVAL := [-1/100,1/100]")
print("MASSLESS_SPECTATOR_KK_MASS_E := |n|*b^(-3/2)")
print("EINSTEIN_FRAME_HUBBLE := (19/20-7*t/10)/sqrt(b)")
print("EXACT_KK_HUBBLE_RATIO_AT_ZERO := 20/19")
print("FULL_INTERVAL_RATIO_STRICT_BOUNDS := ",ratio_lo," < m1,E/H_E < ",ratio_hi)
print("FULL_INTERVAL_SIMPLE_BOUND := 1 < m1,E/H_E < 107/100")
print("TOTAL_EINSTEIN_FRAME_EFOLDS_ON_CERTIFIED_INTERVAL := 19/1000")
print("PARAMETRIC_KK_HUBBLE_SEPARATION := NOT_ESTABLISHED")
print("ZERO_MODE_LOW_ENERGY_TRUNCATION_AT_HUBBLE_SCALE := NOT_CONTROLLED_BY_KK_GAP")
print("MASS_SPECTRUM_FOR_MIXED_GRAVITATIONAL_MATTER_MODES := NOT_RUN")
print("PHYSICAL_5D_NECESSITY := OPEN")
