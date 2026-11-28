#!/usr/bin/env python3
"""Prescribed-opacity perfect-fluid IVP, not a recombination/Boltzmann solver."""
import json, math, time
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp
T=.6; ts=np.linspace(0,T,241); amp=1e-5; g=1.5
s,b,r,l=.26,.05,.09,.60
start=time.monotonic(); calls=0; segments=0; nfev=0

def run(rhs,y,method,tol,step,knots=()):
    global calls,segments,nfev
    if calls>=100 or time.monotonic()-start>90: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
    calls+=1
    result=[]; ends=[0.,*knots,T]
    for left,right in zip(ends[:-1],ends[1:]):
        if segments>=180 or time.monotonic()-start>90: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
        segments+=1
        mask=(ts>=left)&(ts<right if right<T else ts<=right)
        sample=ts[mask]; evals=np.unique(np.r_[sample,right])
        sol=solve_ivp(rhs,(left,right),y,method=method,rtol=tol,atol=tol*.001,t_eval=evals,max_step=step)
        nfev+=sol.nfev
        if not sol.success or sol.nfev>200000: raise RuntimeError('INCOMPLETE_SOLVER')
        y=sol.y[:,-1]; result.append(sol.y[:,:len(sample)])
    return np.concatenate(result,axis=1)

def breakpoints(k,profile):
    return (.3,.3+1/(k*k)) if profile=='rapid' else ()

def opacity(t,k,profile):
    if profile in ('free','generic','matched'): return 0.
    if profile=='smooth': return 3*k*k*max(1-t/.3,0.)**2
    if profile=='rapid': return 3*k*k*max(min((.3+1/(k*k)-t)*k*k,1.),0.)
    if profile=='reentrant': return 3*k*k*(.5+.5*math.cos(8*math.pi*t/T))**2
    raise ValueError(profile)

def data(k,kap,profile):
    if profile in ('generic','matched'):
        A=amp*(.5-1j/kap); B=amp*(.15+.2j); db=.8*amp
        vb=.4*amp if profile=='generic' else .4*amp/k
    else:
        A=k*amp*(.5-1j/kap); B=k*amp*(.15+.2j); db=k*.2*amp; vb=.3*amp
    e=amp; vg=-.1*amp
    return A,B,db,e,vb,vg

def exact(m,kap,profile,method,tol):
    k=math.sqrt(m*kap); A,B,db,e,vb,vg=data(k,kap,profile)
    y=A+B; w=1j*(A-B)-1.5*y/m
    def coeff(z):
        a=z[0].real; x,vx,y,wy=z[1:5]; db,e,vb,vg=z[5:].real
        rho=(abs(x)**2+abs(vx)**2)/2; rb=b/a**3; rr=r/a**4
        H=math.sqrt(l+s*rho+rb+rr); p=k*k/a**2
        K=s*abs(vx)**2; rs0=s*np.real(np.conj(vx)*wy+np.conj(x)*y)
        q=s*np.real(np.conj(vx)*y)/m+a*(rb*vb+4*rr*vg/3)/k
        den=p-g*K
        if den<=0: raise RuntimeError('INCOMPLETE_CONSTRAINT_DENOMINATOR')
        P=-g*(rs0+rb*db+rr*e+3*H*q)/den; D=g*q-H*P
        return a,H,p,P,D,(rs0-K*P)/(s*rho),den/p
    def rhs(t,z):
        a,H,p,P,D,_,_=coeff(z); x,vx,y,wy=z[1:5]; db,e,vb,vg=z[5:].real
        R=3*b*a/(4*r); lam=opacity(t,k,profile); L=k/a; slip=vg-vb
        return np.array([a*H,m*vx,-3*H*vx-m*x,m*wy,-3*H*wy-(m+p/m)*y+4*vx*D-2*m*x*P,-L*vb+3*D,-4*L*vg/3+4*D,-H*vb+L*P+lam*slip/(1+R),L*(e/4+P)-lam*R*slip/(1+R)],complex)
    sol=run(rhs,np.array([1,1,1j,y,w,db,e,vb,vg],complex),method,tol,min(.35/m,1/(3*k*k)),breakpoints(k,profile))
    vals=np.array([coeff(z) for z in sol.T]); a=vals[:,0]; x,vx,y,wy=sol[1:5]; db,e,vb,vg=sol[5:].real
    assert np.max(abs(a**3*np.imag(np.conj(x)*vx)-1))<1e-7
    E=a**3*(abs(x)**2+abs(vx)**2)/2
    assert min(E)>=1-1e-7 and max(E)<=1+24/m**2+1e-7
    Y=a**1.5*y; W=a**1.5*(wy+1.5*vals[:,1]*y/m)
    A=(Y-1j*W)*np.exp(-1j*m*ts)/2/k; B=(Y+1j*W)*np.exp(1j*m*ts)/2/k
    R=3*b*a/(4*r); v=(R*vb+vg)/(1+R)
    return a,np.array([vals[:,5]/k,db/k,e,v,vg-vb,A.real,A.imag,B.real,B.imag])/amp,float(min(vals[:,6]))

