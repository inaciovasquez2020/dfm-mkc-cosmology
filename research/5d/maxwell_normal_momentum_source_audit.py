#!/usr/bin/env python3
"""Maxwell normal momentum source and null-constraint lapse coefficient.
A direct stress-tensor check, NOT a full ADM scalar Hessian.
Requires SymPy; no external downloads or repository mutations.
"""
import sympy as s

t,b0,k,n=s.symbols("t b0 k n", positive=True, real=True)
a=t**s.Rational(3,2)
b=b0*t**s.Rational(3,4)
f=t**-7
E=s.sqrt(51)*b0*t**s.Rational(13,4)/4
Q=s.factor(a**3*f*E/b)
assert Q==s.sqrt(51)/4
v=s.symbols("v", real=True)
# delta A_x = i k v exp(i(kx+ny)), delta A_y=0
Fxy=k*n*v
# Normal stress: T_(normal,x)=f F_(normal,y) F_x^y.
Tnx=s.factor(f*E*Fxy/b**2)
assert s.simplify(Tnx-Q*k*n*v/(a**3*b))==0
kap=k/a
nu=n/b
Tnhatx=s.factor(Tnx/a)
assert s.simplify(Tnhatx-Q*kap*nu*v/a**3)==0
assert s.simplify(kap*Tnhatx-Q*kap**2*nu*v/a**3)==0
H=s.Rational(3,2)/t
F=s.Rational(3,4)/t
Calpha=s.factor(kap**2*(2*H+F)+3*nu**2*H)
assert s.simplify(Calpha-(s.Rational(15,4)*kap**2+s.Rational(9,2)*nu**2)/t)==0
zd,bd,z,beta,source,alpha=s.symbols("zd bd z beta source alpha")
Cgeom=(-kap**2*(2*zd+bd)-3*nu**2*zd
       +Calpha*alpha+kap**2*(H-F)*beta+3*nu**2*(F-H)*z)
alpha_sol=s.solve(Cgeom-source,alpha)[0]
assert s.simplify((Cgeom-source).subs(alpha,alpha_sol))==0
assert s.simplify(s.diff(Cgeom,alpha)-Calpha)==0
print("MAXWELL_NORMAL_MOMENTUM_SOURCE := PASS")
print("ORTHONORMAL_PROJECTION := PASS")
print("NULL_CONSTRAINT_LAPSE_COEFFICIENT := POSITIVE")
print("FORMAL_LAPSE_SOLVABILITY := PASS")
print("FOURIER_PHASE_MATCHING := OPEN")
print("FULL_ADM_SCALAR_HESSIAN := OPEN")
print("PHYSICAL_SCALAR_SPECTRUM := OPEN")
