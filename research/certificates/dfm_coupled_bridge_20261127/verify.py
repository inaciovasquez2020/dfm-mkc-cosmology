#!/usr/bin/env python3
"""Scalar+dust+Lambda Jeans-scaled limit, independent Cartesian IVP."""
import json, time, math
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp
T=1.; ts=np.linspace(0,T,301); amp=1e-5; g=1.5
start=time.monotonic(); calls=0; full_nfev=0

def run(rhs,y,method,tol,step,full=False):
    global calls,full_nfev
    if calls>=120 or time.monotonic()-start>70: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
    calls+=1
    sol=solve_ivp(rhs,(0,T),y,method=method,rtol=tol,atol=tol*.001,t_eval=ts,max_step=step)
    if not sol.success or sol.nfev>200000: raise RuntimeError('INCOMPLETE_SOLVER')
    if full: full_nfev+=sol.nfev
    return sol.y

def symbolic():
    p,H,g,K,R,X,C,P,d,b,q,u=sp.symbols('p H g K R X C P d b q u')
    D=g*(q+u)-H*P; Hd=-g*(K+b)
    rho=R+X-K*P+b*d; pressure=R-X-K*P
    Kd=-6*H*K-2*C; RXd=-6*H*R-p*q+4*K*D-2*C*P
    qd=-3*H*q+R-X; ud=-3*H*u+b*P
    bd=-3*H*b; dd=-p*u/b+3*D
    constraint=p*P+g*(rho+3*H*(q+u))
    deriv=p*(D-2*H*P)+g*(RXd-Kd*P-K*D+bd*d+b*dd+3*Hd*(q+u)+3*H*(qd+ud))
    assert sp.expand(deriv+3*H*constraint)==0
    Dd=g*(qd+ud)-Hd*P-H*D
    assert sp.expand(Dd+4*H*D+(2*Hd+3*H**2)*P-g*pressure)==0
    Q,rs,rb=sp.symbols('Q rs rb')
    mat=sp.Matrix([[Q-g*rs,-g*rb],[-g*rs,-g*rb]])
    assert sp.expand(mat.det()+Q*g*rb)==0
    return {'constraint_propagation':0,'trace_residual':0,'jeans_determinant_residual':0}

def exact(m,k,s,b,l,method,tol):
    A=amp*(.5-1j/k); B=amp*(.15+.2j)
    db=.8*amp; ub=-.6*amp/k
    def coeff(z):
        a=z[0].real; x,v,y,w=z[1:5]; d,u=z[5:].real
        r=(abs(x)**2+abs(v)**2)/2; rb=b/a**3; H=math.sqrt(l+s*r+rb); p=m*k/a**2
        K=s*abs(v)**2; rs0=s*np.real(np.conj(v)*w+np.conj(x)*y); q=s*np.real(np.conj(v)*y)/m+rb*u/m
        den=p-g*K
        if den<=0: raise RuntimeError('INCOMPLETE_CONSTRAINT_DENOMINATOR')
        P=-g*(rs0+rb*d+3*H*q)/den; D=g*q-H*P
        return a,H,p,P,D,(rs0-K*P)/(s*r),den/p
    def rhs(t,z):
        a,H,p,P,D,_,_=coeff(z); x,v,y,w=z[1:5]; d,u=z[5:].real
        return np.array([a*H,m*v,-3*H*v-m*x,m*w,-3*H*w-(m+p/m)*y+4*v*D-2*m*x*P,-k*u/a**2+3*D,m*P],complex)
    y=A+B; w=1j*(A-B)-1.5*y/m
    sol=run(rhs,np.array([1,1,1j,y,w,db,ub],complex),method,tol,.4/m,True)
    vals=np.array([coeff(z) for z in sol.T]); a=vals[:,0]; x,v=sol[1:3]
    assert max(abs(a**3*np.imag(np.conj(x)*v)-1))<1e-7
    E=a**3*(abs(x)**2+abs(v)**2)/2
    assert min(E)>=1-1e-7 and max(E)<=(1+9/m**2)/(1-9/m**2)+1e-7
    return a,vals[:,5]/amp,sol[5].real/amp,float(min(vals[:,6])),float(max(E-1))

def averaged(k,s,b,l):
    def rhs(t,z):
        a,ds,vs,db,vb=z; H=math.sqrt(l+(s+b)/a**3); grav=g*(s*ds+b*db)/a**3
        return [a*H,vs,-2*H*vs-k*k*ds/(4*a**4)+grav,vb,-2*H*vb+grav]
    return run(rhs,[1,amp,amp,.8*amp,.6*amp],'DOP853',1e-12,.02)

def main():
    sym=symbolic(); rows=[]
    for s,b,l in [(.8,.2,0.),(.26,.05,.69),(.1,.4,.5)]:
        for k in [1.,4.,8.]:
            target=averaged(k,s,b,l)
            for m in [32,64,128,256]:
                a,ds,db,den,E=exact(m,k,s,b,l,'DOP853',2e-10)
                aa,dss,dbb,_,_=exact(m,k,s,b,l,'RK45',2e-11)
                diff=float(max(np.max(abs(ds-dss)),np.max(abs(db-dbb))))
                assert diff<3e-6
                err=float(max(np.max(abs(ds-target[1]/amp)),np.max(abs(db-target[3]/amp))))
                rows.append(dict(s=s,b=b,Lambda_fraction=l,kappa=k,m=m,max_density_error=err,m_times_error=m*err,max_solver_disagreement=diff,max_background_error=float(max(abs(a/target[0]-1))),min_relative_constraint_denominator=den,max_scalar_comoving_energy_excess=E))
            assert rows[-1]['max_density_error']<rows[-4]['max_density_error']
    print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,symbolic=sym,integrations=calls,full_rhs_evaluations=full_nfev,cases=rows,grid_samples=len(ts),max_independent_solver_difference=max(x['max_solver_disagreement'] for x in rows),scope='pure canonical scalar plus pressureless dust and nonnegative Lambda; fixed positive kappa; not radiation or observational transfer'),indent=2))
if __name__=='__main__':main()
