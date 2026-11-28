#!/usr/bin/env python3
"""Canonical scalar + physical Legendre photon polarization brightness + massless neutrinos.
No recombination, no observational outputs. Real Fourier harmonic. Cosmic time.
"""
import json, math, time, signal
import numpy as np
import scipy, sympy as sp
from scipy.integrate import solve_ivp
T=.6; grid=np.linspace(0,T,161); g=1.5
s,b,r,n,ell=.26,.05,.06,.03,.60
start=time.monotonic(); calls=0; nfev=0

def guard(*_): raise RuntimeError('INCOMPLETE_WALL_CLOCK')

def symbolic():
    # R and X are the lapse-corrected kinetic and potential cross terms.
    p,H,g,K,C,R,X,Q,rb,rr,rn,d,e,f,Phi,Psi,D,J,S=sp.symbols('p H g K C R X Q rb rr rn d e f Phi Psi D J S')
    W=K+rb+4*(rr+rn)/3
    L=R+X+rb*d+rr*e+rn*f; P=R-X+(rr*e+rn*f)/3
    Hd=-g*W
    # Individual momentum equations with arbitrary exchange and stress.
    qs,qb,qg,qn,sg,sn=sp.symbols('qs qb qg qn sg sn')
    Q=qs+qb+qg+qn; S=4*(rr*sg+rn*sn)/3
    D=g*Q-H*Psi
    Qd=(-3*H*qs+R-X+K*Psi)+(-3*H*qb+rb*Psi+J)+(-3*H*qg+rr*e/3+4*rr*(Psi-sg)/3-J)+(-3*H*qn+rn*f/3+4*rn*(Psi-sn)/3)
    Ld=-6*H*R-p*qs+3*K*D-3*H*rb*d-p*qb+3*rb*D-4*H*rr*e-p*qg+4*rr*D-4*H*rn*f-p*qn+4*rn*D
    assert sp.expand(Ld+3*H*(L+P)+p*Q-3*W*D)==0
    assert sp.expand(Qd+3*H*Q-P-W*Psi+S)==0
    constraint=p*Phi+g*(L+3*H*Q); slip=p*(Phi-Psi)-3*g*S
    Fd=p*(D-2*H*Phi)+g*(Ld+3*Hd*Q+3*H*Qd)
    assert sp.expand(Fd+3*H*constraint-H*slip)==0  # see derivative identity sign below
    psid=sp.symbols('psid'); Dd=g*Qd-Hd*Psi-H*psid
    assert sp.expand(Dd+3*H*D+H*psid+(2*Hd+3*H**2)*Psi+g*S-g*P)==0
    # Derivative-free change, abstract independent real component.
    m,psi,v,eta,ch,Psid=sp.symbols('m psi v eta ch Psid')
    vd=-3*H*v-m*m*psi; etad=ch+v*Psi
    etadd=-3*H*etad-(m*m+p)*eta+v*(Psid+3*D)-2*m*m*psi*Psi
    chd=sp.expand(etadd-vd*Psi-v*Psid)
    assert sp.expand(chd-(-3*H*ch-(m*m+p)*eta+3*v*D-m*m*psi*Psi))==0
    assert sp.expand(vd*ch+v*chd+m*m*(v*eta+psi*etad)-(-6*H*v*ch-p*v*eta+3*v*v*D))==0
    # Collision block, and dipole/baryon dissipation, after normalization.
    Lc=-sp.eye(3)+sp.Matrix([sp.Rational(1,10),sp.Rational(1,2),sp.Rational(1,10)])*sp.ones(1,3); Wc=sp.diag(5,1,5)
    assert Wc*Lc==Lc.T*Wc and Lc.eigenvals()=={-sp.Rational(3,10):1,-1:2}
    return dict(total_energy=0,total_momentum=0,constraint_propagation=0,trace=0,proper_velocity_transform=0,scalar_energy=0,collision_eigenvalues=['-1','-1','-3/10'])

