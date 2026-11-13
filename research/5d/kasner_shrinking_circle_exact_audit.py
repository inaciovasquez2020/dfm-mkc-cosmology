#!/usr/bin/env python3
"""Exact bounded 5D vacuum isotropic-three-space Kasner circle certificate."""
import sympy as s
if not __debug__:
    raise SystemExit('INCOMPLETE: -O disables assertions')
t=s.symbols('t', positive=True)
p,q=s.symbols('p q', real=True)
Rtt=-(3*p*(p-1)+q*(q-1))/t**2
Rxx=s.factor(p*(3*p+q-1)*t**(2*p-2))
Rww=s.factor(q*(3*p+q-1)*t**(2*q-2))
# For nonstatic p,q, the spatial vacuum equations require 3p+q=1.
assert s.factor((3*p*(p-1)+q*(q-1)).subs(q,1-3*p))==6*p*(2*p-1)
assert s.solve([3*p+q-1,3*p*p+q*q-1],[p,q])==[(0,1),(s.Rational(1,2),s.Rational(-1,2))]
# Independently contract the exact 5D Christoffel/Ricci tensor.
coords=(t,*s.symbols('x y z w', real=True)); n=5
g=s.diag(-1,t,t,t,1/t)
inv=g.inv()
G=[[[s.simplify(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(n))) for c in range(n)] for b in range(n)] for a in range(n)]
R=s.zeros(n)
for a in range(n):
  for b in range(n):
    R[a,b]=s.simplify(sum(s.diff(G[c][a][b],coords[c])-s.diff(G[c][a][c],coords[b])+sum(G[c][a][b]*G[d][c][d]-G[d][a][c]*G[c][b][d] for d in range(n)) for c in range(n)))
assert R==s.zeros(n)
# Four-dimensional Einstein-frame zero-mode reduction.
b=t**(-s.Rational(1,2)); aJ=s.sqrt(t); aE=s.simplify(s.sqrt(b)*aJ)
tau=s.Rational(4,3)*t**s.Rational(3,4)
H=s.simplify((s.diff(aE,t)/aE)/s.diff(tau,t))
phi=s.sqrt(s.Rational(3,2))*s.log(b)
phidot=s.simplify(s.diff(phi,t)/s.diff(tau,t))
Hdot=s.simplify(s.diff(H,t)/s.diff(tau,t))
assert s.simplify(aE-t**s.Rational(1,4))==0
assert s.simplify(H-1/(3*tau))==0
assert s.simplify(3*H*H-phidot*phidot/2)==0
assert s.simplify(Hdot+phidot*phidot/2)==0
assert s.simplify((s.diff(phidot,t)/s.diff(tau,t))+3*H*phidot)==0
assert s.simplify(s.diff(s.diff(aE,t)/s.diff(tau,t),t)/s.diff(tau,t))<0
# 5D Riemann-square of the diagonal power-law metric.
exponents=(s.Rational(1,2),)*3+(s.Rational(-1,2),)
K=s.factor(4*(sum((v*(v-1))**2 for v in exponents)+sum((exponents[i]*exponents[j])**2 for i in range(4) for j in range(i+1,4)))/t**4)
assert K==s.Rational(9,2)/t**4
mE=b**(-s.Rational(3,2))
assert s.simplify(mE/H-4*t**s.Rational(3,2))==0
# The other nonstatic branch has constant first-mode KK gap / H.
tau0=s.Rational(2,3)*t**s.Rational(3,2)
aE0=s.sqrt(t)
H0=s.simplify((s.diff(aE0,t)/aE0)/s.diff(tau0,t))
assert s.simplify(H0-1/(3*tau0))==0
assert s.simplify(t**(-s.Rational(3,2))/H0)==2
assert s.simplify(Rtt.subs({p:s.Rational(1,3),q:0}))!=0
print('KASNER_NONSTATIC_BRANCHES := (0,1);(1/2,-1/2)')
print('EXACT_5D_VACUUM_RICCI_25_COMPONENTS := PASS')
print('EINSTEIN_FRAME_MASSLESS_SCALAR_FRIEDMANN := PASS')
print('FOUR_DIMENSIONAL_SCALE_FACTOR_POWER := 1/3 (decelerating)')
print('KRETSCHMANN := 9/(2*t^4)')
print('SHRINKING_CIRCLE_KK_MASS_OVER_H := 4*t^(3/2)')
print('OTHER_BRANCH_KK_MASS_OVER_H := 2')
print('STATIC_MINKOWSKI_ZERO_EXPONENT_BRANCH := EXCLUDED_FROM_NONSTATIC_CLASSIFICATION')
print('STABILIZATION_AND_LATE_ACCELERATION := NOT_ESTABLISHED')
print('FOUR_DIMENSIONAL_OBSERVATIONAL_DISTINCTION := OPEN')
