#!/usr/bin/env python3
"""Independent scalar+interacting perfect photon/dust fluid IVP, finite time only."""
import json, math, time
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp
T=0.8; ts=np.linspace(0,T,321); amp=1e-5; g=1.5
s,b,r,l=.26,.05,.09,.60
start=time.monotonic(); calls=0; nfev=0

def run(rhs,y,method,tol,step):
 global calls,nfev
 if calls>=100 or time.monotonic()-start>90: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
 calls+=1
 sol=solve_ivp(rhs,(0,T),y,method=method,rtol=tol,atol=tol*.001,t_eval=ts,max_step=step)
 nfev+=sol.nfev
 if not sol.success or sol.nfev>180000: raise RuntimeError('INCOMPLETE_SOLVER')
 return sol.y

def symbolic():
 R,H,K,G,vb,vg,e,P,D=sp.symbols('R H K G vb vg e P D')
 w=vg-vb; v=(R*vb+vg)/(1+R)
 bd=-H*vb+K*P+G*w/R; gd=K*(e/4+P)-G*w; ed=-sp.Rational(4,3)*K*vg+4*D
 Eder=H*R*vb**2+2*R*vb*bd+2*vg*gd+sp.Rational(3,8)*e*ed
 assert sp.cancel(Eder-(-H*R*vb**2-2*G*w*w+2*K*P*(R*vb+vg)+sp.Rational(3,2)*e*D))==0
 vd=(H*R*vb+R*bd+gd-H*R*v)/(1+R)
 assert sp.cancel(vd-(-H*R*v/(1+R)+K*(P+e/(4*(1+R)))))==0
 assert sp.cancel(gd-bd-(H*v+K*e/4-(G*(1+1/R)+H/(1+R))*w))==0
 # Conservation of total momentum and propagation of Einstein constraints.
 p,g,Ks,X,Y,C,rb,rr,db,qs,qb,qr=sp.symbols('p g Ks X Y C rb rr db qs qb qr')
 Q=qs+qb+qr; D=g*Q-H*P; Hd=-g*(Ks+rb+4*rr/3)
 L=X+Y-Ks*P+rb*db+rr*e; Pr=X-Y-Ks*P+rr*e/3
 J=sp.symbols('J'); qsd=-3*H*qs+X-Y; qbd=-3*H*qb+rb*P+J; qrd=-3*H*qr+rr*e/3+4*rr*P/3-J
 Qd=qsd+qbd+qrd
 Ld=-6*H*X-p*qs+4*Ks*D-2*C*P-(-6*H*Ks-2*C)*P-Ks*D-3*H*rb*db-p*qb+3*rb*D-4*H*rr*e-p*qr+4*rr*D
 constraint=p*P+g*(L+3*H*Q)
 assert sp.expand(p*(D-2*H*P)+g*(Ld+3*Hd*Q+3*H*Qd)+3*H*constraint)==0
 assert sp.expand(g*Qd-Hd*P-H*D+4*H*D+(2*Hd+3*H**2)*P-g*Pr)==0
 return dict(energy=0,mean=0,slip=0,constraint=0,trace=0)

