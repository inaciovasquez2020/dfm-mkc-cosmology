#!/usr/bin/env python3
"""Exact temporal Maxwell Schur complement on the 5D EMD power-law background.
Scope: only the quadratic terms depending on u=delta A_t; the complete
Einstein/dilaton/Maxwell quadratic Hessian is NOT constructed here.
Requires SymPy; no repo writes or downloads.
"""
import sympy as S

t,b0,k,n=S.symbols('t b0 k n', positive=True, real=True)
a=t**S.Rational(3,2)
b=b0*t**S.Rational(3,4)
f=t**-7
Fty=S.sqrt(51)*b0*t**S.Rational(13,4)/4
Q=S.factor(a**3*f*Fty/b)
Cx=S.factor(a*b*f)
Cy=S.factor(a**3*f/b)
A=S.factor(k*k*Cx)
B=S.factor(n*n*Cy)
D=S.factor(A+B)
assert Q==S.sqrt(51)/4
assert S.simplify(Cx-b0*t**S.Rational(-19,4))==0
assert S.simplify(Cy-t**S.Rational(-13,4)/b0)==0

# Real Fourier quadratures: J is a real independent source representing
# +/- i*n*Q*(3*zeta-beta-alpha) in the complex Fourier notation.
u,v,J=S.symbols('u v J',real=True)
L=S.expand(S.Rational(1,2)*A*(v-u)**2+S.Rational(1,2)*B*u**2+J*u)
ustar=S.solve(S.diff(L,u),u)[0]
assert S.simplify(ustar-(A*v-J)/D)==0
Lred=S.factor(L.subs(u,ustar))
Lexpected=S.Rational(1,2)*A*B/D*v*v+A*J/D*v-J*J/(2*D)
assert S.simplify(Lred-Lexpected)==0
assert S.simplify(S.diff(Lred,v,2)-A*B/D)==0
assert S.simplify(S.diff(L,u,2)-D)==0
# Gaussian Hessian Schur complement is positive for k,n != 0.
Hv=S.hessian(L,(v,u))
assert S.simplify(Hv[0,0]-A)==0
assert S.simplify(Hv[1,1]-D)==0
assert S.simplify(Hv.det()-A*B)==0
assert S.simplify(A*B/D-(b0*k*k*n*n*t**S.Rational(-13,4))/(b0*b0*k*k+n*n*t**S.Rational(3,2)))==0
# k=0 and n=0 are not part of the same dynamical-gauge chart.
assert S.simplify((A*B/D).subs(k,0))==0
assert S.simplify((A*B/D).subs(n,0))==0
print('BACKGROUND_FLUX := PASS')
print('GAUSS_HESSIAN_D_POSITIVE := PASS (for t,b0,k,n>0)')
print('TEMPORAL_MAXWELL_ELIMINATION := PASS')
print('SCHUR_COMPLEMENT_KVV_POSITIVE := PASS (for k,n>0)')
print('FULL_GRAVITATIONAL_CONSTRAINT_BLOCK := OPEN')
print('PHYSICAL_SCALAR_KINETIC_MATRIX := OPEN')
print('FULL_5D_SCALAR_STABILITY := OPEN')
