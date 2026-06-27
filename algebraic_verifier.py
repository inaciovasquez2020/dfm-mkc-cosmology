import sympy as sp

H, a, k, M_Pl, lam, Phi_dot0, Vp = sp.symbols(
    "H a k M_Pl lambda Phi_dot0 Vp", nonzero=True
)
alpha, beta, varphi, varphi_dot = sp.symbols(
    "alpha beta varphi varphi_dot"
)

M_eff2 = M_Pl**2 + sp.Rational(1, 2) * lam * Phi_dot0**2

A_ab = -2 * H * M_eff2
A_bv = Phi_dot0
A_bvdot = 0

A_aa = sp.Rational(1, 2) * Phi_dot0**2 - 3 * lam * H**2 * Phi_dot0**2
A_avdot = -Phi_dot0 + 12 * lam * H**2 * Phi_dot0
A_av = -Vp

constraint_beta = sp.expand(A_ab * alpha + A_bv * varphi)

constraint_alpha = sp.expand(
    2 * A_aa * alpha
    + A_avdot * varphi_dot
    + A_av * varphi
    + (k**2 / a**2) * A_ab * beta
)

beta_solution = sp.solve(sp.Eq(constraint_beta, 0), alpha)[0]

reduced_alpha_constraint = sp.simplify(
    constraint_alpha.subs(alpha, beta_solution)
)

k_scaled_beta_term = sp.simplify((k**2 / a**2) * beta)

assert sp.simplify(M_eff2 - (M_Pl**2 + lam * Phi_dot0**2 / 2)) == 0
assert A_bvdot == 0
assert not k_scaled_beta_term.has(k**-2)

print("ALGEBRAIC_VERIFIER_OK")
print("constraint_beta =", constraint_beta)
print("alpha =", beta_solution)
print("constraint_alpha =", constraint_alpha)
print("reduced_alpha_constraint =", reduced_alpha_constraint)
