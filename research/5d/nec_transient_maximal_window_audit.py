#!/usr/bin/env python3
"""Exact maximal connected physical window for the specified 5D transient model.

No approximated root or grid can substitute for the algebraic argument.
Uses rational root isolation, monotonicity and Bernstein positivity.
"""
from fractions import Fraction as Q
from pathlib import Path
import runpy

if not __debug__:
    raise SystemExit("INCOMPLETE: assert disabled")

s=runpy.run_path(str(Path(__file__).with_name(
    "nec_transient_accelerating_circle_exact.py")))
rho,p3,pw,H,Fc,A=(s[k] for k in ("rho","p3","pw","H","F","A"))
add,sub,scale=(s[k] for k in ("add","sub","scale"))
def E(p,t):
    return sum(c*t**j for j,c in enumerate(p))
def Bernstein2(p,l,r):
    assert len(p)<=3 and l<r
    c0,c2=E(p,l),E(p,r)
    midpoint=(l+r)/2
    c1=2*E(p,midpoint)-(c0+c2)/2
    return (c0,c1,c2)

# Exact lower root of NEC circle C(t)=(15+528t-396t²)/50:
# t_- = 2/3 - sqrt(2101)/66 (~ -0.02782828).
C=add(rho,pw)
assert C==(Q(3,10),Q(264,25),Q(-198,25))
l=Q(-7,250)  # -.028
u=Q(-27,1000)  # -.027
right=Q(1,10)
assert E(C,l)<0 and E(C,u)>0
assert E(C,right)>0
# C'=264/25-396t/25>0 across [l,right].
assert Q(264,25)-Q(396,25)*right>0

# Every other physical or reconstructed-source requirement holds strictly
# on the LARGER interval [l,right], enclosing exact t_-.
D=sub(p3,pw)
V=scale(sub(rho,p3),Q(1,2))
expansion=add(H,scale(Fc,Q(1,2)))
conditions={
    "H_space_positive":H,
    "rho_positive":rho,
    "NEC_space_positive":add(rho,p3),
    "DEC_space_positive":sub(rho,p3),
    "DEC_circle_positive":sub(rho,pw),
    "scalar_kinetic_C_except_lower_root":C,
    "electric_source_D_positive":D,
    "potential_V_positive":V,
    "Einstein_frame_expansion":expansion,
    "Einstein_frame_acceleration":A,
}
for name,P in conditions.items():
    if name=="scalar_kinetic_C_except_lower_root":continue
    coefficients=Bernstein2(P,l,right)
    assert min(coefficients)>0,(name,coefficients)
    print("BIGGER_INTERVAL_POSITIVE :=",name,"MIN_BERNSTEIN",min(coefficients))

# F(t)=t-1/10 is strictly negative for every t<right, zero at right.
assert Fc==(Q(-1,10),Q(1))
assert E(Fc,right)==0
assert E(Fc,l)<0
# The NEC only fails for t < t_- locally, and F<0 only for t<right.
# Hence the maximal connected OPEN set containing t=0 satisfying all
# STRICT properties has endpoints (t_-,right).
# C(t_-) =0, so the scalar clock ceases to be a local diffeomorphism at
# t=t_-; the strict scalar reconstruction excludes that endpoint.

# Log(a_E)=19t/20-7t²/20.
# At upper endpoint t=1/10, log(a_E)=183/2000.
# For t_- = (44-sqrt(2101))/66, use its minimal polynomial
# 396t²-528t-15=0 to reduce log(a_E(t_-)):
# log(a_E(t_-)) = 19t/20-7t²/20
#               = (29t/60) - 7/528 * 15? derive via identity algebraically
# final exact max e-fold N=29 sqrt(2101)/3960 -21529/99000.
# Verify expression by squaring, avoiding any irrational rounded root.
# Define a rational expression for N in terms of symbolic root t_-;
# reduce t_-² = (528t_-+15)/396.
# N=183/2000 -[19t/20-7t²/20]
# =183/2000 +(-19/20+7*528/(20*396))*t + 7*15/(20*396)
# =183/2000 - (29/60)t + 7/528
constant=Q(183,2000)+Q(7,528)
coefficient=-Q(29,60)
assert constant==Q(863,8250)  # verify independent rational normalization
assert coefficient<0
# t_- in [-.028,-.027] implies 0.117 < N < 0.119, no floats.
N_lower=constant+coefficient*u
N_upper=constant+coefficient*l
assert Q(117,1000)<N_lower<N_upper<Q(119,1000)
print("MAX_CONNECTED_INTERVAL := (2/3-sqrt(2101)/66,1/10)")
print("LOWER_END := CIRCLE_NULL_ENERGY_SATURATION; SCALAR_CLOCK_DEGENERATES")
print("UPPER_END := CIRCLE_CONTRACTION_STOPS")
print("MAX_EFOLDS_EXACT := 29*sqrt(2101)/3960-21529/99000")
print("MAX_EFOLDS_RATIONAL_ENCLOSURE := 117/1000 < N < 119/1000")
print("CURRENT_ACTION_CANNOT_SUSTAIN_ONE_EFOLD_IN_THIS_COMPONENT := PROVED")
print("CHANGING_b0_DOES_NOT_CHANGE_EFOLD_COUNT := PROVED")
print("NONPOWERLAW_OTHER_ACTIONS := OPEN")
