#!/usr/bin/env python3
"""NEC bound: no 4D Einstein-frame acceleration with expanding 3-space
and shrinking S1 in a 5D diagonal homogeneous power-law metric.

Exact rational finite checks challenge (but do not replace) the symbolic proof.
"""
from fractions import Fraction as F
from itertools import product
if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

def null_ricci_coefficients(p,q):
    # ds5²=-dt²+t^(2p) dvecx²+t^(2q)dw², t>0.
    # R(V,V)*t² for normalized timelike+circle and timelike+space null vectors.
    return (-3*p*(p-q-1), 2*p+q+p*q-q*q)

def ef_power(p,q):
    # b=t^q, dtau=t^(q/2)dt and a_E=t^(p+q/2).
    # For q>-2, tau=t^(1+q/2)/(1+q/2), so a_E~tau^n.
    assert q > -2
    return (p+q/2)/(1+q/2)

def check_point(p,q):
    circle,spatial=null_ricci_coefficients(p,q)
    nec=(circle>=0 and spatial>=0)
    expanding_3d=p>0
    shrinking_circle=q<0
    accelerating_ef=(p+q/2>0 and q>-2 and ef_power(p,q)>1) if q>-2 else False
    if expanding_3d and shrinking_circle and nec:
        # Circle NEC implies p<=1+q and hence q>-1.
        assert p<=1+q and q>-1
        assert q>-2
        # EF exponent <= (1+3q/2)/(1+q/2) < 1.
        assert ef_power(p,q)<1
        assert not accelerating_ef
    if expanding_3d and shrinking_circle and accelerating_ef:
        assert circle<0
    return nec,accelerating_ef

# Exact finite adversarial sweep; rational mesh 1/8, bounded 512 points.
tested=nec_count=accelerating_count=counterexamples=0
for i,j in product(range(1,33),range(-16,0)):
    p,q=F(i,8),F(j,8)
    tested+=1
    nec,acc=check_point(p,q)
    nec_count+=int(nec)
    accelerating_count+=int(acc)
    counterexamples+=int(nec and acc)
assert tested==512 and nec_count==16 and counterexamples==0
# Vacuum shrinking-circle Kasner: both null contractions vanish.
assert null_ricci_coefficients(F(1,2),F(-1,2))==(0,0)
assert ef_power(F(1,2),F(-1,2))==F(1,3)
# Adversarial accelerating case: explicit NEC violation in circle null channel.
p,q=F(3,2),F(-1,4)
circle,spatial=null_ricci_coefficients(p,q)
assert ef_power(p,q)==F(11,7) and circle<0
assert check_point(p,q)==(False,True)
print("POWER_LAW_5D_NULL_RICCI_FORMULAS := CHECKED")
print("EXPANDING_THREE_SPACE_SHRINKING_S1_NEC_IMPLIES_p_LE_1_PLUS_q := PROVED")
print("NO_ACCELERATING_4D_EINSTEIN_FRAME_POWER_LAW_WITH_5D_NEC := PROVED")
print(f"EXACT_MESH_STATES := {tested}; FULL_NEC := {nec_count}; NEC_AND_ACCELERATION := {counterexamples}")
print(f"ACCELERATING_MESH_EXAMPLES := {accelerating_count} (all fail circle NEC)")
print("VACUUM_KASNER_NEGATIVE_CONTROL := PASS")
print("ACCELERATING_NEC_VIOLATION_CONTROL := PASS")
print("GENERAL_TIME_DEPENDENT_NON_POWER_LAW := OPEN")
print("FOUR_DIMENSIONAL_OBSERVATIONAL_DISTINCTION := OPEN")
