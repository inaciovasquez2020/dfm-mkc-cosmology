"""Exact rational jet audit of nonzero Fourier gauge-orbit completeness.
The symbolic identity holds for k=i*n by rational continuation; tests do not
establish the physical spectrum or on-shell Hessian.
"""
from fractions import Fraction as F
from itertools import product
import random

def main():
    if not __debug__:
        raise SystemExit("INCOMPLETE: assertions disabled")
    rng = random.Random(20261120)
    def val():
        return F(rng.randint(-11, 11), rng.randint(1, 7))
    pairs = [(i,j) for i in range(4) for j in range(i,4)]
    cases = 0
    for b,k,q in product(map(F, [1,2,3]), map(F, [-3,-2,-1,1,2,3]), map(F, [-2,0,3])):
        b /= 2
        k /= 2
        for _ in range(16):
            r,theta,u = val(),val(),val()
            B,dr,du,v = ([val() for i in range(4)] for j in range(4))
            h,S,T,U,V = ({ij:val() for ij in pairs} for j in range(5))
            # S = sym nabla B; T = Hess r; U = Hess xi^w;
            # V = sym nabla xi_mu. Independent pointwise jet data.
            def inv(r,theta,h,S,T):
                return (theta-q*r/k, {ij:h[ij]-b*b*S[ij]/k+2*b*b*T[ij]/k**2 for ij in pairs})
            z,H = inv(r,theta,h,S,T)
            rp, tp = r+k*u,theta+q*u
            Bp = [B[i]+du[i]+k*v[i]/b**2 for i in range(4)]
            hp = {ij:h[ij]+V[ij] for ij in pairs}
            Sp = {ij:S[ij]+2*U[ij]+k*V[ij]/b**2 for ij in pairs}
            Tp = {ij:T[ij]+k*U[ij] for ij in pairs}
            drp = [dr[i]+k*du[i] for i in range(4)]
            assert inv(rp,tp,hp,Sp,Tp)==(z,H)
            # Unique normalizing parameters and their derivative jets.
            def normalize(r,theta,B,dr,h,S,T):
                a=-r/k
                da=[-x/k for x in dr]
                c=[-b*b*(B[i]+da[i])/k for i in range(4)]
                dc={ij:-b*b*(S[ij]-2*T[ij]/k)/k for ij in pairs}
                assert r+k*a==0
                assert all(B[i]+da[i]+k*c[i]/b**2==0 for i in range(4))
                return theta+q*a,{ij:h[ij]+dc[ij] for ij in pairs}
            assert normalize(r,theta,B,dr,h,S,T)==(z,H)
            assert normalize(rp,tp,Bp,drp,hp,Sp,Tp)==(z,H)
            # Recover the unique transformation between equivalent inputs.
            recovered_u=(rp-r)/k
            recovered_du=[(drp[i]-dr[i])/k for i in range(4)]
            recovered_v=[b*b*(Bp[i]-B[i]-recovered_du[i])/k for i in range(4)]
            assert recovered_u==u and recovered_du==du and recovered_v==v
            cases+=1
    assert cases==864
    print(f"GAUGE_ORBIT_JET_CASES := {cases}")
    print("NONZERO_GAUGE_ORBIT_EXACT_AUDIT := PASS")
    print("PHYSICAL_SPECTRUM := OPEN")
    print("LEAN := NOT_RUN")

if __name__=="__main__":
    main()
