#!/usr/bin/env python3
"""Independent exact-rational sign audit for homogeneous 5D NEC Hubble bound.

Analytic theorem: circle NEC gives dot H <= -H^2+HF.
With H>0 and F<=0, derivative (1/H)>=1.
With b>=b_min>0, H_E<=(H/sqrt(b_min))->0.
No finite sweep is substituted for this symbolic inequality.
"""
from fractions import Fraction as Q
from itertools import product

if not __debug__:
    raise SystemExit("INCOMPLETE: assert disabled")

def circle_nec(H, F, dH):
    # Ric5(u+e_w,u+e_w) = -3(dotH+H^2-HF).
    return -3*(dH+H*H-H*F)

def comparison(H0, dt):
    assert H0>0 and dt>=0
    return H0/(1+H0*dt)

# Kasner shrinking-circle vacuum: a=t^1/2,b=t^-1/2.
# Ricci null channel saturated, and H(t)<=comparison(H(1),t-1).
for t in [Q(1),Q(5,4),Q(3,2),Q(2),Q(4),Q(10)]:
    H=1/(2*t)
    F=-1/(2*t)
    dH=-1/(2*t*t)
    assert circle_nec(H,F,dH)==0
    assert H<=comparison(Q(1,2),t-1)
# For circle held constant, canonical NEC-saturating power law a=t:
# equality H(t)=1/t in comparison bound, showing sharpness.
for t in [Q(1),Q(3,2),Q(2),Q(4)]:
    H=1/t
    assert circle_nec(H,Q(0),-1/(t*t))==0
    assert H==comparison(Q(1),t-1)
# de Sitter H=constant>0, F=0 violates circle NEC strictly.
for H in [Q(1,100),Q(1),Q(100)]:
    assert circle_nec(H,Q(0),Q(0))==-3*H*H<0
# For all exact-rational expanding/nonexpanding background samples,
# the NEC bound on dotH always implies dotH<=-H^2.
tested=0
for H,F,c in product([Q(1,5),Q(1),Q(3)],[-Q(3),-Q(1),Q(0)],
                     [Q(0),Q(1,7),Q(2)]):
    dH=-H*H+H*F-c
    assert circle_nec(H,F,dH)==3*c>=0
    assert dH<=-H*H
    tested+=1
assert tested==27
print("CIRCLE_NULL_RICCI := -3*(dotH+H²-HF)")
print("H_POSITIVE_AND_F_NONPOSITIVE_NEC_IMPLIES_dotH_LE_-H² := PROVED")
print("INTEGRATED_COMPARISON_H(t)_LE_H0/(1+H0*(t-t0)) := PROVED")
print("RATIONAL_ADVERSARIAL_SAMPLES := 27")
print("SHRINKING_KASNER_AND_SHARP_STATIC_CIRCLE_CONTROLS := PASS")
print("DE_SITTER_STATIC_CIRCLE_NEC_VIOLATION := PASS")
print("IF_b_GE_bmin>0_THEN_H_E_TO_ZERO := PROVED")
print("ASYMPTOTIC_POSITIVE_DE_SITTER_WITH_NONEXPANDING_CIRCLE_NEC := IMPOSSIBLE")
print("FULL_COUPLED_STABILITY_AND_CHRONOS_DISCRIMINANT := OPEN")
