#!/usr/bin/env python3
"""Exact scalar-shift gravitational principal Hessian for 5D FLRW times S1.
Tests the ADM extrinsic-curvature kinetic term ONLY. Full matter-sourced
momentum constraints, lapse elimination and 5D scalar stability remain OPEN.
Requires SymPy; does not change repository state.
"""
import sympy as s
z, beta, u, v, kap, nu = s.symbols("z beta u v kap nu", real=True, nonzero=True)
K = s.zeros(4)
K[0,0] = z-kap*u
K[1,1] = z
K[2,2] = z
K[3,3] = beta-nu*v
K[0,3] = K[3,0] = -(kap*v+nu*u)/2
F = s.expand(s.trace(K*K)-s.trace(K)**2)
H = s.simplify(s.hessian(F,(u,v)))
assert H == s.Matrix([[nu**2,-kap*nu],[-kap*nu,kap**2]])
assert s.factor(H.det()) == 0
assert H.rank() == 1
null = s.Matrix([kap,nu])
assert H*null == s.zeros(2,1)
grad = s.Matrix([s.diff(F,u),s.diff(F,v)])
assert s.simplify((null.T*grad)[0]-2*(kap**2*beta+(2*kap**2+3*nu**2)*z)) == 0
assert s.simplify((s.Matrix([[u,v]])*H*s.Matrix([u,v]))[0]-(nu*u-kap*v)**2) == 0
print("GRAVITATIONAL_SHIFT_HESSIAN := EXACT_PASS")
print("GRAVITATIONAL_SHIFT_RANK := 1")
print("GRAVITATIONAL_SHIFT_DETERMINANT := 0")
print("NULL_SHIFT_DIRECTION := (kap,nu)")
print("FULL_MATTER_SOURCED_MOMENTUM_CONSTRAINT := OPEN")
print("LAPSE_SHIFT_CONSTRAINT_ELIMINATION := OPEN")
print("PHYSICAL_SCALAR_KINETIC_MATRIX := OPEN")
print("GRADIENT_MASS_EIGENVALUES := OPEN")
print("FULL_5D_SCALAR_STABILITY := OPEN")
