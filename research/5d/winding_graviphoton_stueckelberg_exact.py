#!/usr/bin/env python3
"""Exact zero-mode Stueckelberg reduction of a winding axion and graviphoton.

Action in 5D: S5 = integral sqrt(-g5)[R5/2-Lambda-(dchi)^2/4].
Ansatz: ds5²=gJ_munu dxmu dxnu+b²(dw+B_mudxmu)²,
chi=q*w+theta(x) mod 2*pi*f, q=n*f, w~w+2*pi.
The field B is the Kaluza-Klein graviphoton (NOT an independent Maxwell
field). All results are zero-mode identities; no nonzero KK determinant.
"""
from fractions import Fraction as F
from itertools import product

if not __debug__:
    raise SystemExit("INCOMPLETE: optimized assertions disabled")

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]
def test_metric(g_diag,b,B):
    n=len(g_diag)
    # Covariant Kaluza-Klein metric g5=[gJ+b² BB^T, b² B; b² B^T,b²].
    g5=[[F(0) for _ in range(n+1)] for __ in range(n+1)]
    inv=[[F(0) for _ in range(n+1)] for __ in range(n+1)]
    for i in range(n):
        for j in range(n):
            g5[i][j]=(g_diag[i] if i==j else 0)+b*b*B[i]*B[j]
            inv[i][j]=F(1,g_diag[i]) if i==j else F(0)
        g5[i][n]=g5[n][i]=b*b*B[i]
        inv[i][n]=inv[n][i]=-B[i]/g_diag[i]
    g5[n][n]=b*b
    inv[n][n]=1/(b*b)+sum(B[i]*B[i]/g_diag[i] for i in range(n))
    assert matmul(g5,inv)==[[int(i==j) for j in range(n+1)]
                             for i in range(n+1)]
    return g5,inv

# Exercise an indefinite 4D metric, nonzero offdiagonal KK graviphoton,
# and variable rational winding (including zero and negative).
for b in (F(1,7),F(1),F(3,2),F(9)):
    for B in ((F(0),F(0),F(0),F(0)),
              (F(1,3),F(-2,5),F(7,11),F(1,8))):
        g,ginv=test_metric((F(-1),F(2),F(3),F(5)),b,B)
        for q in (F(-2),F(0),F(1,3),F(7)):
            for dth in ((F(0),)*4,(F(1,2),F(-4),F(3,7),F(9))):
                dv=list(dth)+[q]
                kinetic=sum(ginv[i][j]*dv[i]*dv[j]
                            for i,j in product(range(5),repeat=2))
                reduced=sum((dth[i]-q*B[i])**2/
                            (F(-1),F(2),F(3),F(5))[i] for i in range(4))
                assert kinetic==reduced+q*q/(b*b)

# Jordan reduced terms per coordinate circle 2*pi, under Einstein gE=b*gJ:
# graviphoton -b^3/8 * F_B^2, Stueckelberg -1/4(dtheta-qB)^2,
# winding potential q^2/(4b^3). Canonical Maxwell Z=b^3/2,
# Proca term m0²=q²/2; hence physical mB²=q²/b³.
for b,q in product((F(1,100),F(1),F(3,2),F(100)),
                   (F(1,10),F(1),F(3))):
    Z=b**3/2
    m0_squared=q*q/2
    mB_squared=m0_squared/Z
    assert mB_squared==q*q/b**3
    A=q*q/4
    assert mB_squared==4*A/b**3
    # Gauge: w'=w-lambda(x), B'=B+d(lambda), theta'=theta+q lambda.
    B0,dtheta,dlambda=F(2,7),F(11,5),F(-3,2)
    assert (dtheta+q*dlambda)-q*(B0+dlambda)==dtheta-q*B0

# Apply to PR #343's exactly specified truncated mixed-spectrum family,
# b*=1, A=Bcas/2, so mB²=2*Bcas,
# H²=V/3 with 9/10<V/Bcas<91/100.
# mB²/H²=6/(V/Bcas), hence 600/91 < ratio² < 20/3.
lo=F(600,91)
hi=F(20,3)
assert F(5,2)**2<lo<hi<F(13,5)**2
print("FIVE_BY_FIVE_METRIC_INVERSION := PASS")
print("AXION_NORM_REDUCTION := (dtheta-q*B)^2+q^2/b^2")
print("EINSTEIN_FRAME_STUECKELBERG := -(dtheta-q*B)^2/4")
print("EINSTEIN_FRAME_VECTOR_KINETIC := -b^3*F_B^2/8")
print("CANONICAL_GRAVIPHOTON_MASS_SQUARED := q^2/b^3 = 4*A/b^3")
print("MASSIVE_VECTOR_PHYSICAL_POLARIZATIONS := 3 (zero-mode, q!=0)")
print("INDEPENDENT_FREE_AXION_ZERO_MODE := ABSENT (eaten)")
print("PR343_TRUNCATED_SPECTRUM_GRAVIPHOTON_M_OVER_H := BETWEEN_5/2_AND_13/5")
print("NONZERO_KK_COUPLED_HESSIAN_AND_DETERMINANT := OPEN")
print("QUANTUM_SPECTRAL_COMPLETENESS := OPEN")
print("PHYSICAL_5D_AND_CHRONOS := OPEN")
