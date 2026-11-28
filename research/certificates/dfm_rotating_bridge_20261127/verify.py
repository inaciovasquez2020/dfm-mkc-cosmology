#!/usr/bin/env python3
"""Pure quadratic scalar, source-level constraint closure; a_i=H_i=rho_i=1."""
import json, math, time, sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp
T=1.5; DELTA=1e-5; G4=1.5; TS=np.linspace(0,T,401)
START=time.monotonic(); CALLS=0

def run(rhs,y,method,tol,step):
    global CALLS
    CALLS+=1
    if CALLS>100 or time.monotonic()-START>65: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
    s=solve_ivp(rhs,(0,T),y,t_eval=TS,rtol=tol,atol=tol*.001,method=method,max_step=step)
    if not s.success or s.nfev>200000: raise RuntimeError('INCOMPLETE_SOLVER')
    return s

def coeff(a,x,v,y,w,m,kappa):
    rho=(abs(x)**2+abs(v)**2)/2; H=math.sqrt(rho)
    p2=m*kappa/a**2; q=np.real(np.conj(v)*y)/m
    dr0=np.real(np.conj(v)*w+np.conj(x)*y)
    den=p2-G4*abs(v)**2
    if den<=0: raise RuntimeError('INCOMPLETE_CONSTRAINT_DENOMINATOR')
    Phi=-G4*(dr0+3*H*q)/den
    dPhi=G4*q-H*Phi
    return rho,H,p2,Phi,dPhi,(dr0-abs(v)**2*Phi)/rho,den/p2

def full(m,kappa,method,tol):
    A=DELTA*(.5-1j/kappa); y=A; w=(1j-1.5/m)*A
    def rhs(t,s):
        a=s[0].real;x,v,y,w=s[1:];rho,H,p2,Phi,dPhi,_,_=coeff(a,x,v,y,w,m,kappa)
        return np.array([a*H,m*v,-3*H*v-m*x,m*w,-3*H*w-(m+p2/m)*y+4*v*dPhi-2*m*x*Phi],complex)
    s=run(rhs,np.array([1,1,1j,y,w],complex),method,tol,.3/m)
    a=s.y[0].real;x,v,y,w=s.y[1:]; obs=np.array([coeff(*args,m,kappa) for args in zip(a,x,v,y,w)])
    assert np.max(abs(a**3*np.imag(np.conj(x)*v)-1))<2e-7
    X=a**1.5*x; Z=a**1.5*(v+1.5*obs[:,1]*x/m)
    U=(X-1j*Z)*np.exp(-1j*m*TS)/2; V=(X+1j*Z)*np.exp(1j*m*TS)/2
    Y=a**1.5*y; W=a**1.5*(w+1.5*obs[:,1]*y/m)
    A=(Y-1j*W)*np.exp(-1j*m*TS)/2; B=(Y+1j*W)*np.exp(1j*m*TS)/2
    return a,obs,A,B,U,V,s.nfev

def averaged(kappa):
    def rhs(t,z):
        a=(1+1.5*t)**(2/3); H=1/(1+1.5*t)
        return [z[1],-2*H*z[1]-(kappa**2/(4*a**4)-1.5/a**3)*z[0]]
    return run(rhs,[DELTA,DELTA],'DOP853',1e-12,.02).y[0]/DELTA

def main():
    cases=[]; maxdiff=0.; total=0
    for kappa in [1.,2.,4.,8.]:
        target=averaged(kappa)
        for m in [32,64,128,256]:
            a,obs,A,B,U,V,n=full(m,kappa,'DOP853',2e-10); total+=n
            delta=obs[:,5]/DELTA
            aa,oo,AA,BB,UU,VV,n2=full(m,kappa,'RK45',2e-11); total+=n2
            diff=float(np.max(abs(delta-oo[:,5]/DELTA)));maxdiff=max(maxdiff,diff)
            assert diff<2e-6
            err=float(np.max(abs(delta-target)))
            cases.append(dict(kappa=kappa,m=m,max_density_error=err,m_times_error=m*err,max_background_relative_error=float(max(abs(a/(1+1.5*TS)**(2/3)-1))),max_counterrotating_background=float(max(abs(V))),max_counterrotating_perturbation=float(max(abs(B))/DELTA),min_relative_constraint_denominator=float(min(obs[:,6])),max_solver_difference=diff,final_exact=float(delta[-1]),final_averaged=float(target[-1])))
    for kappa in [1.,2.,4.,8.]:
        rows=[r for r in cases if r['kappa']==kappa]
        assert rows[-1]['max_density_error']<rows[0]['max_density_error']
    print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,time_interval=[0,T],initial_density_contrast=DELTA,time_samples=len(TS),cases=cases,integrations=CALLS,full_rhs_evaluations=total,max_independent_solver_difference=maxdiff,scope='pure quadratic scalar, source-level constraint closure; Jeans scaling k^2=m*kappa; not visible species or observational likelihood'),indent=2))
if __name__=='__main__':main()
