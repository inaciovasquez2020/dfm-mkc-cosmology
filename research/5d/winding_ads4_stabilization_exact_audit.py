#!/usr/bin/env python3
"""5D Einstein + compact winding scalar: stabilized AdS4 x S1 exact benchmark.

A reproducible classical construction, not a novelty or physical-5D claim.
SymPy required; assertions enabled; no repository state mutations.
"""
import sympy as s

if not __debug__:
    raise SystemExit("INCOMPLETE: Python -O disables assertion checks")

L,b,q,k=s.symbols("Lambda5 b q k", real=True)
V=L/b+q*q/(4*b**3)
# For action S5=integral sqrt(-g5)[R5/2-Lambda5-(dchi)^2/4],
# Einstein-form equation: Ric_AB = (2 Lambda5/3)g_AB + (dchi)_A(dchi)_B/2.
# ds5^2=ds4^2+b^2 dw^2, Ric4=3k g4 and chi=q w (mod 2*pi*f).
assert s.simplify((3*k-s.Rational(2,3)*L).subs(k,2*L/9))==0
assert s.simplify((s.Rational(2,3)*L*b*b+q*q/2).subs(q*q,-4*L*b*b/3))==0
assert s.simplify(s.diff(V,b)+(4*L*b*b+3*q*q)/(4*b**4))==0
q2=-4*L*b*b/3
assert s.simplify(V.subs(q*q,q2)-2*L/(3*b))==0
assert s.simplify(s.diff(V,b,2).subs(q*q,q2)+2*L/b**3)==0
m2=s.simplify((s.Rational(2,3)*b*b*s.diff(V,b,2)).subs(q*q,q2))
assert s.simplify(m2+4*L/(3*b))==0
# Einstein-frame AdS radius squared: L_E^2=b * [-9/(2 Lambda5)].
assert s.simplify(m2*(-9*b/(2*L)))==6
# For b>0, q!=0, Lambda5>=0, V'(b)<0: no stationary radius.
assert s.simplify(s.diff(V,b).subs({L:0,q:1})+s.Rational(3,4)/b**4)==0

params={L:-s.Rational(3,2),q:1,b:s.sqrt(2)/2,k:-s.Rational(1,3)}
assert s.simplify((s.Rational(2,3)*L*b*b+q*q/2).subs(params))==0
assert s.simplify(s.diff(V,b).subs(params))==0
assert s.simplify(m2.subs(params))>0

# Independent direct five-dimensional tensor check using a Poincare AdS4 patch.
z,t,x,y,w=s.symbols("z t x y w", real=True, positive=True)
coords=(t,x,y,z,w)
g=s.diag(-3/z**2,3/z**2,3/z**2,3/z**2,s.Rational(1,2))
inv=g.inv()
N=5
Gamma=[[[s.simplify(sum(inv[a,d]*(
    s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])
    -s.diff(g[b,c],coords[d]))/2 for d in range(N)))
    for c in range(N)] for b in range(N)] for a in range(N)]
Ric=s.zeros(N)
for i in range(N):
    for j in range(N):
        Ric[i,j]=s.simplify(sum(
            s.diff(Gamma[p][i][j],coords[p])-s.diff(Gamma[p][i][p],coords[j])
            +sum(Gamma[p][i][j]*Gamma[d][p][d]
                 -Gamma[d][i][p]*Gamma[p][j][d] for d in range(N))
            for p in range(N)))
expected=-g+s.diag(0,0,0,0,s.Rational(1,2))
assert Ric==expected,(Ric,expected)
# Box chi=0 for chi=w: sqrt(-g5), g^(w,w) are w-independent.
assert s.diff(s.simplify(g.det()),w)==0
assert s.diff(inv[4,4],w)==0

print("DIRECT_5D_RICCI_25_COMPONENTS := PASS")
print("5D_EINSTEIN_AXION_EQUATIONS := PASS")
print("AXION_EQUATION := PASS")
print("4D_EINSTEIN_FRAME_STATIONARITY := PASS")
print("RADION_MASS_SQUARED_POSITIVE_FOR_NEGATIVE_LAMBDA5 := PASS")
print("RADION_MASS_SQUARED_TIMES_ADS_RADIUS_SQUARED := 6")
print("NO_FIXED_RADIUS_FOR_LAMBDA5_NONNEGATIVE_AND_NONZERO_WINDING := PROVED")
print("STABLE_DE_SITTER := NOT_ESTABLISHED")
print("FULL_5D_PERTURBATION_STABILITY := NOT_ESTABLISHED")
print("PHYSICAL_5D_NECESSITY := OPEN")
