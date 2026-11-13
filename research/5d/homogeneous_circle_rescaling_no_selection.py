#!/usr/bin/env python3
"""Off-shell circle-size scaling identity for homogeneous Einstein-scalar-Maxwell.

Metric ds²=-N(t)²dt²+a(t)²dvecx²+b(t)²dw², A=A_w(t)dw, phi=phi(t).
Potential V(phi) and gauge coupling f(phi) are *arbitrary smooth functions*.
A five-dimensional parent Einstein+matter action, circle-independent.
Identity is purely algebraic and holds before field equations.
"""
from fractions import Fraction
from collections import defaultdict
if not __debug__:
    raise SystemExit("INCOMPLETE: Python assertions disabled")

# Every reduced minisuperspace monomial is represented by
# [coefficient, powers of (a, a_dot, b, b_dot, N, phi_dot, A_dot, V, f)].
names=("a","adot","b","bdot","N","phidot","Adot","V","f")
terms={
    "Einstein_a":(Fraction(-3),(1,2,1,0,-1,0,0,0,0)),
    "Einstein_b":(Fraction(-3),(2,1,0,1,-1,0,0,0,0)),
    "scalar_kinetic":(Fraction(1,2),(3,0,1,0,-1,2,0,0,0)),
    "scalar_potential":(Fraction(-1),(3,0,1,0,1,0,0,1,0)),
    "Maxwell_electric":(Fraction(1,2),(3,0,-1,0,-1,0,2,0,1)),
}
# Reduced Lagrangian (up to 2*pi coordinate circle length and boundary terms):
# -3 a*b*adot²/N -3*a²*adot*bdot/N
# +a³*b*phidot²/(2N)-N*a³*b*V(phi)
# +a³*f(phi)*Adot²/(2*N*b)
# Under (b,bdot,Adot)->(c*b,c*bdot,c*Adot), all terms -> c*L.
for name, (coefficient, powers) in terms.items():
    weight=powers[2]+powers[3]+powers[6]
    assert weight == 1,(name,weight)
    print("OFF_SHELL_SCALE_WEIGHT := ",name,weight)

def evaluate(terms, values):
    result=Fraction(0)
    for coefficient,powers in terms.values():
        t=coefficient
        for v,e in zip(values,powers):
            if e:t*=v**e
        result+=t
    return result

# Adversarial exact rational checks: arbitrary formal values f,V,
# including negative V. This is NOT the proof (the integer weights are).
cases=[
    [2,3,Fraction(1,7),Fraction(-1,3),5,7,Fraction(3,4),-2,11],
    [1,Fraction(1,9),7,2,Fraction(2,5),Fraction(-3,2),5,12,Fraction(1,10)],
    [3,2,Fraction(7,11),0,8,0,Fraction(-5,4),0,9]
]
for c in (Fraction(1,100),Fraction(5,3),117):
    for row in cases:
        scaled=row[:]
        for i in (2,3,6):scaled[i]*=c
        assert evaluate(terms,scaled)==c*evaluate(terms,row)

# The Maxwell canonical momentum for A_w is
# P_A = a³*f(phi)*Adot/(N*b), so it is exactly scale invariant.
for row in cases:
    a,adot,b,bdot,N,phidot,Adot,V,f=row
    flux=a**3*f*Adot/(N*b)
    for c in (Fraction(1,100),Fraction(7,3)):
        assert (a**3*f*(c*Adot)/(N*(c*b)))==flux

# If E_i=d/dt(∂L/∂qdot_i)-∂L/∂q_i=0, an invertible point
# transformation with L'(q')=c L(q) preserves E_i=0.
# More explicitly, E_a,E_N,E_phi scale c, while E_b,E_A are unchanged.
# Therefore it maps *all* homogeneous Euler-Lagrange solutions into
# homogeneous Euler-Lagrange solutions with the SAME V,f and Maxwell flux.
print("OFF_SHELL_LAGRANGIAN_COVARIANCE := PROVED (L_transformed=c*L)")
print("MAXWELL_CONSERVED_FLUX_COVARIANCE := PASS")
print("FULL_HOMOGENEOUS_EULER_LAGRANGE_SOLUTION_FAMILY := PROVED")
print("GLOBAL_PERIODIC_CIRCLE_CIRCUMFERENCE_CHANGES := TRUE")
print("UNIQUE_RADIUS_SELECTION_FROM_THIS_ANSATZ_ALONE := REFUTED")
print("STATIC_RADION_MASS_OR_GHOST_SPECTRUM := NOT_INFERRED")
print("GAUGE_HOLONOMY_BOUNDARY_QUANTIZATION := NOT_AUDITED")
print("ALL_W_DEPENDENT_KK_MODES := OUT_OF_SCOPE")
print("PHYSICAL_FIFTH_DIMENSION := OPEN")
