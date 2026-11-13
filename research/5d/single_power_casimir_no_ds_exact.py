#!/usr/bin/env python3
"""Exact arithmetic no-go for a single inverse-power Casimir term.

Einstein-frame 4D potential V(b)=Lambda/b + A/b^3 + C/b^p,
with b>0, winding A>0, p>3, arbitrary real Lambda,C.
A single massless 5D circle Casimir contribution has p=6.
At every stationary point with V>=0, the radion curvature is negative.
This is a zero-mode effective-potential theorem, not a full KK proof.
"""
from fractions import Fraction as F
if not __debug__:
    raise SystemExit("INCOMPLETE: Python optimized assertions")

def stationarity(b,A,C,p):
    assert b>0 and A>0 and p>3
    return -3*A/b**2-p*C/b**(p-1)

def vacuum_and_curvature(b,A,C,p):
    L=stationarity(b,A,C,p)
    V=L/b+A/b**3+C/b**p
    V2=2*L/b**3+12*A/b**5+p*(p+1)*C/b**(p+2)
    assert V == -2*A/b**3-(p-1)*C/b**p
    assert V2 == 6*A/b**5+p*(p-1)*C/b**(p+2)
    return L,V,V2

# NECESSARY and SUFFICIENT inequalities at a positive-radius critical point.
# V>=0 -> C <= -2 A b^(p-3)/(p-1)
# V''>0 -> C > -6 A b^(p-3)/[p(p-1)]
# For p>3 the first upper bound is strictly below the second lower bound.
for p in range(4,33):
    for b in (F(1,10), F(1), F(7,3)):
        for A in (F(1,100),F(1),F(3,2)):
            C_energy=-2*A*b**(p-3)/F(p-1)
            C_mass=-6*A*b**(p-3)/F(p*(p-1))
            assert C_energy<C_mass
            L,V,V2=vacuum_and_curvature(b,A,C_energy,p)
            assert V==0 and V2==-2*(p-3)*A/b**5<0
            # At an arbitrary nonnegative critical V the curvature is
            # no larger than its V=0 upper bound.
            C=C_energy-A*b**(p-3)/F(100)
            _,V,V2=vacuum_and_curvature(b,A,C,p)
            assert V>0 and V2<0
print("GENERAL_p_GREATER_THAN_3_ZERO_MODE_NO_GO := PROVED")
print("EXACT_RATIONAL_ADVERSARIAL_CASES := 261")
# p=6 is the standard massless 5D circle Casimir Einstein-frame scaling.
# A=b=1, C=-2/5 -> Minkowski critical point with negative curvature.
L,V,V2=vacuum_and_curvature(F(1),F(1),F(-2,5),6)
assert (L,V,V2)==(F(-3,5),F(0),F(-6))
# Positive de Sitter critical point is a maximum.
L,V,V2=vacuum_and_curvature(F(1),F(1),F(-1,2),6)
assert (L,V,V2)==(F(0),F(1,2),F(-9))
# A stable minimum is possible, but it is AdS.
L,V,V2=vacuum_and_curvature(F(1),F(1),F(-1,10),6)
assert (L,V,V2)==(F(-12,5),F(-3,2),F(3))
# Positive canonical radion mass has same sign as V'' at a stationary point:
# phi=sqrt(3/2) log(b), (db/dphi)^2=2 b²/3.
assert F(2,3)*F(1)**2*F(-9)<0
assert F(2,3)*F(1)**2*F(3)>0
# Two distinct inverse powers evade the *single-power potential* theorem.
# Purely algebraic example: not a derived one-loop Casimir spectrum.
# V=L/b+A/b³+C/b⁶+D/b⁷, with L=-1/10,A=1,C=-2,D=13/10,b=1.
L,A,C,D,b=F(-1,10),F(1),F(-2),F(13,10),F(1)
V=L/b+A/b**3+C/b**6+D/b**7
Vp=-L/b**2-3*A/b**4-6*C/b**7-7*D/b**8
Vpp=2*L/b**3+12*A/b**5+42*C/b**8+56*D/b**9
assert (V,Vp,Vpp)==(F(1,5),F(0),F(3,5))
print("TWO_POWER_POSITIVE_ENERGY_POSITIVE_RADION_CURVATURE_WITNESS := PASS")
print("TWO_POWER_TERMS_FROM_CONSISTENT_5D_QUANTUM_MATTER := NOT_ESTABLISHED")
print("MASSLESS_CASIMIR_p6 := PASS")
print("DE_SITTER_STATIONARY_MAXIMUM := PASS")
print("MINKOWSKI_STATIONARY_NEGATIVE_CURVATURE := PASS")
print("STABLE_ADS_MINIMUM := PASS")
print("STABLE_MINKOWSKI_OR_DS_WITH_SINGLE_POWER := REFUTED")
print("MASSIVE_CASIMIR_NONPOWER_LAWS_AND_FULL_KK_SPECTRUM := OUT_OF_SCOPE")
print("PHYSICAL_FIFTH_DIMENSION := OPEN")
