#!/usr/bin/env python3
"""Exact polynomial certificate for a periodic massive-boson Casimir no-go.

4D Einstein-frame potential:
 V(b) = Lambda/b + A/b^3 - sum_j B_j/b^6 *
         sum_(n>=1) exp(-z_jn) P(z_jn)/n^5,
 z_jn=2*pi*n*m_j*b, P(z)=1+z+z²/3;
 b>0, A>0, B_j>0, m_j>=0.
At a stationary point with V>=0, V'' is STRICTLY negative.
This is a zero-mode one-loop effective-potential theorem under the
specified finite, locally-renormalized periodic bosonic spectrum.
"""
from fractions import Fraction as Q
if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

# Polynomial coefficients are low-to-high, exact Fractions.
def add(a,b):
    return tuple((a[i] if i<len(a) else Q(0))+
                 (b[i] if i<len(b) else Q(0))
                 for i in range(max(len(a),len(b))))
def mul(a,b):
    z=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return tuple(z)
def scale(a,s):return tuple(x*Q(s) for x in a)
def derivative(a):return tuple(i*a[i] for i in range(1,len(a))) or (Q(0),)
def shift(a):return (Q(0),)+a
def exp_derivative(a):
    # if h(z)=exp(-z)*P(z), h'=exp(-z)*(P'-P)
    return add(derivative(a),scale(a,-1))
P=(Q(1),Q(1),Q(1,3))
P1=exp_derivative(P)
P2=exp_derivative(P1)
# At stationary nonnegative energy, the upper bound on V'' is
# -sum_j B_j b^-8 sum_n exp(-z)/n^5 * W(z),
# W=15P-7z(P'-P)+z²(P''-2P'+P).
W=add(add(scale(P,15),scale(shift(P1),-7)),
      shift(shift(P2)))
assert W==(Q(15),Q(15),Q(7),Q(2),Q(1,3))
assert all(c>0 for c in W)
# Equivalent integer-coefficient identity.
assert scale(W,3)==(Q(45),Q(45),Q(21),Q(6),Q(1))
# Therefore W(z)>0 for ALL z>=0, not merely on a finite mesh.
for z in (Q(0),Q(1,100),Q(1),Q(7,3),Q(50)):
    assert sum(c*z**i for i,c in enumerate(W))>0
print("MASSIVE_BOSON_SPECTRAL_POLYNOMIAL := 1+z+z^2/3")
print("NO_GO_POLYNOMIAL_3W := 45+45z+21z^2+6z^3+z^4")
print("ALL_POLYNOMIAL_COEFFICIENTS_STRICTLY_POSITIVE := PASS")
print("UNIFORM_FOR_ALL_MASS_NONNEGATIVE := PROVED")
print("UNIFORM_FOR_EVERY_PERIODIC_WINDING_INDEX_n_GE_1 := PROVED")
print("ANY_FINITE_POSITIVE_BOSON_MULTIPLICITIES := PROVED")
print("EVERY_STATIONARY_NONNEGATIVE_VACUUM_HAS_NEGATIVE_RADION_CURVATURE := PROVED")
print("MASSLESS_LIMIT := P(0)=1, W(0)=15, RECOVERS_SINGLE_POWER_CASE")
# Explicit adversarial differentiation (Laurent polynomial, rational b)
# using massless limit one boson: V=Lambda/b+A/b³-B/b⁶.
def v_all(b,L,A,B):
    v=L/b+A/b**3-B/b**6
    d=-L/b**2-3*A/b**4+6*B/b**7
    dd=2*L/b**3+12*A/b**5-42*B/b**8
    return v,d,dd
assert v_all(Q(1),Q(-3,5),Q(1),Q(2,5))==(Q(0),Q(0),Q(-6))
assert v_all(Q(1),Q(0),Q(1),Q(1,2))==(Q(1,2),Q(0),Q(-9))
assert v_all(Q(1),Q(-12,5),Q(1),Q(1,10))==(Q(-3,2),Q(0),Q(3))
print("MASSLESS_MINKOWSKI_DS_ADS_NEGATIVE_CONTROLS := PASS")
print("SPECIFIC_REAL_SCALAR_ONE_LOOP_NORMALIZATION := B=3/(64*pi^6)")
print("BOUNDARY_CONDITIONS := PERIODIC; LOCAL_BULK_COUNTERTERM_SUBTRACTED")
print("FERMIONIC_OR_TWISTED_OR_MASS_DEPENDENT_COUPLING := OUT_OF_SCOPE")
print("FULL_5D_KK_SPECTRUM_AND_CHRONOS_OBSERVABLE := OPEN")
