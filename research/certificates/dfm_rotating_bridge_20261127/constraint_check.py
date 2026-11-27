#!/usr/bin/env python3
"""Exact symbolic propagation identity for the pure scalar Einstein constraints."""
import sympy as s
import json
p2,H,g,A,Q,R,X,C,Phi=s.symbols('p2 H g A Q R X C Phi',real=True)
D=g*Q-H*Phi
Hd=-g*A
rho=R+X-A*Phi
pressure=R-X-A*Phi
Ad=-6*H*A-2*C
RplusXd=-6*H*R-p2*Q+4*A*D-2*C*Phi
qd=-3*H*Q+R-X
# derivative of p2 Phi + g (rho+3H Q), setting Phi_dot=D
constraint=p2*Phi+g*(rho+3*H*Q)
derivative=p2*(D-2*H*Phi)+g*(RplusXd-Ad*Phi-A*D+3*Hd*Q+3*H*qd)
assert s.expand(derivative+3*H*constraint)==0
# D_dot follows from differentiating D = g Q - H Phi
Dd=g*qd-Hd*Phi-H*D
assert s.expand(Dd+4*H*D+(2*Hd+3*H**2)*Phi-g*pressure)==0
print(json.dumps({'status':'EXACT_SYMBOLIC_PASS','sympy':s.__version__,'constraint_derivative_plus_3H_constraint':0,'spatial_trace_residual':0},indent=2))