def run(rhs,y,method,tol,step):
    global calls,nfev
    if calls>=140 or time.monotonic()-start>100: raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
    calls+=1
    sol=solve_ivp(rhs,(0,T),y,method=method,rtol=tol,atol=tol*.005,t_eval=grid,max_step=step)
    nfev+=sol.nfev
    if not sol.success or sol.nfev>150000: raise RuntimeError('INCOMPLETE_SOLVER')
    return sol.y

def rate(t,k,profile):
    if profile=='free':return 0.
    if profile=='release':return k*k*max(1-t/(T*.5),0.)**2
    if profile=='reentrant':return k*k*(.5+.5*math.cos(6*math.pi*t/T))**2
    raise ValueError(profile)

def init(N):
    # Weighted-norm finite low data, including nonzero polarization and shear.
    F=np.zeros((3,N+1));F[0,:3]=[.15,.08,-.04];F[1,:3]=[.03,-.02,.05];F[2,:3]=[.12,-.06,.07]
    return .5-.2j,.15+.1j,.2,.3,F

def solve(m,kap,N,profile,method='DOP853',tol=2e-10,reduced=False):
    k=math.sqrt(m*kap); weights=2*np.arange(N+1)+1.; lidx=np.arange(1,N+1)
    A,B,d,vb,F=init(N)
    def pack(a,x,v,y,w,d,vb,F):return np.r_[a,x.real,x.imag,v.real,v.imag,y.real,y.imag,w.real,w.imag,d,vb,F.ravel()]
    def unpack(z):return z[0],complex(*z[1:3]),complex(*z[3:5]),complex(*z[5:7]),complex(*z[7:9]),z[9],z[10],z[11:].reshape(3,N+1)
    def coeff(z):
        a,x,v,y,w,d,vb,F=unpack(z); rb=b/a**3; rg=r/a**4; rn=n/a**4; R=3*rb/(4*rg); L=k/a; p=L*L
        rho=(abs(x)**2+abs(v)**2)/2
        H=math.sqrt(ell+s*(a**-3 if reduced else rho)+rb+rg+rn)
        if reduced:
            P0=-g*(2*s*y.real+b*d)/(kap*a); Psi=k*P0/m; Phi=Psi; D=0.; ds=2*y.real
        else:
            Q=s*k/m*np.real(np.conj(v)*y)+a/k*(rb*vb+4*rg*F[0,1]+4*rn*F[2,1])
            sr=s*k*np.real(np.conj(v)*w+np.conj(x)*y)
            Phi=-g*(sr+rb*k*d+4*rg*F[0,0]+4*rn*F[2,0]+3*H*Q)/p
            shear=8/3*(rg*F[0,2]+rn*F[2,2]); Psi=Phi-3*g*shear/p; D=g*Q-H*Psi; ds=sr/(s*rho*k)
        return a,H,R,L,p,Phi,Psi,D,ds
    def rhs(t,z):
        a,x,v,y,w,d,vb,F=unpack(z); a,H,R,L,p,Phi,Psi,D,ds=coeff(z); G=rate(t,k,profile)
        out=np.zeros_like(F);out[:,1:]+=L*lidx/weights[1:]*F[:,:-1];out[:,:-1]-=L*lidx/weights[:-1]*F[:,1:]
        # Ma-Bertschinger photon temperature and polarization brightness, neutrino F/4.
        Pi=F[0,2]+F[1,0]+F[1,2]
        out[0,1:]-=G*F[0,1:];out[0,1]+=G*vb/3;out[0,2]+=G*Pi/10
        out[1]-=G*F[1];out[1,0]+=G*Pi/2;out[1,2]+=G*Pi/10
        out[0,0]+=D;out[2,0]+=D;out[0,1]+=L*Psi/3;out[2,1]+=L*Psi/3
        vbd=-H*vb+L*Psi+G*(3*F[0,1]-vb)/R
        if reduced:
            om=kap/(2*a*a); P0=m*Psi/k
            return pack(a*H,0j,0j,1j*(om*y+P0),-1j*om*w,-vb/a,vbd,out)
        return pack(a*H,m*v,-3*H*v-m*x,m*w+m/k*v*Psi,-3*H*w-(m+p/m)*y+3/k*v*D-m/k*x*Psi,-vb/a+3*D/k,vbd,out)
    if reduced:y,w=A,B
    else:y=A+B;w=1j*(A-B)-1.5*y/m
    z=run(rhs,pack(1,1+0j,1j,y,w,d,vb,F),method,tol,min(.035,.4/m,1/(k*k+1)))
    a=z[0]; out=[]; norms=[]; cons=[]
    for t,zt in zip(grid,z.T):
        a0,x,v,y,w,d,vb,F=unpack(zt); a0,H,R,L,p,Phi,Psi,D,ds=coeff(zt)
        if reduced:A,B=y,w
        else:
            Y=a0**1.5*y; W=a0**1.5*(w+1.5*H*y/m)
            A=(Y-1j*W)*np.exp(-1j*m*t)/2; B=(Y+1j*W)*np.exp(1j*m*t)/2
        # Fixed norm uses sqrt(R/3)*vb; compare on same convention.
        fluid=np.sqrt(weights)*F
        out.append(np.r_[A.real,A.imag,B.real,B.imag,d,ds,vb,fluid.ravel(),k*Phi,k*Psi])
        norms.append(float(math.sqrt(abs(A)**2+abs(B)**2+d*d+R*vb*vb/3+np.sum(fluid**2))))
        if not reduced:
            E=a0**3*(abs(x)**2+abs(v)**2)/2
            assert 1-1e-7<=E<=1+24/m**2+1e-7
            cons.append(abs(a0**3*np.imag(np.conj(x)*v)-1))
    assert not cons or max(cons)<1e-7
    return a,np.array(out).T,max(norms),max(cons,default=0.)