def full(m,kappa,mode,method,tol):
 k=math.sqrt(m*kappa); rate=k*k*math.sqrt(m)
 A=amp*(.5-1j/kappa); B=amp*(.15+.2j); e=amp; sigma=.2*amp
 R0=3*b/(4*r); v=.3*amp; w0=(.4*amp if mode=='slip' else 0.)
 vb=v-w0/(1+R0); vg=v+R0*w0/(1+R0); db=sigma+.75*e
 y=A+B; w=1j*(A-B)-1.5*y/m
 def coeff(z):
  a=z[0].real; x,vx,y,wy=z[1:5]; db,e,vb,vg=z[5:].real
  rho=(abs(x)**2+abs(vx)**2)/2; rb=b/a**3; rr=r/a**4; H=math.sqrt(l+s*rho+rb+rr); p=m*kappa/a**2
  K=s*abs(vx)**2; rs0=s*np.real(np.conj(vx)*wy+np.conj(x)*y); q=s*np.real(np.conj(vx)*y)/m+a*(rb*vb+4*rr*vg/3)/k
  den=p-g*K
  if den<=0: raise RuntimeError('INCOMPLETE_DENOMINATOR')
  P=-g*(rs0+rb*db+rr*e+3*H*q)/den; D=g*q-H*P
  return a,H,p,P,D,(rs0-K*P)/(s*rho),den/p
 def rhs(t,z):
  a,H,p,P,D,_,_=coeff(z); x,vx,y,wy=z[1:5]; db,e,vb,vg=z[5:].real
  R=3*b*a/(4*r); G=rate*R/(1+R); w=vg-vb; K=k/a
  return np.array([a*H,m*vx,-3*H*vx-m*x,m*wy,-3*H*wy-(m+p/m)*y+4*vx*D-2*m*x*P,-K*vb+3*D,-4*K*vg/3+4*D,-H*vb+K*P+G*w/R,K*(e/4+P)-G*w],complex)
 sol=run(rhs,np.array([1,1,1j,y,w,db,e,vb,vg],complex),method,tol,min(.4/m,1/rate))
 vals=np.array([coeff(z) for z in sol.T]); a=vals[:,0]; x,vx=sol[1:3]; db,e,vb,vg=sol[5:].real; R=3*b*a/(4*r)
 assert np.max(abs(a**3*np.imag(np.conj(x)*vx)-1))<1e-7
 E=a**3*(abs(x)**2+abs(vx)**2)/2
 assert min(E)>=1-1e-7 and max(E)<=1+24/m**2+1e-7
 obs=np.array([vals[:,5],db,e,(R*vb+vg)/(1+R),db-.75*e,(vg-vb)])/amp
 return a,obs,float(min(vals[:,6])),rate

def reduced(m,kappa):
 k=math.sqrt(m*kappa)
 def rhs(t,z):
  a,ds,vs,e,v=z; H=math.sqrt(l+(s+b)/a**3+r/a**4); R=3*b*a/(4*r); K=k/a
  return [a*H,vs,-2*H*vs-kappa*kappa*ds/(4*a**4)+g*(s*ds+b*.2*amp)/a**3,-4*K*v/3,-H*R*v/(1+R)+K*e/(4*(1+R))]
 sol=run(rhs,[1,amp,amp,amp,.3*amp],'DOP853',1e-12,.025)
 a,ds,vs,e,v=sol
 return a,np.array([ds,.2*amp+.75*e,e,v,np.full_like(e,.2*amp)])/amp

def spectral():
 # constant-background unforced fluid. lambda is the slip decay rate.
 rows=[]
 for R in [.2,1.,4.]:
  for alpha in [.2,1.,5.]:
   for k in [16.,64.,256.,1024.]:
    Gamma=alpha*k*k; L=Gamma*(1+1/R); c2=1/(3*(1+R)); d=R/(3*(1+R))
    roots=np.roots([1,L,k*k*(c2+d),L*k*k*c2]); z=roots[np.argmax(roots.imag)]; expected=-R**2/(6*alpha*(1+R)**2)
    assert z.imag>0 and z.real<0
    if k==1024: assert abs(z.real/expected-1)<1e-4
    rows.append(dict(R=R,alpha=alpha,k=k,real=float(z.real),predicted_decay=expected,imag_over_k=float(z.imag/k)))
 return rows

def main():
 sym=symbolic(); rows=[]
 for kap in [1.,4.]:
  for m in [16,32,64,128]:
   a0,targ=reduced(m,kap)
   for mode in ['matched','slip']:
    a,y,den,L=full(m,kap,mode,'DOP853',2e-10)
    aa,yy,_,_=full(m,kap,mode,'RK45',2e-11)
    diff=float(np.max(abs(y-yy))); assert diff<3e-6
    err=np.max(abs(y[:5]-targ),axis=1)
    rows.append(dict(kappa=kap,m=m,mode=mode,lambda_over_k2=L/(m*kap),scalar_error=float(err[0]),baryon_error=float(err[1]),photon_error=float(err[2]),mean_velocity_error=float(err[3]),entropy_error=float(err[4]),final_slip=float(abs(y[5,-1])),solver_difference=diff,background_error=float(max(abs(a/a0-1))),min_denominator=den))
 for kap in [1.,4.]:
  for mode in ['matched','slip']:
   v=[x for x in rows if x['kappa']==kap and x['mode']==mode]
   for key in ['scalar_error','baryon_error','photon_error','entropy_error']: assert v[-1][key]<v[0][key]
 print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,symbolic=sym,cases=rows,integrations=calls,rhs_evaluations=nfev,grid_samples=len(ts),spectral_cases=spectral()),indent=2))
if __name__=='__main__':main()
