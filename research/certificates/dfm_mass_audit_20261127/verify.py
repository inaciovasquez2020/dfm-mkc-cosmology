import json, math, time, sys
import numpy as np, scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from bao_data import z,y,kind,C,w
ob=.049309230511847414; oc=.264156592027754; ore=9.2e-5; ol=1-ob-oc-ore
Ni=-.1; Nmin=-np.log1p(max(z)); E0=3*oc
start=time.monotonic(); calls=0
# state (m Re psi,m Im psi, Re dot psi, Im dot psi, distance integral)
def evolve(m,Ei,Nstart,Nend,rtol=2e-9,method='DOP853',dense=False):
 global calls
 calls+=1
 if calls>1600 or time.monotonic()-start>90: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
 amp=np.sqrt(Ei*np.exp(-3*Nstart))
 def rhs(N,s):
  x=s[:2]; v=s[2:4]; rho=(x@x+v@v)/2
  H=np.sqrt(ol+ob*np.exp(-3*N)+ore*np.exp(-4*N)+rho/3)
  return np.r_[m*v/H,-3*v-m*x/H,-np.exp(-N)/H]
 sol=solve_ivp(rhs,(Nstart,Nend),[amp,0,0,amp,0],rtol=rtol,atol=rtol*.01,method=method,max_step=.025,dense_output=dense)
 if not sol.success or sol.nfev>100000: raise RuntimeError('INCOMPLETE_SOLVER')
 return sol

def calibrate(m,tol=2e-9,method='DOP853'):
 def res(Ei):
  s=evolve(m,Ei,Ni,0,tol,method).y[:4,-1]; return s@s/2-E0
 Ei=brentq(res,E0*.5,E0*1.5,xtol=1e-12)
 s=evolve(m,Ei,Ni,0,tol,method).y[:4,-1]; p=(s[2:]@s[2:]-s[:2]@s[:2])/2
 return Ei,p/E0

def measure(m,Ei,initial=Ni,method='DOP853',tol=2e-10):
 lo=evolve(m,Ei,initial,Nmin,tol,method,True); hi=evolve(m,Ei,initial,0,tol,method,True) if initial<0 else None
 def get(N):
  s=(lo if N<=initial or hi is None else hi).sol(N); x=s[:2];v=s[2:4];rho=(x@x+v@v)/2; H=np.sqrt(ol+ob*np.exp(-3*N)+ore*np.exp(-4*N)+rho/3)
  return H,rho,np.exp(3*N)*(x[0]*v[1]-x[1]*v[0]),s[4]
 H0,rho0,_,d0=get(0); assert abs(rho0/E0-1)<1e-6
 Ns=np.linspace(Nmin,0,4001); vals=np.array([get(N) for N in Ns]); H,rho,q,_=vals.T; E=rho*np.exp(3*Ns); eps=1.5*max(H)/m
 assert max(abs(q/Ei-1))<2e-6 and min(E/Ei)>1-2e-6
 if 2*eps<1: assert max(E/Ei)<=(1+4*eps**2)/(1-4*eps**2)+2e-6
 h=lambda N: np.sqrt(ol+(ob+oc)*np.exp(-3*N)+ore*np.exp(-4*N))
 f=[]
 for zz,k in zip(z,kind):
  hz,_,_,dd=get(-np.log1p(zz)); dm=dd-d0; dh=1/hz
  f.append(dm if k=='DM' else dh if k=='DH' else (zz*dm**2*dh)**(1/3))
 f=np.array(f); A=float(f@w(y)/(f@w(f))); r=y-A*f; chi=float(r@w(r))
 return dict(m_over_H0=m,Ei=Ei,chi2=chi,max_H_rel=float(max(abs(H/h(Ns)-1))),max_E_excess=float(max(E/Ei-1)),epsilon_star=float(eps),nfev=lo.nfev+(hi.nfev if hi else 0))

def main():
 grid=np.arange(8.,129.,2.); vals=[calibrate(m)[1] for m in grid]; roots=[]
 for a,b,fa,fb in zip(grid[:-1],grid[1:],vals[:-1],vals[1:]):
  if fa*fb<0:
   m=brentq(lambda x:calibrate(x)[1],a,b,xtol=1e-9); Ei,p=calibrate(m,2e-11); assert abs(p)<2e-7
   v=measure(m,Ei); v['w_today']=p; Ei2,p2=calibrate(m,2e-12,'RK45'); v2=measure(m,Ei2,method='RK45',tol=2e-12); assert abs(v['chi2']-v2['chi2'])<1e-4 and abs(p2)<2e-7; roots.append(v)
 # relaxed branch: circular initial condition today, no historical circular condition
 relaxed=[measure(m,E0,0) for m in [16,32,64,128,256,512]]
 from scipy.integrate import quad
 h=lambda zz:np.sqrt(ol+(ob+oc)*(1+zz)**3+ore*(1+zz)**4)
 f=np.array([quad(lambda x:1/h(x),0,zz)[0] if k=='DM' else 1/h(zz) if k=='DH' else (zz*quad(lambda x:1/h(x),0,zz)[0]**2/h(zz))**(1/3) for zz,k in zip(z,kind)]); A=float(f@w(y)/(f@w(f)));r=y-A*f
 print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,mass_grid=grid.tolist(),pressure_residuals=vals,sign_change_roots=roots,relaxed_present_circular=relaxed,lcdm_chi2=float(r@w(r)),ode_calls=calls,scope='sign-change scan only; not exhaustive root isolation; fixed densities, profiled BAO amplitude; no growth or early-time calibration'),indent=2))
if __name__=='__main__': main()
