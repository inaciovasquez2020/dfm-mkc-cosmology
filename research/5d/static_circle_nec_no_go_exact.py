#!/usr/bin/env python3
"""Exact NEC obstruction for an unwarped static S1 times dS4 in 5D Einstein gravity.

Uses only Python's Fraction. Source matter may be arbitrary; assumes Einstein
equations, an exact direct-product metric, and an everywhere-flat circle.
This does NOT address warp factors, varying radius, higher curvature or EFT.
"""
from fractions import Fraction as F

if not __debug__:
    raise SystemExit("INCOMPLETE: optimization disables assert checks")

def null_contractions(k, b2):
    """For g=diag(-1,1,1,1,b2), null v=(1,0,0,0,1/sqrt(b2)).
    
    Avoid square roots using v^w²=1/b2. Ric4=3k*g4, Ric_ww=0.
    """
    assert b2 > 0
    metric_null = F(-1) + b2/b2
    ricci_null = -3*k
    return metric_null,ricci_null

def tensor_nec(k,b2,kappa2=F(1)):
    metric_null,ricci_null=null_contractions(k,b2)
    assert metric_null==0 and kappa2>0
    # Cosmological constant vanishes on null contraction.
    return ricci_null/kappa2

for k,b2 in [(F(1,3),F(3,2)),(F(1,10),F(1,7)),
             (F(0),F(7,3)),(F(-1,3),F(2,1))]:
    nn=tensor_nec(k,b2)
    assert (nn<0)==(k>0)
    assert (nn==0)==(k==0)
    assert (nn>0)==(k<0)
print("NULL_VECTOR_METRIC_CONTRACTION := ZERO")
print("NULL_RICCI_CONTRACTION := -3*k (every b2>0)")
print("LAMBDA_CONTRIBUTION_ON_NULL_VECTOR := ZERO")
print("NEC_IMPLIES_k_NONPOSITIVE := PASS")
print("STATIC_UNWARPED_DS4_S1_WITH_NEC := IMPOSSIBLE")

# NEC-satisfying winding scalar with coefficient -g^AB dchi_A dchi_B /4:
# for w-gradient q, T(v,v) = q²/(2b²)>0, contradicting k>0.
for b2,q in [(F(1),F(1)),(F(3,2),F(1)),(F(7,3),F(2))]:
    assert q*q/(2*b2)>0
    # Einstein null equation forces k = -q²/(6*b²) for canonical winding.
    k=-q*q/(6*b2)
    assert tensor_nec(k,b2)==q*q/(2*b2)
    assert k<0

# Adversarial limiting example: a WRONG-SIGN scalar can evade the NEC gate.
# Stress tensor for ghost winding gives T(v,v)=-q²/(2b²).
# Einstein equations solve k=q²/(6b²), Lambda5=3q²/(4b²).
b2,q2=F(1),F(2)
k=q2/(6*b2)
lam=3*q2/(4*b2)
Q=q2/(4*b2)
assert k==F(1,3) and lam==F(3,2)
assert 3*k==lam-Q and -6*k+lam==-Q
assert tensor_nec(k,b2)==-q2/(2*b2)<0
print("CANONICAL_WINDING_NEGATIVE_CURVATURE := PASS")
print("WRONG_SIGN_GHOST_COUNTERMODEL := PASS (unphysical; violates NEC)")
print("WARPED_OR_TIME_DEPENDENT_COMPACTIFICATIONS := OUT_OF_SCOPE")
print("GAUSS_BONNET_MODIFIED_FIELD_EQUATIONS := OUT_OF_SCOPE")
print("PHYSICAL_5D_NECESSITY := OPEN")
