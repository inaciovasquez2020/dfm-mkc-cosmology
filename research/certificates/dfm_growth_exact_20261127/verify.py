#!/usr/bin/env python3
"""Independent Bessel/ODE comparison for the averaged matter-era IVP only."""
import json, math, time
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn, spherical_yn

def exact(q,t):
    if q == 0: return np.ones_like(t)
    xi=2*math.sqrt(q); x=xi*np.exp(-np.asarray(t)/2)
    return x**3/xi*(spherical_yn(1,xi)*spherical_jn(2,x)-spherical_jn(1,xi)*spherical_yn(2,x))

def limit(q):
    if q==0: return 1.
    xi=2*math.sqrt(q)
    return 3*spherical_jn(1,xi)/xi

def F(t):
    return .4*(-np.expm1(-t)-(np.exp(-t)-np.exp(-2.5*t))/1.5)

def main():
    start=time.monotonic(); count=0; worst=0.; solver_diff=0.; nfev=0; checks=0; limerr=0.; repo=[]
    qs=sorted(set([0.,1e-10,1e-8,1e-6,1e-4,.00390625,.0625,.31640625,1.5,5.,20.,100.,400.]+list(np.geomspace(.001,100,48))))
    # repository k=.5,1,1.5, m=2,H1=1,ai=.25 => q=k^4/4
    qs=sorted(set(qs+[k**4/4 for k in [0.,.5,1.,1.5]]))
    ts=np.linspace(0,16,641)
    for q in qs:
        def rhs(t,y): return [y[1],-2.5*y[1]-q*math.exp(-t)*y[0]]
        sols=[]
        for method,tol in [('DOP853',2e-11),('RK45',2e-11)]:
            if time.monotonic()-start>40 or count>=150: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
            s=solve_ivp(rhs,(0,16),[1.,0.],t_eval=ts,rtol=tol,atol=tol*.01,method=method,max_step=.1)
            count+=1; nfev+=s.nfev
            if not s.success or s.nfev>50000: raise RuntimeError('INCOMPLETE_SOLVER')
            sols.append(s.y)
        a=exact(q,ts); err=float(max(abs(a-sols[0][0]))); worst=max(worst,err)
        solver_diff=max(solver_diff,float(max(abs(sols[0][0]-sols[1][0]))))
        assert err<2e-8 and max(abs(sols[0][0]-sols[1][0]))<2e-8
        assert np.max(abs(a))<=1+1e-10
        assert np.all(1-a<=q*F(ts)+1e-10)
        if q<=1.5:
            assert np.min(a)>=.4-1e-10 and np.all(np.diff(a)<=1e-10)
            assert np.all(1-a>=q*F(ts)*(1-q*F(ts))-1e-10)
        if q>0:
            energy=sols[0][0]**2+sols[0][1]**2*np.exp(ts)/q
            assert np.max(np.diff(energy))<1e-7
        limerr=max(limerr,abs(float(exact(q,40))-limit(q)))
        checks+=len(ts)
    observed=[1.,.9962278801932982,.9405803367049294,.7189321621883279]
    for k,old in zip([0.,.5,1.,1.5],observed):
        q=k**4/4; v=float(exact(q,math.log(4)))
        assert abs(v-old)<2e-10
        repo.append(dict(k=k,q=q,exact_ratio=v,repository_ratio=old,absolute_error=abs(v-old),late_transfer=limit(q)))
    assert limerr<1e-10
    # independent quadrature of the normalized spherical top-hat Fourier transform
    from scipy.integrate import quad
    for q in qs:
        xi=2*math.sqrt(q)
        val=quad(lambda u:3*u*u*np.sinc(xi*u/np.pi),0,1,epsabs=1e-12)[0]
        assert abs(val-limit(q))<1e-11
    print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,repository_revision='ea4f548e5c9b3160ea0a4dde76cab74be6a4964f',q_count=len(qs),ode_integrations=count,total_rhs_evaluations=nfev,analytic_grid_checks=checks,max_exact_vs_ode_error=worst,max_independent_ode_difference=solver_diff,max_late_limit_error=limerr,repository_cases=repo,scope='averaged EdS equation only; signed IVP transfer, not full-field or empirical power spectrum'),indent=2))
if __name__=='__main__': main()
