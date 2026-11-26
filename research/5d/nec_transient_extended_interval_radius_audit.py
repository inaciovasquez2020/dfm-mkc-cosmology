#!/usr/bin/env python3
"""Exact rational proof certificate for a wider NEC/DEC accelerating interval
and freely rescaled 5D circle. No dependencies, downloads, or file writes.

The rescaling preserves the locally reconstructed Einstein-scalar-Maxwell
equations (given the flux ansatz in PR #340); it does not establish stability.
"""
from fractions import Fraction as F
from pathlib import Path
import runpy

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")
src=runpy.run_path(str(Path(__file__).with_name(
    "nec_transient_accelerating_circle_exact.py")))
rho,p3,pw,H,Fc,A = (src[v] for v in
                   ("rho","p3","pw","H","F","A"))
add,sub,scale,poly = (src[v] for v in ("add","sub","scale","poly"))
def evaluate(p,t):
    return sum(c*t**i for i,c in enumerate(p))
def bernstein2(p,l,r):
    assert len(p)<=3 and l<r
    m=(l+r)/2
    b0=evaluate(p,l)
    b2=evaluate(p,r)
    b1=2*evaluate(p,m)-(b0+b2)/2
    # A quadratic equals b0*(1-u)^2+2*b1*u*(1-u)+b2*u^2
    # for u=(t-l)/(r-l). All positive coefficients imply positivity
    # throughout the full closed interval, without sampling.
    return b0,b1,b2

lo,hi=F(-1,50),F(9,100)
C=add(rho,pw)
D=sub(p3,pw)
V=scale(sub(rho,p3),F(1,2))
Hhat=add(H,scale(Fc,F(1,2)))
checks={
    "3space_expansion":H,
    "circle_shrinking":scale(Fc,-1),
    "energy_density":rho,
    "NEC_space":add(rho,p3),
    "NEC_circle":C,
    "DEC_space":sub(rho,p3),
    "DEC_circle":sub(rho,pw),
    "positive_scalar_kinetic":C,
    "positive_Maxwell_electric":D,
    "positive_reconstructed_potential":V,
    "Einstein_frame_expansion":Hhat,
    "Einstein_frame_acceleration":A
}
for name,p in checks.items():
    coeff=bernstein2(p,lo,hi)
    assert min(coeff)>0,(name,coeff)
    print("POSITIVE_BERNSTEIN2 :=",name,"LOWER_CONTROL",min(coeff))
# Dimensionless scale factors: log aE(t) = (19/20)t - (7/20)t^2
efolds=F(19,20)*(hi-lo)-F(7,20)*(hi*hi-lo*lo)
assert efolds==F(20361,200000)>F(1,10)
# Any constant b0>0 replaces b(t) by b0*exp(g(t)).
# This is not the time-dependent scalar phi. In the constructed action,
# C,D,V are unchanged and f(phi)=a(t)^(-6)/D(t) remains unchanged.
# Choose the Maxwell solution A'_w=b0 exp(g) a(t)^3 D(t);
# the source energy f(A'_w/b)^2/2=D/2 and Maxwell flux stays exactly 1.
# Hence the Einstein, Maxwell and scalar equations survive the rescaling.
# For a 5D massless spectator and a unit coordinate circle:
# m1,E/H_E=1/[b0*exp(g(t))*Hhat(t)].
b0=F(1,100)
# For t in [-.02,.09], g=-t/10+t²/2:
# |g| <= |t|/10+t²/2 <= 9/1000+81/20000 = 261/20000.
u=F(261,20000)
assert u<F(1)
# Elementary bounds exp(g) >= 1-u, exp(g) <= 1/(1-u).
# Hhat is positive and decreasing linearly.
Hmax=evaluate(Hhat,lo);Hmin=evaluate(Hhat,hi)
assert Hmax==F(241,250) and Hmin==F(887,1000)
ratio_lower=(1-u)/(b0*Hmax)
ratio_upper=1/(b0*(1-u)*Hmin)
assert ratio_lower==F(98695,964)
assert ratio_upper==F(2000000000,17508493)
assert ratio_lower>100 and ratio_upper<120
print("FULL_INTERVAL := [-1/50,9/100]")
print("EXACT_EINSTEIN_FRAME_EFOLDS :=",efolds)
print("CIRCLE_BASE_RADIUS_PARAMETER := b0 > 0 (unfixed modulus)")
print("EXACT_EQUATIONS_UNDER_b0_RESCALING := INVARIANT_BY_CONSTRUCTION")
print("EXAMPLE_b0 := 1/100")
print("FULL_INTERVAL_KK_HUBBLE_LOWER_BOUND :=",ratio_lower)
print("FULL_INTERVAL_KK_HUBBLE_UPPER_BOUND :=",ratio_upper)
print("HUBBLE_VS_SPECTATOR_FIRST_KK := GREATER_THAN_100_FOR_b0_1_OVER_100")
print("ZERO_MODE_KK_HIERARCHY := PARAMETRICALLY_ADJUSTABLE_NOT_DYNAMICAL")
print("FULL_COUPLED_KK_MODE_STABILITY := NOT_RUN")
print("RADION_STABILIZATION_AND_MICROPHYSICAL_SELECTION := OPEN")
print("CHRONOS_DISTINCTIVE_PHYSICAL_OBSERVABLE := OPEN")
