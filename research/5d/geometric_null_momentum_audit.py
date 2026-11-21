#!/usr/bin/env python3
"""Exact geometric null projection of 5D ADM scalar momentum constraints.
This tests the GEOMETRIC LINEARIZED constraint only. Matter momentum source,
lapse elimination, and physical scalar kinetic matrix remain OPEN.
"""
import sympy as s
kap,nu,H,F,z,beta,zd,bd,alpha,u,v=s.symbols(
    'kap nu H F z beta zd bd alpha u v', real=True)
dK=s.Matrix([
    [zd-H*alpha-kap*u,0,0,-(nu*u+kap*v)/2],
    [0,zd-H*alpha,0,0],
    [0,0,zd-H*alpha,0],
    [-(nu*u+kap*v)/2,0,0,bd-F*alpha-nu*v]])
dE=s.simplify(dK-s.eye(4)*s.trace(dK))
Cx=s.expand(kap*dE[0,0]+nu*dE[3,0]+kap*(H-F)*beta)
Cy=s.expand(kap*dE[0,3]+nu*dE[3,3]+3*nu*(F-H)*z)
null=s.expand(kap*Cx+nu*Cy)
expected=s.expand(-kap**2*(2*zd+bd)-3*nu**2*zd
    +(kap**2*(2*H+F)+3*nu**2*H)*alpha
    +kap**2*(H-F)*beta+3*nu**2*(F-H)*z)
assert s.simplify(null-expected)==0
assert s.diff(null,u)==0 and s.diff(null,v)==0
Fkin=s.expand(s.trace(dK*dK)-s.trace(dK)**2)
Hs=s.simplify(s.hessian(Fkin,(u,v)))
assert Hs==s.Matrix([[nu**2,-kap*nu],[-kap*nu,kap**2]])
assert Hs.det()==0 and Hs*s.Matrix([kap,nu])==s.zeros(2,1)
assert s.factor((s.Matrix([[nu,-kap]])*Hs*s.Matrix([nu,-kap]))[0]) == (kap**2+nu**2)**2
print('GEOMETRIC_NULL_MOMENTUM_CONSTRAINT := PASS')
print('NULL_SHIFT_CANCELLATION := PASS')
print('SHIFT_HESSIAN_RANK := 1')
print('MATTER_MOMENTUM_SOURCE := OPEN')
print('LAPSE_SHIFT_ELIMINATION := OPEN')
print('FULL_PHYSICAL_SCALAR_KINETIC := OPEN')
print('GLOBAL_5D_STABILITY := OPEN')
