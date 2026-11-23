# Radion stabilization with winding and a periodic massive Casimir term

This checkpoint extends the single-power no-go in #341. The existence results apply to the stated Einstein-frame zero-mode potential. The fluctuation results below specify the approximation used for each sector. Lean and independent review have not been run.

## Two inverse powers

For V(b) = Λ/b + A/b³ + C/bᵖ + D/bᑫ with b>0, A>0 and 3<p<q, eliminate Λ at stationarity:
```text
L(b) = -3A/b² - pC/b^(p-1) - qD/b^(q-1)
E(b) = -2A/b³ - (p-1)C/b^p - (q-1)D/b^q
L'(b) = E'(b) = b V''(b) at Λ = L(b)
b E'(b) = -2(p-3)A/b³ - p E(b) + (q-p)(q-1)D/b^q
```
Positive energy and curvature require D>0. Write E=(p-1)b⁻ᵖ(-C-H), with H=[2Ab^(p-3)+(q-1)Db^(p-q)]/(p-1). Differentiation gives the unique minimum at b₀=[(q-p)(q-1)D/(2A(p-3))]^(1/(q-3)). Its value is 2A(q-3)b₀^(p-3)/[(p-1)(q-p)]. A de Sitter minimum for some Λ exists exactly when -C exceeds this value. At equality E=E'=0 at the unique nonnegative-energy stationary radius.

Above threshold, E>0 between two roots b₋ and b₊. The sign of E' is the sign of G=6Ab^(q-3)+p(p-1)Cb^(q-p)+q(q-1)D. Since C<0, G' has one positive zero, with sign changing from negative to positive. Also G(b₋)>0>G(b₊). Thus G has exactly one simple zero bₘ in the positive-energy interval. Since L'=E', a unique positive-energy minimum with positive curvature exists exactly for L(b₋)<Λ<L(bₘ). The lower endpoint is a positive-curvature Minkowski minimum. The upper endpoint has positive energy and V'''=E''(bₘ)/bₘ<0, so it is a stationary inflection.

## Periodic massive spectrum

Use V=Λ/b+A/b³+b⁻⁶[-B+M f(μb)], with A,B,M,μ>0, μ=2πm for proper mass m, and
```text
f(x) = Σ_{n≥1} e^(-nx) [1+nx+(nx)^2/3]/n^5
R(x) = 5f(x)-xf'(x)
T(x) = M R(x)+2(A/μ³)x³
E(b) = b^(-6) [5B-T(μb)]
```
At stationarity bV''=E'. The derivative T'/x² is 6A/μ³ minus M times the sum of e^(-nx)[1/(nx)+1+nx/3]/n². Each summand is positive and strictly decreasing, and their sum goes from infinity to zero. Termwise differentiation is justified by uniform exponential convergence on compact subsets of x>0. Thus T has a unique minimum. When Mζ(5)>B, both endpoint values of T exceed 5B. A de Sitter minimum for some Λ exists exactly when min T<5B. At the first crossing, E=0 and E'>0. Immediately to its right both E and E' are positive. At equality E=E'=0.

When Mζ(5)≤B, set U=5B-T. Then U(0)≥0 and U'/x² is strictly decreasing. If U'>0, integration gives U(x)>U(0)+xU'(x)/3, so xU'-6U<0. If U'≤0 the same curvature expression is negative wherever U>0. Hence this coefficient range cannot give a positive-energy minimum.

For one winding scalar and the 5D graviton, the leading flat-circle massless determinant gives B=6κζ(5). For N equal-mass neutral periodic Dirac fields, M=4Nκ. Here κ is the positive real-scalar Casimir normalization in the b⁻⁶ potential. One Dirac field is insufficient. For two fields and A/(κμ³)=1/100, R(3)<47/19 because its nth numerator polynomial is at most 47n³ and e⁻³<1/20. Therefore T(3)/κ<8(47/19)+27/50<30<5B/κ. Two fields are sufficient, and zero fields fall under the single-power no-go. This count is specific to this field family and the leading flat-circle determinants.

## Quadratic sectors and scale separation

With reference radius b*, use ds₅²=(b*/b)ds₄²+b²(dy+K)² and winding scalar θ=wy+s, with y of period 2π. The Einstein and scalar kinetic terms reduce to -ZF²/4-Y(∂s-wK)²/2, with Z=M₄²b³/(2b*) and Y=2πb*f₅³. The winding potential is Vw=πf₅³w²b*²/b³. Both kinetic coefficients are positive and the Stückelberg vector mass is mK²=Yw²/Z=4Vw/M₄². At a constant radion and zero vector background the radion and vector decouple at quadratic order. This uses tree-level kinetic terms.

Set b*=b₀ at the minimum and write V=b₀⁻⁴v(b/b₀), with a the coefficient of y⁻³ in v. Holding v fixed, H², radion mass squared and vector mass squared divided by b₀⁻² are respectively v(1)/(6π), v''(1)/(3π), and 2a/π, each divided by (M₅b₀)³. This is a family obtained by scaling the proper mass and scalar kinetic scale as b₀⁻¹ and bulk energy density as b₀⁻⁵.

For free Dirac perturbations on the product background, mₙ²=m²+n²/b₀². In the spatially flat de Sitter patch, multiplication of the spinor by the scale factor to the power 3/2 removes the Hubble term. The resulting mode Hamiltonian is Hermitian, so the rescaled mode norm is constant. Vanishing background spinors imply decoupling from bosonic perturbations at quadratic order.

## Flat-product loop threshold and the remaining bosonic problem

At external KK momentum n, the flat-product two-fermion threshold is [m_floor(n/2)+m_ceil(n/2)]². Strict convexity of u ↦ sqrt(m²+u²/b₀²) places the minimum at the two nearest integers to n/2. The Euclidean triangle inequality gives s_pair(n)-n²/b₀²≥4m², with equality for even n. This is a kinematic result at the bare flat-product shell. The real self-energy and the de Sitter response remain open.

The product dS₄×S¹ is conformally flat. Its five-dimensional Schouten tensor equals H²g/2 along dS₄ and -H²g/2 along the circle, which reproduces all background Riemann components via the metric–Schouten product. A finite Weyl-squared term therefore vanishes together with its first variation on the background but adds a term proportional to (δWeyl)² at quadratic order. The radion potential leaves that coefficient undetermined. The open obligation is the renormalized retarded metric response projected onto the constrained nonzero bosonic KK sectors, with finite local terms specified and controlled within the EFT regime.

## Reproduction and references

Run `python3 -I -B research/5d/radion_spectral_checkpoint.py` for exact arithmetic checks of the two-power example, the massive threshold witness and the flat-product pair threshold. The analytic arguments above give the general statements.

- Biswas, Juberi and Kamal, [Quality time in extra dimensions](https://arxiv.org/abs/2611.12765), periodic circle kernel and winding Stückelberg reduction.
- [Casimir dark energy, stabilization of the extra dimensions and Gauss–Bonnet term](https://doi.org/10.1140/epjc/s10052-014-3237-0), graviton and fermion determinant weights.
- Lüst and Masias, [A LooKK at the Higuchi Bound](https://arxiv.org/abs/2609.16103), related Casimir-supported circle analysis.
- Anderson, Molina-París and Mottola, [Linear response, validity of semiclassical gravity, and the stability of flat space](https://doi.org/10.1103/PhysRevD.67.024026), stress-tensor linear response.
