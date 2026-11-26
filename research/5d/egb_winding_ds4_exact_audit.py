#!/usr/bin/env python3
"""Exact 5D Einstein-Gauss-Bonnet + winding scalar dS4 x circle benchmark.

Pure Python fractions; no dependencies, external data, or repository writes.
Background field equations only. NO ghost/hyperbolicity/full stability result.
"""
from fractions import Fraction as F
from itertools import product

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled by -O")

D = 5
sig = (-1, 1, 1, 1, 1)
k = F(1, 3)
alpha = F(-1)
lam = F(5, 6)
q = F(1)
b_squared = F(3, 2)
Q = q*q/(4*b_squared)
assert Q == F(1,6)
assert k > 0 and lam > 0 and b_squared > 0

# Full Riemann curvature in an orthonormal frame for dS4(k) x S1(b).
# R_abcd=k(g_ac g_bd-g_ad g_bc) for indices in {0,1,2,3};
# every component with circle index 4 vanishes.
def riem(a, b, c, d):
    if 4 in (a,b,c,d):
        return F(0)
    return k * sig[a] * sig[b] * (
        int(a==c and b==d) - int(a==d and b==c)
    )

ric = {(a,b):sum(sig[c]*riem(c,a,c,b) for c in range(D))
       for a,b in product(range(D), repeat=2)}
scalar = sum(sig[a]*ric[a,a] for a in range(D))
ric2 = sum(sig[a]*sig[b]*ric[a,b]**2
           for a,b in product(range(D), repeat=2))
riem2 = sum(sig[a]*sig[b]*sig[c]*sig[d]*riem(a,b,c,d)**2
            for a,b,c,d in product(range(D), repeat=4))
GB = riem2-4*ric2+scalar*scalar
assert scalar == 12*k and GB == 24*k*k

def lanczos(a,b):
    # H_ab=2(R Ric_ab -2Ric_ac Ric_b^c -2 Ric^cd R_acbd
    #          + R_a^cde R_bcde)-g_ab GB/2.
    v=scalar*ric[a,b]
    v-=2*sum(sig[c]*ric[a,c]*ric[b,c] for c in range(D))
    v-=2*sum(sig[c]*sig[d]*ric[c,d]*riem(a,c,b,d)
             for c,d in product(range(D),repeat=2))
    v+=sum(sig[c]*sig[d]*sig[e]*riem(a,c,d,e)*riem(b,c,d,e)
           for c,d,e in product(range(D),repeat=3))
    return 2*v-F(1,2)*sig[a]*int(a==b)*GB

assert all(lanczos(a,b)==(F(-12)*k*k if a==b==4 else F(0))
           for a,b in product(range(D),repeat=2))

# Action S=∫sqrt(-g)[R/2-Lambda5+alpha GB/2-(dchi)^2/4].
# chi=q*w mod 2*pi, q integer; (dchi)_4^2=q^2/b^2.
# G_AB+Lambda5*g_AB+alpha*H_AB
# = (1/2)(dchi)_A(dchi)_B - (1/4)g_AB(dchi)^2.
for a,b in product(range(D),repeat=2):
    g_ab=sig[a]*int(a==b)
    Einstein=ric[a,b]-F(1,2)*scalar*g_ab
    stress=(F(1,2)*q*q/b_squared if a==b==4 else F(0))-Q*g_ab
    residual=Einstein+lam*g_ab+alpha*lanczos(a,b)-stress
    assert residual == 0, (a,b,residual)

assert 3*k == lam+Q
assert -6*k+lam-12*alpha*k*k == Q

# Constant-radius branch from independent equation elimination:
# Q=-(3/2)k-6alpha*k^2, Lambda=(9/2)k+6alpha*k^2.
assert Q == -F(3,2)*k-6*alpha*k*k
assert lam == F(9,2)*k+6*alpha*k*k

# Linearized Jordan-frame trace + scalar equation on a maximally
# symmetric 4D background gives, for C=1+4alpha*k not zero,
# (Box-m_radion,J^2) delta b=0, with
# m^2 = 4 Q (1+2C)/(3C^2).
# This is a formal mode equation; NO full kinetic/ghost audit is inferred.
C=1+4*alpha*k
assert C==F(-1,3)
mass_J2=4*Q*(1+2*C)/(3*C*C)
assert mass_J2==F(2,3)>0
# 4D Jordan de Sitter radius squared is 1/k.
assert mass_J2/k == 2

print("EGB_LOVEL0CK_25_TENSOR_RESIDUALS := PASS")
print("GAUSS_BONNET_SCALAR := 8/3")
print("EXACT_DS4_X_S1_BACKGROUND := PASS")
print("LAMBDA5 := 5/6; ALPHA_GB := -1; WINDING := 1")
print("DS4_CURVATURE_K := 1/3; CIRCLE_RADIUS_SQUARED := 3/2")
print("LINEARIZED_RADION_TRACE_SCALAR_MASS_JORDAN_SQUARED := 2/3 (FORMAL)")
print("FULL_GHOST_HYPERBOLICITY_KK_STABILITY := OPEN")
print("CHRONOS_EVENT_OBSERVABLE_TRANSFER := OPEN")
print("PHYSICAL_FIFTH_DIMENSION := NOT_ESTABLISHED")