def reduced(m,kap,profile):
    k=math.sqrt(m*kap); A,B,db,e,vb,vg=data(k,kap,profile); R0=3*b/(4*r)
    def rhs(t,z):
        a,ar,ai,br,bi,db,e,v,w=z; H=math.sqrt(l+(s+b)/a**3+r/a**4); R=3*b*a/(4*r); L=k/a
        P=-g*(2*s*ar+b*db)/(kap*a); om=kap/(2*a*a); lam=opacity(t,k,profile)
        return [a*H,-om*ai,om*ar+P,om*bi,-om*br,-(v-w/(1+R))/a,-4*L/3*(v+R*w/(1+R)),-H*R*v/(1+R)+kap*P/a+L*e/(4*(1+R)),H*v+L*e/4-(lam+H/(1+R))*w]
    sol=run(rhs,[1,A.real/k,A.imag/k,B.real/k,B.imag/k,db/k,e,(R0*vb+vg)/(1+R0),vg-vb],'DOP853',2e-12,min(.025,1/(3*k*k)),breakpoints(k,profile))
    a,ar,ai,br,bi,db,e,v,w=sol
    return a,np.array([2*ar,db,e,v,w,ar,ai,br,bi])/amp

def symbolic():
    H,R,L,lam,v,w,e,P,D=sp.symbols('H R L lam v w e P D')
    vb=v-w/(1+R); vg=v+R*w/(1+R)
    bd=-H*vb+L*P+lam*w/(1+R); gd=L*(e/4+P)-lam*R*w/(1+R); ed=-sp.Rational(4,3)*L*vg+4*D
    vd=-H*R*v/(1+R)+L*(P+e/(4*(1+R))); wd=H*v+L*e/4-(lam+H/(1+R))*w
    Fd=H*R*vb**2+2*R*vb*bd+2*vg*gd+sp.Rational(3,8)*e*ed
    assert sp.cancel(Fd-(-H*R*vb**2-2*lam*R*w*w/(1+R)+2*L*P*(R*vb+vg)+sp.Rational(3,2)*e*D))==0
    assert sp.cancel(gd-bd-wd)==0
    assert sp.cancel((H*R*vb+R*bd+gd-H*R*v)/(1+R)-vd)==0
    assert sp.cancel(R*(bd+H*vb-L*P)+(gd-L*(e/4+P)))==0
    # Reduced weighted energy is the same form; no derivative of lambda.
    Fmean=(1+R)*v*v+R*w*w/(1+R)+sp.Rational(3,16)*e*e
    assert sp.cancel(Fmean-(R*vb*vb+vg*vg+sp.Rational(3,16)*e*e))==0
    return dict(energy=0,slip=0,mean=0,collision_momentum=0,energy_coordinates=0)

def main():
    sym=symbolic(); rows=[]
    for kap in [1.,4.]:
        for profile in ['smooth','rapid','reentrant','generic','matched']:
            for m in [16,32,64]:
                k=math.sqrt(m*kap)
                a,targ=reduced(m,kap,profile)
                aa,y,den=exact(m,kap,profile,'DOP853',2e-10)
                ab,yy,_=exact(m,kap,profile,'RK45',2e-11)
                diff=float(np.max(abs(y-yy))); assert diff<3e-6, (kap,m,profile,diff,np.unravel_index(np.argmax(abs(y-yy)),y.shape))
                errors=np.max(abs(y-targ),axis=1)
                rows.append(dict(kappa=kap,m=m,profile=profile,scaled_max_error=float(max(errors)),scaled_matter_error=float(max(errors[:2])),solver_disagreement=diff,background_error=float(max(abs(aa/a-1))),min_denominator=den,baryon_unscaled_max=float(k*max(abs(y[1]))),baryon_scaled_final=float(y[1,-1]),baryon_unscaled_final=float(k*y[1,-1]),reference_scaled_final=float(targ[1,-1])))
            rr=rows[-3:]
            assert rr[-1]['scaled_max_error']<rr[0]['scaled_max_error']
    handoff=[]
    for kap in [1.,4.]:
        def response(t,z):
            a,ds,vs,db,vb=z; H=math.sqrt(l+(s+b)/a**3+r/a**4); grav=g*(s*ds+b*db)/a**3
            return [a*H,vs,-2*H*vs-kap**2*ds/(4*a**4)+grav,vb,-2*H*vb+grav]
        unit=run(response,[1,0,0,0,-1],'DOP853',1e-12,.025)[3,-1]
        assert unit<-.1
        for m in [16,32,64]:
            k=math.sqrt(m*kap)
            x,y=[next(z for z in rows if z['kappa']==kap and z['m']==m and z['profile']==p) for p in ['generic','matched']]
            pred=.4*(1-1/k)*unit
            ref=x['reference_scaled_final']-y['reference_scaled_final']
            measured=x['baryon_scaled_final']-y['baryon_scaled_final']
            assert abs(ref-pred)<2e-9
            handoff.append(dict(kappa=kap,m=m,unit_response=float(unit),predicted_scaled_difference=float(pred),reduced_scaled_difference=ref,full_scaled_difference=measured,unscaled_difference=k*measured))
        assert abs(handoff[-1]['unscaled_difference'])>abs(handoff[-3]['unscaled_difference'])
    print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,symbolic=sym,integrations=calls,solver_segments=segments,rhs_evaluations=nfev,grid_samples=len(ts),cases=rows,handoff=handoff,scope='prescribed collision relaxation rate; perfect photon fluid; not realistic recombination or primordial transfer'),indent=2))
if __name__=='__main__':main()
