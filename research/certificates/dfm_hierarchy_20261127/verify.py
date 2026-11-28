#!/usr/bin/env python3
"""Finite-section hierarchy audit, prescribed geometry, not a CMB solver."""
import json, math, time
import numpy as np
import scipy, sympy as sp
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn
start=time.monotonic(); calls=0; nfev=0; grid=np.linspace(0,1,101)
def bound(k,d):return math.exp(d*math.log(k)-math.lgamma(d+1))
def symbolic():
    L=-sp.eye(3)+sp.Matrix([sp.Rational(1,10),sp.Rational(1,2),sp.Rational(1,10)])*sp.ones(1,3); W=sp.diag(5,1,5)
    assert W*L==L.T*W and L.eigenvals()=={-sp.Rational(3,10):1,-1:2}
    Lr=-sp.eye(2)+sp.Matrix([sp.Rational(1,10),sp.Rational(1,10)])*sp.Matrix([[1,6]]); Wr=sp.diag(5,30)
    assert Wr*Lr==Lr.T*Wr and Lr.eigenvals()=={-sp.Rational(3,10):1,-1:1}
    R,b,v,G,H=sp.symbols('R b v G H',positive=True)
    Eprime=(H*R*b*b+2*R*b*(-H*b+G*(v-b)/R)+2*v*(-G*(v-b)))/3
    assert sp.expand(Eprime+H*R*b*b/3+2*G*(v-b)**2/3)==0
    return {'physical_collision_eigenvalues':['-1','-1','-3/10'],'repository_row_eigenvalues':['-1','-3/10'],'weighted_symmetry':True,'dipole_energy_identity':True}
def run(k,N,profile,method,model,forced=True):
    global calls,nfev
    if calls>=220 or time.monotonic()-start>70:raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
    calls+=1
    w=np.sqrt(2*np.arange(N+1)+1.); c=np.arange(1,N+1)/(w[:-1]*w[1:]); H=.2
    y=np.zeros((3,N+1)); y[0,0]=1.
    if forced:y[0,1]=.2;y[0,2]=-.1;y[1,2]=.15;y[2,1]=.1
    def rhs(t,flat):
        X=flat.reshape(3,N+1); a,p=X[:2]; b=X[2,1]; R=.6*math.exp(H*t)
        G=0. if profile=='free' else (20*(1-t)**2 if profile=='release' else 40*(.5+.5*math.cos(6*math.pi*t))**2)
        d=np.zeros_like(X);d[:2,1:]+=k*c*X[:2,:-1];d[:2,:-1]-=k*c*X[:2,1:]
        if model=='repository':d[1,:2]=0;d[1,2]=-k*c[2]*p[3] if N>=3 else 0.
        d[0,1:]-=G*a[1:];d[1]-=G*p
        d[0,1]+=G*b/math.sqrt(R);d[2,1]=-H*b/2+G*(a[1]/math.sqrt(R)-b/R)
        if model=='physical':
            S=a[2]/w[2]+p[0]+p[2]/w[2];d[0,2]+=G*w[2]*S/10;d[1,0]+=G*S/2;d[1,2]+=G*w[2]*S/10
        else:
            S=a[2]/w[2]+math.sqrt(6)*p[2]/w[2];d[0,2]+=G*w[2]*S/10;d[1,2]+=G*math.sqrt(6)*w[2]*S/10
        if forced:d[0,0]+=.05*math.cos(t);d[0,1]+=.03*math.sin(t);d[2,1]+=.02*math.cos(t)
        return d.ravel()
    sol=solve_ivp(rhs,(0,1),y.ravel(),method=method,rtol=2e-11,atol=2e-13,t_eval=grid,max_step=min(.035,.5/(k+1)))
    nfev+=sol.nfev
    if not sol.success or sol.nfev>50000:raise RuntimeError('INCOMPLETE_SOLVER')
    M=float(np.linalg.norm(y))+(math.sqrt(.05**2+.03**2+.02**2) if forced else 0.)
    assert max(np.linalg.norm(sol.y,axis=0))<=M+2e-9
    return sol.y.reshape(3,N+1,-1),M
def main():
    sym=symbolic();rows=[];maxdiff=0.;maxbessel=0.
    for k in [1.,4.,12.,24.]:
        X,M=run(k,96,'free','DOP853','physical',False)
        exact=np.sqrt(2*np.arange(97)+1.)[:,None]*spherical_jn(np.arange(97)[:,None],k*grid[None,:])
        err=float(np.max(abs(X[0]-exact)));assert err<2e-9;maxbessel=max(err,maxbessel)
        for model in ['physical','repository']:
            for profile in ['free','release','reentrant']:
                ref,M=run(k,96,profile,'DOP853',model);ref2,_=run(k,96,profile,'RK45',model)
                diff=float(np.max(abs(ref-ref2)));assert diff<3e-9;maxdiff=max(maxdiff,diff)
                referr=M*bound(k,190)
                for N in [4,8,16,32]:
                    small,_=run(k,N,profile,'DOP853',model)
                    low=float(max(np.linalg.norm((ref[:,:3]-small[:,:3]).reshape(9,-1),axis=0)))
                    tail=float(max(np.linalg.norm(ref[:,N+1:].reshape(-1,len(grid)),axis=0)))
                    B=M*bound(k,2*N-2);Bt=M*bound(k,N-1)
                    assert low<=B+referr+3e-9,(k,N,model,profile,low,B)
                    assert tail<=Bt+3e-9
                    rows.append(dict(k=k,N=N,model=model,profile=profile,low_error=low,low_bound=B,tail_norm=tail,tail_bound=Bt,reference_low_bound=referr))
    print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,symbolic=sym,integrations=calls,rhs_evaluations=nfev,grid_samples=len(grid),cases=len(rows),max_reference_solver_difference=maxdiff,max_free_streaming_bessel_error=maxbessel,rows=rows),indent=2))
if __name__=='__main__':main()
