#!/usr/bin/env python3
"""Rigorous rational enclosures of a mixed periodic boson/fermion radion dS minimum.

Field content: one periodic massless real scalar, one periodic massive 5D
Dirac fermion (four real-spin degrees), and a circle-winding compact scalar.
One-loop Einstein-frame V(b)=Lambda/b+A/b^3 + B*(4*S(m*b)-zeta(5))/b^6,
B=3/(64*pi^6), S(x)=sum_(n>=1) exp(-2*pi*n*x)*P(2*pi*n*x)/n^5,
P(z)=1+z+z²/3. Parameters: b*=1, 2*pi*m=5, A=B/2.
The bare bulk Lambda is fixed analytically by V'(1)=0.
No floating point, external dependencies, finite-grid inference or network.
"""
from fractions import Fraction as F
from math import factorial
if not __debug__:
    raise SystemExit("INCOMPLETE: -O disables assertions")

def evaluate(poly,z):
    return sum(c*z**j for j,c in enumerate(poly))

P=(F(1),F(1),F(1,3))
P1=(F(0),-F(1,3),-F(1,3))  # (exp(-z)*P)' / exp(-z)
P2=(-F(1,3),-F(1,3),F(1,3)) # second derivative after factoring exp(-z)

# Bound exp(-5) by reciprocal Taylor sums of exp(5).
# For k>N the Taylor tail is <= first_omitted/(1-5/(N+2)).
N=60
Elo=sum(F(5**k,factorial(k)) for k in range(N+1))
first=F(5**(N+1),factorial(N+1))
Ehi=Elo+first/(1-F(5,N+2))
rlo,rhi=1/Ehi,1/Elo
assert 0<rlo<rhi<F(1,100)

def spectral(poly,mode):
    lo=hi=F(0)
    for n in range(1,13):
        z=5*n
        c=F(evaluate(poly,z),n**5)*z**mode
        lo+=c*(rlo**n if c>=0 else rhi**n)
        hi+=c*(rhi**n if c>=0 else rlo**n)
    # For n>=13, each of |P(5n)|, |5n P1(5n)|, and
    # |(5n)^2 P2(5n)|, divided by n^5, is < 260.
    # Sum geometric bound with rhi<1/100, preserving all tail terms.
    tail=F(260)*rhi**13/(1-rhi)
    return lo-tail,hi+tail

S=spectral(P,0)
S1=spectral(P1,1) # b*d/db S at b=1
S2=spectral(P2,2) # b²*d²/db² S at b=1

# 100 terms of zeta(5) plus rigorous integral-test tail.
M=100
zbase=sum(F(1,n**5) for n in range(1,M+1))
zeta=zbase+F(1,4*(M+1)**4),zbase+F(1,4*M**4)

def plus(a,b):return a[0]+b[0],a[1]+b[1]
def times(a,c):
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)

G=plus(times(S,4),times(zeta,-1))
G1=times(S1,4)
G2=times(S2,4)
# V = Lambda/b + A/b³ + B*G(b)/b^6, with A=B/2,
# G(b)=4*S(m*b)-zeta(5).
# Exact stationarity sets Lambda/B=-3/2+G1-6G.
# At b=1: V/B=-1+G1-5G; V''/B=3+G2-10G1+30G.
lam=plus(plus(G1,times(G,-6)),(F(-3,2),F(-3,2)))
V=plus(plus(G1,times(G,-5)),(F(-1),F(-1)))
V2=plus(plus(plus(G2,times(G1,-10)),times(G,30)),
        (F(3),F(3)))

assert F(1)<lam[0]<=lam[1]<F(11,10)
assert F(9,10)<V[0]<=V[1]<F(91,100)
assert F(5,4)<V2[0]<=V2[1]<F(13,10)
# Canonical radion phi=sqrt(3/2)log b: m_phi²=(2/3)*b²*V''.
assert times(V2,F(2,3))[0]>0
# On a de Sitter stationary point H_E²=V/3 and radion m_phi²=2V''/3.
# Thus (m_phi/H_E)²=2V''/V. Interval bounds show a positive but
# Hubble-scale radion, not a second parametrically decoupled mode.
radH2_lo=2*V2[0]/V[1]
radH2_hi=2*V2[1]/V[0]
assert radH2_lo>F(33,20)**2
assert radH2_hi<F(17,10)**2
print("RADION_MASS_OVER_H := STRICTLY_BETWEEN_33/20_AND_17/10")

# B=3/(64*pi^6), and pi>3 implies B<1/10000.
# For this normalization m1,KK,E=1 (b=1) while H²=V/3.
# Hence m1,KK,E/H > sqrt(3*10000/.91) > 100.
assert 3*F(91,100)<F(3) and F(3,64*3**6)<F(1,10000)
assert (F(91,100)*F(1,10000))/3 < F(1,10000)
print("SPECTRAL_EXPONENTIAL_AND_ZETA_TAILS := RIGOROUS_FRACTION_BOUNDS")
print("FIELD_CONTENT := ONE_PERIODIC_MASSLESS_REAL_SCALAR_PLUS_ONE_PERIODIC_MASSIVE_5D_DIRAC")
print("FERMION_MASS := 5/(2*pi); WINDING_COEFFICIENT_A := B/2")
print("STATIONARITY := LAMBDA/B=-3/2+G1-6G (EXACT_DEFINITION)")
print("CERTIFIED_LAMBDA_OVER_B := 1 < ratio < 11/10")
print("CERTIFIED_V_OVER_B := 9/10 < ratio < 91/100")
print("CERTIFIED_V_SECOND_OVER_B := 5/4 < ratio < 13/10")
print("RADION_LOCAL_MINIMUM_AND_POSITIVE_VACUUM := PROVED")
print("SPECTATOR_KK_MASS_OVER_H := GREATER_THAN_100_IN_CHOSEN_NORMALIZATION")
print("FULL_QUANTUM_OR_COUPLED_KK_STABILITY := NOT_RUN")
print("COSMOLOGICAL_CONSTANT_AND_WINDING_F_PARAMETER_SELECTION := TUNED")
print("PHYSICAL_5D_AND_CHRONOS_DISTINCTIVENESS := OPEN")
