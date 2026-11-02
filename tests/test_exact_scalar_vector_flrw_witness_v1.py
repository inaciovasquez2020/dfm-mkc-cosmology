"""Exact nonzero temporal-vector FLRW solution of the supplied action.

Mathematical witness, not a physically calibrated cosmology.  In units with
H=1 and M_Pl^2=1, choose flat FLRW a=e^t, N=1, phi=0, A_0=1,
m_A^2=3, xi_A=-1, Lambda_0=3/2, and no matter.  Other scalar-sector
couplings are set to zero except alpha_phi=1.  The homogeneous Maxwell
term vanishes identically because F_{mu nu}=0.

The test independently varies the unreduced-curvature homogeneous
action and its boundary-integrated form.  All four field residuals
must vanish identically after substitution.  It makes no stability,
sound-horizon, physical normalization, or observational claims.
"""

import json
from pathlib import Path

import sympy as sp


SOURCE_SPEC = (
    Path(__file__).resolve().parents[1]
    / "specs"
    / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
)


def test_nonzero_temporal_vector_desitter_solution_of_source_action():
    action = json.loads(SOURCE_SPEC.read_text())["action_functional"]["definition"]
    for required_term in (
        "M_Pl^2/2 R",
        "- Lambda_0",
        "- m_A^2/2 A_mu A^mu",
        "- xi_A/2 R_{mu nu} A^mu A^nu",
    ):
        assert required_term in action

    t = sp.Symbol("t", real=True)
    a, lapse, A0, phi = (
        sp.Function(s)(t) for s in ("a", "N", "A0", "phi")
    )
    M2, Lambda, mA2, xiA, xiPhi, alphaPhi, mPhi2, lamPhi, beta = (
        sp.symbols(
            "M2 Lambda mA2 xiA xiPhi alphaPhi mPhi2 lamPhi beta",
            real=True,
        )
    )
    adot = sp.diff(a, t)
    addot = sp.diff(a, t, 2)
    Ndot = sp.diff(lapse, t)

    # Flat FLRW: signature (-+++), A_mu dx^mu = A0(t) dt.
    scalar_R = 6 / lapse**2 * (
        addot / a + adot**2 / a**2 - adot * Ndot / (a * lapse)
    )
    ricci_00 = -3 * (addot / a - adot * Ndot / (a * lapse))
    F = M2 - xiPhi * phi**2
    vector_mass_sq = mA2 + beta * phi**2
    potential = (
        Lambda + mPhi2 * phi**2 / 2 + lamPhi * phi**4 / 4
    )
    # These terms are the specified scalar-vector action after imposing
    # homogeneous isotropy.  F_{mu nu}=0 and matter is absent.
    raw = sp.expand(
        lapse * a**3 * (
            F * scalar_R / 2
            + alphaPhi * sp.diff(phi, t)**2 / (2 * lapse**2)
            - potential
            + vector_mass_sq * A0**2 / (2 * lapse**2)
            - xiA * ricci_00 * A0**2 / (2 * lapse**4)
        )
    )

    coefficient_addot = sp.diff(raw, addot)
    first_order = sp.expand(
        raw - sp.diff(coefficient_addot * adot, t)
    )
    assert sp.simplify(sp.diff(first_order, addot)) == 0

    def euler_raw(q):
        return (
            sp.diff(raw, q)
            - sp.diff(sp.diff(raw, sp.diff(q, t)), t)
            + sp.diff(
                sp.diff(raw, sp.diff(q, t, 2)),
                t, 2,
            )
        )

    def euler_first_order(q):
        return (
            sp.diff(first_order, q)
            - sp.diff(sp.diff(first_order, sp.diff(q, t)), t)
        )

    witness = {
        a: sp.exp(t),
        sp.diff(a, t): sp.exp(t),
        sp.diff(a, t, 2): sp.exp(t),
        lapse: sp.Integer(1),
        sp.diff(lapse, t): sp.Integer(0),
        sp.diff(lapse, t, 2): sp.Integer(0),
        A0: sp.Integer(1),
        sp.diff(A0, t): sp.Integer(0),
        sp.diff(A0, t, 2): sp.Integer(0),
        phi: sp.Integer(0),
        sp.diff(phi, t): sp.Integer(0),
        sp.diff(phi, t, 2): sp.Integer(0),
        M2: sp.Integer(1),
        Lambda: sp.Rational(3, 2),
        mA2: sp.Integer(3),
        xiA: sp.Integer(-1),
        xiPhi: sp.Integer(0),
        alphaPhi: sp.Integer(1),
        mPhi2: sp.Integer(0),
        lamPhi: sp.Integer(0),
        beta: sp.Integer(0),
    }
    assert witness[A0] != 0 and witness[xiA] != 0
    assert witness[mA2] > 0 and witness[M2] > 0

    for field in (lapse, a, A0, phi):
        raw_eq = euler_raw(field)
        integrated_eq = euler_first_order(field)
        # Full off-shell identity, not just equality at the selected solution.
        assert sp.simplify(raw_eq - integrated_eq) == 0
        assert sp.simplify(raw_eq.xreplace(witness)) == 0

    # Exceptional vector branch: m_A^2 + 3*xi_A*H^2 = 0.
    assert witness[mA2] + 3 * witness[xiA] == 0

    # Mutation test: the fixed cosmological constant is not arbitrary.
    altered = dict(witness, **{})  # preserve exact witness dictionary
    altered[Lambda] = sp.Integer(2)
    assert sp.simplify(euler_raw(lapse).xreplace(altered)) != 0

    # Distinct genuinely coupled solution on the same exceptional A0 branch.
    # Here phi, A0, beta_phi_A, xi_A are all nonzero, and the scalar
    # potential balances the scalar-vector mass contribution.
    coupled = dict(witness)
    coupled.update({
        phi: sp.Integer(1),
        Lambda: sp.Integer(1),
        mA2: sp.Integer(2),
        mPhi2: sp.Integer(1),
        beta: sp.Integer(1),
    })
    assert all(coupled[x] != 0 for x in (phi, A0, beta, xiA))
    assert coupled[mA2] + coupled[beta] * coupled[phi]**2 + 3 * coupled[xiA] == 0
    for field in (lapse, a, A0, phi):
        assert sp.simplify(euler_raw(field).xreplace(coupled)) == 0
        assert sp.simplify(euler_first_order(field).xreplace(coupled)) == 0
    broken_coupling = dict(coupled)
    broken_coupling[beta] = sp.Integer(2)
    assert sp.simplify(euler_raw(A0).xreplace(broken_coupling)) != 0
