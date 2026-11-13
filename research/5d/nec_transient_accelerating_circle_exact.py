#!/usr/bin/env python3
"""Exact interval certificate for a transient NEC/DEC-compatible 5D circle reduction.

5D Einstein gravity, Lambda5=0, flat homogeneous 3-space, one compact circle.
Stress-energy is DEFINED as G_AB (kappa5^2=1), not derived from a matter action.
Standard-library rational polynomial arithmetic, no finite-grid substitutions.
"""
from fractions import Fraction as Q

if not __debug__:
    raise SystemExit("INCOMPLETE: Python optimization disabled assertions")

def poly(*xs):
    return tuple(Q(x) for x in xs)

def add(a,b):
    return tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b))))

def neg(a):
    return tuple(-x for x in a)

def sub(a,b):
    return add(a,neg(b))

def mul(a,b):
    z=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            z[i+j]+=x*y
    return tuple(z)

def scale(a,c):
    return tuple(x*Q(c) for x in a)

def diff(a):
    return tuple(i*a[i] for i in range(1,len(a))) or (Q(0),)

def eq(a,b):
    n=max(len(a),len(b))
    return all((a[i] if i<len(a) else 0)==(b[i] if i<len(b) else 0)
               for i in range(n))

def lower_bound(a,r):
    """Valid on [-r,r] by triangle inequality for nonconstant monomials."""
    return a[0]-sum(abs(a[i])*r**i for i in range(1,len(a)))

# a(t)=exp(t-3t^2/5), b(t)=exp(-t/10+t^2/2).
H=poly(1,Q(-6,5))
F=poly(Q(-1,10),1)
dH=diff(H)
dF=diff(F)
H2=mul(H,H)
F2=mul(F,F)
HF=mul(H,F)

# G^0_0=-rho; G^i_i=p3; G^w_w=pw with kappa5^2=1, Lambda5=0.
rho=scale(add(H2,HF),3)
p3=neg(add(add(scale(dH,2),dF),add(scale(H2,3),add(scale(HF,2),F2))))
pw=neg(add(scale(dH,3),scale(H2,6)))
null_circle=add(rho,pw)
null_space=add(rho,p3)
# Einstein-frame metric: g_E=b*g_4, d(tau)=sqrt(b)dt, a_E=a sqrt(b).
# (a_E)'' / a_E = A/b with A=dot(H)+dot(F)/2+H^2+HF/2.
A=add(add(dH,scale(dF,Q(1,2))),add(H2,scale(HF,Q(1,2))))

expected={
    "rho":poly(Q(27,10),Q(-96,25),Q(18,25)),
    "rho_plus_p3":poly(Q(129,100),Q(33,25),Q(-11,5)),
    "rho_plus_pw":poly(Q(3,10),Q(264,25),Q(-198,25)),
    "A":poly(Q(1,4),Q(-46,25),Q(21,25)),
}
assert eq(rho,expected["rho"])
assert eq(null_space,expected["rho_plus_p3"])
assert eq(null_circle,expected["rho_plus_pw"])
assert eq(A,expected["A"])

# Homogeneous 5D Bianchi identity: conservation is an exact polynomial identity.
assert eq(add(diff(rho),add(scale(mul(H,null_space),3),
                            mul(F,null_circle))),poly(0))

r=Q(1,100)
positive={
    "3-space expansion H":H,
    "circle contraction -F":neg(F),
    "energy density rho":rho,
    "NEC space rho+p3":null_space,
    "NEC circle rho+pw":null_circle,
    "DEC space rho-p3":sub(rho,p3),
    "DEC circle rho-pw":sub(rho,pw),
    "Einstein frame expansion H+F/2":add(H,scale(F,Q(1,2))),
    "Einstein frame acceleration numerator A":A,
}
for name,p in positive.items():
    bound=lower_bound(p,r)
    assert bound>0,(name,bound)
    print("POSITIVE_ON_INTERVAL :=",name,"LOWER_BOUND",bound)

# Non-power-law example and exact t=0 witness.
assert A[0]==Q(1,4)
assert null_circle[0]==Q(3,10)
assert null_space[0]==Q(129,100)
assert rho[0]==Q(27,10)
assert p3[0]==Q(-141,100)
assert pw[0]==Q(-12,5)

print("INTERVAL := [-1/100,1/100]")
print("EINSTEIN_FIELD_EQUATIONS := SATISFIED_BY_DEFINITION_T_EQ_G")
print("STRESS_CONSERVATION_BIANCHI := PASS")
print("FIVE_DIMENSIONAL_NEC_AND_DEC := CERTIFIED_ON_INTERVAL")
print("SHRINKING_CIRCLE_WITH_TRANSIENT_4D_EINSTEIN_ACCELERATION := PASS")
print("MICROPHYSICAL_MATTER_ACTION := NOT_CONSTRUCTED")
print("RADION_STABILIZATION := NOT_ESTABLISHED")
print("GLOBAL_OR_LATE_TIME_ACCELERATION := NOT_ESTABLISHED")
print("PHYSICAL_FIFTH_DIMENSION := OPEN")
