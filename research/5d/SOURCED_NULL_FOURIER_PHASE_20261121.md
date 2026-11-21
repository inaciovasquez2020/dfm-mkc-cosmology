# Complex Fourier matching of the 5D EMD sourced null momentum constraint

**Status:** exact symbolic check PASS for the *necessary linearized null momentum equation* in the specified Fourier/Codazzi conventions. NOT a complete coupled ADM second variation, Hamiltonian/shift elimination, physical scalar kinetic matrix, or full stability proof. No novelty/Lean/independent review claimed.

## Conventions

Background: ds²=-dt²+a²d x₃²+b²dy², with a=t^(3/2), b=b0 t^(3/4), f=t^(-7), F_ty=(sqrt(51)/4)b0 t^(13/4), and Q=a³ f F_ty/b=sqrt(51)/4. Work at k,n nonzero and t,b0 positive.

Choose complex Fourier coefficients proportional to exp(i(kx+ny)), and delta A_x=i k v, delta A_y=0. Hence delta F_xy=k n v. The real-coefficient geometric null expression C_null(g) in GEOMETRIC_NULL_MOMENTUM_20261121.md has factored out the i from the spatial divergence. The ADM extrinsic curvature is K_ij=(dot gamma_ij-D_i N_j-D_j N_i)/(2N). The chosen Codazzi sign is D_j(K^j_i-delta^j_i K)=T_(normal,i).

The Maxwell source in orthonormal x direction is T_(normal,xhat) = f F_ty delta F_xy/(a b²) = Q kap nu v/a³, where kap=k/a and nu=n/b. The projected geometric divergence therefore matches the source as

    i C_null(g) = kap T_(normal,xhat) = Q kap² nu v/a³.

Taking C_null(g)=C_alpha alpha+R, with

    C_alpha = [15 kap²/4 + 9 nu²/2]/t > 0,

the **necessary** lapse value determined by this momentum equation is

    alpha = [ -i Q kap² nu v/a³ - R ]/C_alpha.

Complex conjugation at the opposite Fourier level maps this relation to the paired real mode under the usual reality convention. For a general complex scalar amplitude the real and imaginary parts must not be equated before the Fourier factors are accounted for.

## Validation and remaining obligations

Run `python3 -B research/5d/sourced_null_fourier_phase_audit.py` with installed SymPy. The exact assertions cover EMD flux normalization, perturbed F_xy, the normal momentum source, the Fourier i factor, the lapse algebra, and conjugate momentum-source consistency.

The result is **only necessary**, and depends on the geometric constraint expression and gauge conventions already stated in the earlier research notes. The full coupled ADM scalar Hessian must be independently derived and tested against linearized Einstein/Maxwell/dilaton equations. In particular, the Hamiltonian constraint may impose additional conditions; a positive coefficient C_alpha does not imply an unconstrained lapse degree of freedom.

**OPEN:** Hamiltonian and complementary shift equations; their mutual compatibility and constraint rank; the physical kinetic Schur complement after full gauge fixing; full gradient/mass spectrum; nonzero-KK scalar and complete five-dimensional stability. Stop on any convention mismatch, singular gauge, or omitted source. No merge/promotion justified by this certificate alone.
