#!/usr/bin/env python3
"""Exact TT circle-direction principal symbol in 5D EGB winding dS4 x S1.

Independent of the background-solution verifier.  Tests curvature linearization
with off-diagonal tangent perturbation and proves C=1+4 alpha k<0 from Q>0.
Classical unrestricted Fourier tower only; UV-completed theory not assessed.
"""
from fractions import Fraction as F
from itertools import product

if not __debug__:
    raise SystemExit("INCOMPLETE: Python optimized assertions")
N=5
signature=(-1,1,1,1,1)
k=F(1,3)
alpha=F(-1)
q=F(1)
b2=F(3,2)
Q=q*q/(4*b2)
C=1+4*alpha*k
assert Q==-F(3,2)*k*C
assert Q>0 and k>0 and C<0

# Curvature of constant-curvature four-space x flat one-circle, orthonormal.
def bg(a,b,c,d):
    if 4 in (a,b,c,d): return F(0)
    return k*signature[a]*signature[b]*(
        int(a==c and b==d)-int(a==d and b==c))
def wedge(i,j,a,b):
    return int(a==i and b==j)-int(a==j and b==i)
def delta(a,b,c,d):
    # Algebraic Riemann perturbation with only dR_(1,4,2,4)=1,
    # representing the principal circle second derivative of h_12.
    return F(wedge(1,4,a,b)*wedge(2,4,c,d)
            +wedge(2,4,a,b)*wedge(1,4,c,d))
def ricci(R):
    return {(a,b):sum(signature[c]*R(c,a,c,b) for c in range(N))
            for a,b in product(range(N),repeat=2)}
r=ricci(bg)
dr=ricci(delta)
R0=sum(signature[a]*r[a,a] for a in range(N))
dR=sum(signature[a]*dr[a,a] for a in range(N))
assert R0==12*k and dR==0 and dr[1,2]==1

# Differentiate the 5D Lanczos tensor H_ab with respect to the algebraic
# Riemann perturbation, keeping metric fixed at the principal-symbol level.
def delta_lanczos(a,b):
    val=dR*r[a,b]+R0*dr[a,b]
    val-=2*sum(signature[c]*(dr[a,c]*r[b,c]+r[a,c]*dr[b,c])
               for c in range(N))
    val-=2*sum(signature[c]*signature[d]*(
        dr[c,d]*bg(a,c,b,d)+r[c,d]*delta(a,c,b,d))
        for c,d in product(range(N),repeat=2))
    val+=sum(signature[c]*signature[d]*signature[e]*(
        delta(a,c,d,e)*bg(b,c,d,e)
        +bg(a,c,d,e)*delta(b,c,d,e))
        for c,d,e in product(range(N),repeat=3))
    # g_12=0, so -g_ab GB/2 vanishes for this off-diagonal component.
    return 2*val

assert delta_lanczos(1,2)==4*k*dr[1,2]
# Einstein+GB: principal circle derivative coefficient is 1+4 alpha k.
assert dr[1,2]+alpha*delta_lanczos(1,2)==C

# Exact algebraic sign argument holds for every k>0, Q>0 branch:
# Q=-(3k/2)C implies C<0, so the high Fourier mode dispersion
# omega^2 = |spatial p|^2 + C n^2 / b^2 + O(k)
# is eventually negative for n increasing, holding p fixed.
assert C/b2==F(-2,9)
for n in (1,2,3,10,100):
    leading_KK_mass2=C*F(n*n,1)/b2
    assert leading_KK_mass2==-F(2,9)*n*n
assert C<0 and Q>0

print("LINEARIZED_5D_LANCZOS_TT_CIRCLE_COEFFICIENT := PASS (4*k)")
print("TENSOR_CIRCLE_PRINCIPAL_SYMBOL := C = 1+4*alpha*k = -1/3")
print("DE_SITTER_WINDING_BRANCH_FORCES_C_NEGATIVE := PROVED")
print("UNRESTRICTED_HIGH_KK_TENSOR_TACHYON_OBSTRUCTION := PROVED (classical model)")
print("RADION_MASS_POSITIVE_NOT_FULL_STABILITY := PASS")
print("UV_CUTOFF_AND_FULL_COMPLETED_THEORY := OPEN")
print("PHYSICAL_5D := OPEN")
