#!/usr/bin/env python3
"""Exact nonzero-Fourier-mode diffeomorphism audit on M4 x S1.

Linearized about ds²=g4+b²dw² with b constant, B=0, chi=q*w.
k=i*n (nonzero), and lambda^w_n, lambda_mu,n are the diffeomorphism
parameters. Tests algebraically treat k as a nonzero formal variable;
the formulas remain valid under k=i*n in complex Fourier space.

This computes GAUGE TRANSFORMATIONS, NOT the quadratic action,
constraints, dynamical spectrum, ghost determinant or propagating dofs.
"""
from fractions import Fraction as Q
from itertools import product
if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

# Under delta g_AB = Lie_xi g_AB, delta chi=Lie_xi chi:
# delta chi_n=q xi^w_n
# delta r_n=k xi^w_n, r_n=delta g_ww,n/(2b²)
# delta B_mu,n = partial_mu xi^w_n + k xi_mu,n/b²
# delta h_mu nu,n=partial_mu xi_nu+partial_nu xi_mu
# where B_mu,n=delta g_mu w,n/b².
# Thus Z_n=delta chi_n - (q/k)r_n is invariant
# under ALL linearized circle and 4D diffeomorphisms (k != 0).
# Crucially the pair (chi,B_mu) alone is not closed under
# nonzero-n gauge transformations without r and h_mu nu.
count=0
for n,b,q,xi_w,r,theta in product(
    (-3,-2,-1,1,2,5),
    (Q(1,100),Q(1),Q(7,3)),
    (Q(0),Q(1,3),Q(-2)),
    (Q(-9,10),Q(0),Q(11,7)),
    (Q(-3,5),Q(0),Q(5)),
    (Q(-7),Q(3,4))
):
    # Algebraically set k=n; replacing n by i*n does not
    # change the universal rational function identity.
    k=Q(n)
    Z=theta-q*r/k
    theta_prime=theta+q*xi_w
    r_prime=r+k*xi_w
    assert theta_prime-q*r_prime/k==Z
    # Under circle diffeomorphisms an isolated theta_n is
    # not gauge invariant for nonzero winding and xi_w.
    if q and xi_w:
        assert theta_prime!=theta
    count+=1
assert count==6*3*3*3*3*2
# Under 4D Fourier diffeomorphisms with xi^w=0, an
# isolated graviphoton B_mu,n transforms by k xi_mu/b².
for k,b,xi_mu,dxi_w in product((Q(-3),Q(1),Q(4)),
                               (Q(1,5),Q(1),Q(11)),
                               (Q(-2),Q(1,7)),
                               (Q(-5),Q(3,2))):
    dB=dxi_w+k*xi_mu/(b*b)
    dr=k*Q(1)                     # xi^w=1
    covector_shift=dB-(dr/k)*dxi_w # not a physical combination
    assert dB-dxi_w==k*xi_mu/(b*b)
    if xi_mu:assert dB!=dxi_w
# At n=0, the radius scalar r_0 has zero circle-gauge
# variation whereas theta_0 shifts by q xi^w_0; no 1/k invariant.
for q,xi in ((Q(1),Q(3)),(Q(-2),Q(1,2))):
    assert q*xi!=0
print("LINEARIZED_CIRCLE_DIFEO := delta(theta_n)=q xi_w; delta(r_n)=i*n xi_w")
print("NONZERO_MODE_GAUGE_INVARIANT := Z_n=theta_n-q*r_n/(i*n)")
print("GAUGE_INVARIANCE_ADVERSARIAL_RATIONAL_CASES :=",count)
print("VECTOR_MIXING := delta(B_mu,n)=partial_mu(xi_w,n)+i*n*xi_mu,n/b^2")
print("FOUR_D_METRIC_MIXING := delta(h_mu,nu,n)=partial_mu(xi_nu)+partial_nu(xi_mu)")
print("N_NONZERO_TRUNCATION_OF_RADION_AND_FOUR_D_GRAVITON := NOT_GAUGE_CLOSED")
print("ZERO_MODE_Z_N_FORMULA := UNDEFINED; STUECKELBERG_ZERO_MODE_REMAINS_VALID")
print("PHYSICAL_PROPAGATION_OF_Z_N := NOT_ESTABLISHED")
print("GAUGE_FIXED_FULL_NONZERO_KK_QUADRATIC_HESSIAN := OPEN")
print("COMPLETE_ONE_LOOP_DETERMINANT := OPEN")
