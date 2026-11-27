"""Independent continuation of July 21 conditional solution; no early-time calibration or joint fit."""
import json, numpy as np, scipy
from scipy.integrate import solve_ivp, quad
from bao_data import z,y,kind,C,w
m2=256.0366189147147; m=np.sqrt(m2); Q=.048621919894669685
Ni=-.1; Nmin=-np.log1p(max(z)); phi=.06404492230824137
ob=.049309230511847414; oc=.264156592027754; ore=9.2e-5; ol=1-ob-oc-ore
init=np.array([phi,0.,0.,Q*np.exp(-3*Ni)/phi])
def quantities(N,s):
    x=s[:2]; v=s[2:]; rho=(v@v+m2*(x@x))/2
    H=np.sqrt(ol+ob*np.exp(-3*N)+ore*np.exp(-4*N)+rho/3)
    return H,rho,(v@v-m2*(x@x))/2,np.exp(3*N)*(x@v),np.exp(3*N)*(x[0]*v[1]-x[1]*v[0])
def rhs(N,s):
    H,*_=quantities(N,s)
    return np.r_[s[2:]/H,-3*s[2:]-m2*s[:2]/H]
def run(method,rtol,atol):
    lo=solve_ivp(rhs,(Ni,Nmin),init,method=method,rtol=rtol,atol=atol,dense_output=True,max_step=.02)
    hi=solve_ivp(rhs,(Ni,0),init,method=method,rtol=rtol,atol=atol,dense_output=True,max_step=.02)
    assert lo.success and hi.success
    def get(N): return quantities(N,(lo if N<Ni else hi).sol(N))
    Ns=np.linspace(Nmin,0,4001); vals=np.array([get(t) for t in Ns]); H,rho,p,J,charge=vals.T
    E=np.exp(3*Ns)*rho; eps=1.5*H/m; I=E+1.5*H*J
    assert np.all(E**2 >= m2*(charge**2+J**2)-1e-10)
    assert max(eps)<1 and min(I)>0 and np.all(np.diff(H)<=1e-10)
    # exact endpoint bounds for E(t)/E(today), t earlier than today
    # I(t)/I(0) in [ (1-eps(t))/(1-eps(0)), reciprocal ]; E(t)/E(0) via endpoints
    low=(1-eps)/(1-eps[-1])*I[-1]/E[-1]/(1+eps)
    high=(1-eps[-1])/(1-eps)*I[-1]/E[-1]/(1-eps)
    assert np.all(E/E[-1]>=low-1e-8) and np.all(E/E[-1]<=high+1e-8)
    H0,rho0,p0,_,_=get(0); assert abs(H0-1)<2e-8 and abs(rho0-3*oc)<2e-8 and abs(p0)<2e-8
    assert np.max(np.abs(charge-Q))<1e-8
    dm={t:quad(lambda x:1/get(-np.log1p(x))[0],0,t,epsabs=2e-10,epsrel=2e-10,points=[np.expm1(-Ni)] if t>np.expm1(-Ni) else None)[0] for t in set(z)}
    f=np.array([dm[t] if k=='DM' else 1/get(-np.log1p(t))[0] if k=='DH' else (t*dm[t]**2/get(-np.log1p(t))[0])**(1/3) for t,k in zip(z,kind)])
    A=float(f@w(y)/(f@w(f))); r=y-A*f; ch=float(r@w(r)); assert abs(ch-r@np.linalg.solve(C,r))<1e-9
    Hlcd=np.sqrt(ol+(ob+oc)*np.exp(-3*Ns)+ore*np.exp(-4*Ns))
    return dict(method=method,rtol=rtol,atol=atol,nfev=lo.nfev+hi.nfev,max_charge_error=float(max(abs(charge-Q))),present_H=H0,present_rho=rho0,present_p=p0,H_at_max_z=float(H[0]),epsilon_max=float(max(eps)),comoving_E_ratio_min=float(min(E/E[-1])),comoving_E_ratio_max=float(max(E/E[-1])),max_abs_H_fractional_difference_from_matched_LCDM=float(max(abs(H/Hlcd-1))),earliest_energy_ratio_bounds=[float(low[0]),float(high[0])],profiled_A=A,chi2=ch,predictions=(A*f).tolist())
a=run('DOP853',1e-10,1e-12); b=run('RK45',2e-12,2e-14)
assert abs(a['chi2']-b['chi2'])<1e-6 and max(abs(np.array(a['predictions'])-b['predictions']))<1e-7
# Matched LCDM (same fixed density fractions and independently profiled amplitude).
h=lambda t: np.sqrt(ol+(ob+oc)*(1+t)**3+ore*(1+t)**4)
dm={t:quad(lambda x:1/h(x),0,t,epsabs=1e-12)[0] for t in set(z)}
f=np.array([dm[t] if k=='DM' else 1/h(t) if k=='DH' else (t*dm[t]**2/h(t))**(1/3) for t,k in zip(z,kind)])
A=float(f@w(y)/(f@w(f))); r=y-A*f; ch=float(r@w(r))
print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,repo_revision='ea4f548e5c9b3160ea0a4dde76cab74be6a4964f',source='July 21 conditional calibration receipt; Cartesian continuation, not new shooting or early-time calibration',grid_points=4001,redshift_max=float(max(z)),runs=[a,b],matched_fixed_LCDM=dict(profiled_A=A,chi2=ch),delta_chi2_canonical_minus_matched=a['chi2']-ch,early_time_sound_horizon='NOT_RUN',growth='NOT_RUN',joint_fit='NOT_RUN'),indent=2))
