#!/usr/bin/env python3
"""Exact rational sensitivity certificate for the fixed mixed-spectrum radion witness.
No external dependencies, floating point, or repository modifications.
This does NOT calculate the actual missing coupled determinant.
"""
if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

from fractions import Fraction as F
from math import factorial

def poly(p,z): return sum(c*z**j for j,c in enumerate(p))
N=60
elo=sum((F(5**k,factorial(k)) for k in range(N+1)),F(0))
first=F(5**(N+1),factorial(N+1))
ehi=elo+first/(1-F(5,N+2))
rlo,rhi=1/ehi,1/elo
assert 0<rlo<rhi<F(1,100)

def spectral(p,mode):
    lo=hi=F(0)
    for n in range(1,13):
        z=5*n
        c=F(poly(p,z)*z**mode,n**5)
        lo+=c*(rlo**n if c>=0 else rhi**n)
        hi+=c*(rhi**n if c>=0 else rlo**n)
    tail=260*rhi**13/(1-rhi)
    return lo-tail,hi+tail

def add(x,y): return x[0]+y[0],x[1]+y[1]
def mul(x,k): return (x[0]*k,x[1]*k) if k>=0 else (x[1]*k,x[0]*k)
P=(F(1),F(1),F(1,3))
P1=(F(0),-F(1,3),-F(1,3))
P2=(-F(1,3),-F(1,3),F(1,3))
S,S1,S2=spectral(P,0),spectral(P1,1),spectral(P2,2)
zbase=sum((F(1,n**5) for n in range(1,101)),F(0))
zeta=zbase+F(1,4*101**4),zbase+F(1,4*100**4)
G=add(mul(S,4),mul(zeta,-1)); G1=mul(S1,4);G2=mul(S2,4)
V=add(add((F(-1),F(-1)),G1),mul(G,-5))
Vpp=add(add(add((F(3),F(3)),G2),mul(G1,-10)),mul(G,30))
assert F(9,10)<V[0]<=V[1]<F(91,100)
assert F(5,4)<Vpp[0]<=Vpp[1]<F(13,10)
# Adding alpha copies of one real massless periodic boson corresponds to
# -alpha B zeta(5)/b^6. Readjust Lambda only to keep b=1 stationary.
# delta Lambda/B=+6 alpha zeta; delta V/B=+5 alpha zeta;
# delta Vpp/B=-30 alpha zeta. Exactly, alpha_crit=Vpp/(30 zeta).
threshold_lo=Vpp[0]/(30*zeta[1]);threshold_hi=Vpp[1]/(30*zeta[0])
assert threshold_lo>F(1,25)
assert threshold_hi<F(1,24), '1/24 bosonic determinant must destabilize'
stable_alpha=F(1,25)
stable_vpp=add(Vpp,mul(zeta,-30*stable_alpha))
assert stable_vpp[0]>0
alpha=F(1,24)
newv=add(V,mul(zeta,5*alpha))
newvpp=add(Vpp,mul(zeta,-30*alpha))
assert newv[0]>0 and newvpp[1]<0
print('RIGOROUS_RATIONAL_INTERVALS := PASS')
print('THRESHOLD_ALPHA_BOUNDS := 1/25 < alpha_crit < 1/24')
print('AT_ALPHA_1_OVER_25 := STATIONARY_POSITIVE_CURVATURE')
print('AT_ALPHA_1_OVER_24 := STATIONARY_POSITIVE_ENERGY_NEGATIVE_CURVATURE')
print('ZERO_MODE_STABILITY_FRAGILITY := PROVED_CONDITIONAL_ON_ADDED_FREE_BOSON_SPECTRAL_SHAPE')
print('ACTUAL_COUPLED_5D_DETERMINANT := OPEN')
print('MODEL_SCOPE := ADDITIONAL_FREE_MASSLESS_PERIODIC_BOSON_SHAPE_ONLY')
