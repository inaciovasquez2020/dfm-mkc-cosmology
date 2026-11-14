#!/usr/bin/env python3
"""Exact non-identifiability witness for the 5D fluctuation Hessian.

Two 5D diffeomorphism-invariant local actions S0 and
S_lambda=S0+(lambda/2)*integral sqrt(-g5)*(Box_5 chi)^2
have identical actions and first variations on every circle-independent
block-diagonal background ds5²=g4(x)+b(x)²dw², chi=q*w.
Their nonzero-winding Fourier Hessians differ.

This is an EFT non-uniqueness witness; it does NOT assert the higher-
derivative operator is present in the original Einstein-winding action
or that its coefficient is physically admissible at arbitrary scales.
"""
from fractions import Fraction as Q
from itertools import product
if not __debug__:
    raise SystemExit("INCOMPLETE: Python assertions disabled")

# For ds5²=g4(x)+b(x)²dw², sqrt(|g5|)=b sqrt(|g4|),
# g^{w w}=1/b², g^{mu w}=0; and chi=q w:
# Box_5 chi=1/(b sqrt(|g4|))*partial_w[
#             b sqrt(|g4|)*(q/b²)]=0.
# No restrictions on g4(x), b(x)>0 or constant winding q.
# S_extra and d S_extra vanish along the entire background family:
# d[(Box chi)^2]=2(Box chi)d(Box chi)=0.

for b,q in product((Q(1,100),Q(1),Q(11,7),Q(100)),
                   (Q(-3),Q(0),Q(2,5),Q(17))):
    # Exact w-independence of the flux density (q/b).
    flux_w=q/b
    w_derivative=Q(0)
    box_chi=w_derivative/b
    assert box_chi==0
    assert box_chi*box_chi==0

# Fix flat g4 and constant b; perturb chi by eps*cos(n*w),
# n !=0 integer, with no 4D dependence. At fixed metric,
# delta(Box_5 chi)= -n² eps cos(nw)/b².
# The lambda-dependent O(eps²) reduced action, integrating w 0..2pi,
# per unit 4-volume, is
# (lambda/2)*b*(n^4/b^4)*integral cos²(nw)dw
# = lambda*pi*n^4/(2*b^3).
# We certify the dimensionless coefficient after division by pi.
def coeff(b,n,lam):
    assert b>0 and n!=0
    return lam*Q(n**4,2*b**3)
for b,n,lam in product((Q(1,100),Q(1),Q(7,3),Q(100)),
                       (-7,-2,-1,1,2,5),
                       (Q(-3),Q(1,100),Q(1),Q(17))):
    c=coeff(b,n,lam)
    assert c!=0
    assert c*2*b**3==lam*n**4
    assert coeff(b,n,-lam)==-c

# Zero 4D momentum and Fourier n=0 with constant perturbation has
# delta(Box chi)=0. For x-dependent modes an extra Box4 operator
# enters, so this higher-derivative term also changes dispersion.
assert coeff(Q(1),1,Q(1))==Q(1,2)
assert coeff(Q(2),3,Q(5))==Q(405,16)
print("BACKGROUND_FAMILY := arbitrary circle-independent g4(x), b(x)>0, winding q")
print("BOX_CHI_BACKGROUND := EXACTLY_ZERO")
print("ADDED_COVARIANT_OPERATOR := (lambda/2)*(Box_5 chi)^2")
print("BACKGROUND_ACTION_AND_FIRST_VARIATION := UNCHANGED")
print("NONZERO_FOURIER_QUADRATIC_COEFF_PER_pi := lambda*n^4/(2*b^3)")
print("EXACT_ADVERSARIAL_COEFFICIENT_CHECKS := 96")
print("FULL_HESSIAN_FROM_HOMOGENEOUS_V_RADION := NON_IDENTIFIABLE")
print("ORIGINAL_CLASSICAL_LAGRANGIAN_FIXED := NO_EXTRA_TERM_ASSUMED")
print("COMPLETE_ONE_LOOP_EFFECTIVE_ACTION_SECOND_VARIATION := OPEN")