def main():
    signal.signal(signal.SIGALRM,guard);signal.alarm(115)
    sym=symbolic();rows=[];tails=[]
    for kap in [1.,4.]:
        for profile in ['free','release','reentrant']:
            for m in [16,32,64,128]:
                a,z,nn,q=solve(m,kap,32,profile)
                a2,z2,_,_=solve(m,kap,32,profile,'RK45',2e-11)
                ad,zd,_,_=solve(m,kap,32,profile,reduced=True)
                diff=float(np.max(abs(z-z2)));assert diff<3e-6,(m,kap,profile,diff)
                err=float(max(np.linalg.norm(z-zd,axis=0)))
                rows.append(dict(kappa=kap,m=m,profile=profile,max_state_error=err,max_density_error=float(np.max(abs(z[4:6]-zd[4:6]))),max_metric_scaled_error=float(np.max(abs(z[-2:]-zd[-2:]))),max_norm=nn,solver_difference=diff,background_error=float(max(abs(a/ad-1))),charge_error=q))
            assert rows[-1]['max_state_error']<rows[-4]['max_state_error']
    # Independent cutoff comparison, full feedback; low variables and moments 0..2.
    for profile in ['free','reentrant']:
        for m in [32,128]:
            kap=4.; a,z,_,_=solve(m,kap,48,profile)
            def low(z,N):return np.r_[z[:7],z[7:7+3*(N+1)].reshape(3,N+1,-1)[:,:3].reshape(9,-1),z[-2:]]
            ref=low(z,48)
            for N in [4,8,16]:
                _,small,_,_=solve(m,kap,N,profile)
                err=float(max(np.linalg.norm(ref-low(small,N),axis=0)))
                D=2*N-2;x=math.sqrt(m*kap)*T
                tails.append(dict(m=m,kappa=kap,profile=profile,N=N,low_error=err,factorial_without_feedback_prefactor=math.exp(D*math.log(x)-math.lgamma(D+1))))
            assert tails[-1]['low_error']<tails[-3]['low_error']+1e-8
    print(json.dumps(dict(status='COMPUTATION_PASS_SCOPED',numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,symbolic=sym,integrations=calls,rhs_evaluations=nfev,grid_samples=len(grid),cases=rows,cutoff_cases=tails,scope='linear canonical quadratic scalar with Thomson Legendre brightness and massless neutrinos; prescribed cosmic opacity; no recombination or primordial observables'),indent=2));signal.alarm(0)
if __name__=='__main__':main()
