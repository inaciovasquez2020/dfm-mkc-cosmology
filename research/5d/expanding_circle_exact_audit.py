#!/usr/bin/env python3
"""Exact 5D expanding-circle vacuum Lambda solution.
Hypotheses: h,t,tau>0; y periodically identified; Lambda5=6 h^2.
SymPy required. No external data, downloads, or changes to repository state.
This is a bounded mathematical certificate, not evidence for physical 5D.
"""
import sympy as s
h,t,tau=s.symbols('h t tau', real=True, positive=True)
y,x1,x2,x3=s.symbols('y x1 x2 x3',real=True)
coords=[t,x1,x2,x3,y]
E=s.exp(2*h*t)
g=s.diag(-1,E,E,E,E)
inv=g.inv(); dim=5
Gamma=[[[s.simplify(s.Rational(1,2)*sum(
    inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))
    for d in range(dim))) for c in range(dim)] for b in range(dim)] for a in range(dim)]
Ric=s.zeros(dim)
for a in range(dim):
    for b in range(dim):
        Ric[a,b]=s.simplify(sum(
            s.diff(Gamma[c][a][b],coords[c])-s.diff(Gamma[c][a][c],coords[b])
            +sum(Gamma[c][a][b]*Gamma[d][c][d]-Gamma[d][a][c]*Gamma[c][b][d]
                 for d in range(dim)) for c in range(dim)))
assert (Ric-4*h*h*g)==s.zeros(dim)
assert s.simplify(sum(inv[a,a]*Ric[a,a] for a in range(dim))-20*h*h)==0
b=(h*tau/2)**2
aE=(h*tau/2)**3
HE=s.simplify(s.diff(aE,tau)/aE)
phi=s.sqrt(s.Rational(3,2))*s.log(b)
phidot=s.simplify(s.diff(phi,tau))
V=s.simplify(6*h*h/b)
coupling=s.sqrt(s.Rational(2,3))
assert s.simplify(3*HE**2-(phidot**2/2+V))==0
assert s.simplify(s.diff(HE,tau)+phidot**2/2)==0
assert s.simplify(s.diff(phi,tau,2)+3*HE*phidot-coupling*V)==0
assert s.simplify(s.diff(aE,tau,2))==s.Rational(3,4)*h**3*tau
m1=s.simplify(b**(-s.Rational(3,2)))
assert s.simplify(m1/HE-8/(3*h**3*tau**2))==0
print('FULL_5D_RICCI := PASS (25 components)')
print('EINSTEIN_LAMBDA5 := PASS')
print('4D_FRIEDMANN_RADION := PASS')
print('4D_EINSTEIN_ACCELERATION := PASS')
print('CIRCLE_STABILIZATION := FAIL (radius grows)')
print('PHYSICAL_5D_NECESSITY := OPEN')
