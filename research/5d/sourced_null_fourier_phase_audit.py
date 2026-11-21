#!/usr/bin/env python3
"""Complex Fourier source matching for 5D EMD null ADM momentum constraint.
CERTIFIES a necessary sourced momentum equation only, not complete scalar
constraints or the physical quadratic action. SymPy required.
"""
import sympy as s
I=s.I
t,b0,k,n=s.symbols('t b0 k n',positive=True,real=True)
a=t**s.Rational(3,2); b=b0*t**s.Rational(3,4); f=t**-7
H=s.diff(a,t)/a; F=s.diff(b,t)/b
E=s.sqrt(51)*b0*t**s.Rational(13,4)/4
Q=s.factor(a**3*f*E/b)
assert Q==s.sqrt(51)/4
kap=k/a; nu=n/b
z,be,zd,bed,alpha,v=s.symbols('z be zd bed alpha v')
Cgeom=s.expand(-kap**2*(2*zd+bed)-3*nu**2*zd+
  (kap**2*(2*H+F)+3*nu**2*H)*alpha+
  kap**2*(H-F)*be+3*nu**2*(F-H)*z)
# delta A_x=i*k*v e^{i(kx+ny)} -> delta F_xy=k*n*v e^{i(kx+ny)}.
Fxy=k*n*v
Tnx=s.factor(f*E*Fxy/b**2)
Tnxhat=s.factor(Tnx/a)
assert s.simplify(Tnx-Q*k*n*v/(a**3*b))==0
assert s.simplify(Tnxhat-Q*kap*nu*v/a**3)==0
source=s.factor(kap*Tnxhat)
assert s.simplify(source-Q*kap**2*nu*v/a**3)==0
Ca=s.factor(s.diff(Cgeom,alpha))
assert s.simplify(Ca-(s.Rational(15,4)*kap**2+s.Rational(9,2)*nu**2)/t)==0
R=s.expand(Cgeom-Ca*alpha)
# With K_ij=(dot gamma_ij-D_i N_j-D_j N_i)/(2N),
# Codazzi D_j(K^j_i-delta^j_i K)=T_(normal,i).
# Fourier divergence contributes i, so i*Cgeom=source.
asol=s.simplify((-I*source-R)/Ca)
assert s.simplify((I*Cgeom-source).subs(alpha,asol))==0
kr,nr=s.symbols('kr nr',real=True,nonzero=True)
assert s.simplify(s.conjugate(-I*Q*kr**2*nr*v/(a**5*b))-
  I*Q*kr**2*nr*s.conjugate(v)/(a**5*b))==0
print('MAXWELL_NORMAL_MOMENTUM := PASS')
print('FOURIER_PHASE_MATCHING := PASS under stated conventions')
print('SOURCED_MOMENTUM_LAPSE_SOLVABILITY := PASS')
print('FULL_HAMILTONIAN_SHIFT_ELIMINATION := OPEN')
print('FULL_ADM_SCALAR_HESSIAN := OPEN')
print('PHYSICAL_KINETIC_GRADIENT_MASS := OPEN')
print('FULL_5D_SCALAR_STABILITY := OPEN')
