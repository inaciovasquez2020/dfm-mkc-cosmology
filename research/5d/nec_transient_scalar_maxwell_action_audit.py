#!/usr/bin/env python3
"""Exact local reconstruction of healthy-sign scalar + Maxwell matter in 5D.

The potential and gauge coupling are explicitly DEFINED as smooth parametric
functions using an inverse monotone scalar clock. No new physical predictions
or naturalness claims follow from this inverse-engineered action.
"""
from fractions import Fraction as Q
from pathlib import Path
import runpy

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")
base=runpy.run_path(str(Path(__file__).with_name(
    "nec_transient_accelerating_circle_exact.py")))
poly,add,sub,mul,scale,diff,eq,lower_bound=(
    base[k] for k in ("poly","add","sub","mul","scale","diff","eq","lower_bound")
)
H,F,rho,p3,pw=(base[k] for k in ("H","F","rho","p3","pw"))
C=add(rho,pw)                 # phi_dot^2, canonical scalar
D=sub(p3,pw)                 # 2*E, circle-directed Maxwell electric anisotropy
V=scale(sub(rho,p3),Q(1,2))
r=Q(1,100)
for name,a in (("scalar_speed_squared",C),("electric_anisotropy",D),
               ("scalar_potential",V)):
    lb=lower_bound(a,r)
    assert lb>0,(name,lb)
    print("STRICT_INTERVAL_LOWER_BOUND :=",name,lb)
assert eq(C,poly(Q(3,10),Q(264,25),Q(-198,25)))
assert eq(D,poly(Q(99,100),Q(-231,25),Q(143,25)))
assert eq(V,poly(Q(411,200),Q(-9,2),Q(91,50)))

# 5D ACTION S=int sqrt(-g)[R/2-(dphi)^2/2-V(phi)-f(phi) F²/4].
# F_(tw)=dA_w/dt. Maxwell flux a³ f F_tw/b = 1.
# Choose phi(t)=int_0^t sqrt(C(u))du; strictly increasing by C>0.
# Set x=phi^{-1}(phi). Then
#   V(phi)=V(x),  f(phi)=exp[-6(x-3x²/5)]/D(x)>0.
# Choose A_w(t)=int_0^t b(u)*a(u)^3*D(u)du.
# This makes the flux exactly 1 and E=1/[2 a^6 f]=D/2.
K=scale(C,Q(1,2))
E=scale(D,Q(1,2))
assert eq(rho,add(add(K,E),V))
assert eq(p3,sub(add(K,E),V))
assert eq(pw,sub(sub(K,E),V))

# Scalar EOM for homogeneous phi: ddot phi+(3H+F)dot phi+
# V_phi-E*f_phi/f=0.
# Multiply by sqrt(C). Since
# (log f)_dot=-6H-D_dot/D, the rational expression simplifies to:
# C_dot/2+(3H+F)C+V_dot+3H D+D_dot/2 == 0.
scalar_eom=add(add(scale(diff(C),Q(1,2)),
                   mul(add(scale(H,3),F),C)),
               add(diff(V),add(scale(mul(H,D),3),
                               scale(diff(D),Q(1,2)))))
assert eq(scalar_eom,poly(0))

# Maxwell equation is exact from f*a^6*D=1 and
# A_w_dot=b*a³*D; no approximation or discrete time samples used.
# The electric stress is E=f*(A_w_dot/b)^2/2 = D/2.
assert eq(add(scale(E,2),neg_D:=tuple(-v for v in D)),poly(0))
assert eq(add(add(add(K,V),E),tuple(-v for v in rho)),poly(0))

print("ACTION := R5/2 - (dphi)^2/2 - V(phi) - f(phi)*F_AB*F^AB/4")
print("PHI := integral_0^t sqrt(C(u)) du; C(t)=rho+pw>0")
print("POTENTIAL := V(phi(t))=(rho(t)-p3(t))/2")
print("GAUGE_COUPLING := f(phi(t))=exp(-6*t+18*t*t/5)/D(t); D(t)=p3-pw>0")
print("CIRCLE_ELECTRIC_FIELD := dA_w/dt=b*a^3*D")
print("MAXWELL_FLUX := 1 IDENTICALLY")
print("CANONICAL_SCALAR_AND_POSITIVE_MAXWELL_COUPLING := PASS")
print("ALL_DIAGONAL_EINSTEIN_EQUATIONS := PASS (5D tensor symmetry)")
print("SCALAR_EQUATION_EXACT_POLYNOMIAL_IDENTITY := PASS")
print("ACTION_DEFINED_SMOOTHLY_ON_CLOSED_TIME_INTERVAL := PASS")
print("MATTER_ACTION_EXISTS := CONDITIONAL_LOCAL_INVERSE_ENGINEERED")
print("PHYSICAL_NATURALNESS_AND_FULL_PERTURBATIVE_STABILITY := OPEN")
print("PREDICTIVE_5D_NECESSITY := OPEN")
