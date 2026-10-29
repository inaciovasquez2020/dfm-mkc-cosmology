# DFM-MKC FLRW Reduction and Parameter Identifiability Audit — 2026-10-29

Status: `ANALYTIC_HOMOGENEOUS_REDUCTION_CHECKED; NUMERICAL_SOLVER_AND_DATA_HASH_GATES_OPEN`

## Pinned inputs

This note is derived against the action and field-equation JSON artifacts at commit `336b2e9049fc612d5dee81e27bee2160005f1db9`:

- Action artifact: `artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json`, Git blob SHA-1 `e4b28e93e1afe8108cbd96e857187754fdedccb3`.
- Field-equation artifact: `artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json`, Git blob SHA-1 `1c3f86071228a5bc19f3e3ba19c28ad571aea67e`.

These SHA-1 values identify Git blobs; they are not raw-byte SHA-256 receipts.

## Conventions and covariant equations

Use signature ((-+++)), (c=\hbar=1), and
[
L_D=-\frac{\alpha}{2}(\nabla\phi)^2-\frac{\beta}{2}\phi^2(\nabla\theta)^2-U(\phi),\quad
U=\rho_\star+\frac12m_\phi^2\phi^2+\frac14\lambda_\phi\phi^4.
]
Here (\alpha,\beta>0), (\lambda_\phi\ge0), and (\phi\ne0) for the phase-current quotient. The field equations are
[
\alpha\Box\phi-\beta\phi(\nabla\theta)^2-U'(\phi)=0,\qquad
\nabla_\mu(\beta\phi^2\nabla^\mu\theta)=0,
]
with (U'=m_\phi^2\phi+\lambda_\phi\phi^3). The stress tensor is the metric variation recorded in the pinned field-equation artifact.

## Homogeneous FLRW reduction

For (ds^2=-dt^2+a(t)^2\gamma_{ij}dx^idx^j), (H=\dot a/a), and homogeneous (\phi(t),\theta(t)),
[
\Box\phi=-(\ddot\phi+3H\dot\phi),\quad
(\nabla\theta)^2=-\dot\theta^2.
]
Therefore
[
\ddot\phi+3H\dot\phi-\frac{\beta}{\alpha}\phi\dot\theta^2+\frac{U'}{\alpha}=0.
]
The phase equation becomes
[
\frac{d}{dt}(a^3\beta\phi^2\dot\theta)=0,
\quad Q_\theta:=a^3\beta\phi^2\dot\theta=\mathrm{constant},
\quad \dot\theta=\frac{Q_\theta}{a^3\beta\phi^2}.
]
The homogeneous density and pressure are
[
\rho_D=\frac{\alpha}{2}\dot\phi^2+\frac{\beta}{2}\phi^2\dot\theta^2+U,
\quad
p_D=\frac{\alpha}{2}\dot\phi^2+\frac{\beta}{2}\phi^2\dot\theta^2-U.
]
For visible matter minimally coupled through (g_{\mu\nu}), with its equations of motion satisfied and no direct exchange terms,
[
H^2+\frac{k}{a^2}=\frac{8\pi G}{3}(\rho_{\rm vis}+\rho_D)+\frac{\Lambda}{3}.
]

## Continuity identity (symbolic hand-check)

Differentiate (\rho_D):
[
\dot\rho_D=\alpha\dot\phi\ddot\phi+
\beta\phi\dot\phi\dot\theta^2+
\beta\phi^2\dot\theta\ddot\theta+U'\dot\phi.
]
Differentiating (a^3\beta\phi^2\dot\theta=Q_\theta) gives
[
\beta\phi^2\dot\theta\ddot\theta
=-3H\beta\phi^2\dot\theta^2-2\beta\phi\dot\phi\dot\theta^2.
]
Multiplying the amplitude equation by (\alpha\dot\phi) (equivalently substituting it into the derivative above) cancels the remaining (U'\dot\phi) and amplitude/phase cross terms, yielding
[
\boxed{\dot\rho_D=-3H(\alpha\dot\phi^2+\beta\phi^2\dot\theta^2)
=-3H(\rho_D+p_D).}
]
Thus (\dot\rho_D+3H(\rho_D+p_D)=0). Visible-sector conservation then makes the time derivative of the Friedmann constraint consistent with the acceleration equation wherever the usual differentiability assumptions hold. This is an analytic identity, not a numerical constraint-preservation test.

## Normalization and identifiable combinations

Set the canonical amplitude (\psi=\sqrt{\alpha}\,\phi), which is allowed because (\alpha>0). The dark Lagrangian becomes
[
L_D=-\frac12(\nabla\psi)^2
-\frac{\kappa}{2}\psi^2(\nabla\theta)^2
-\rho_\star-\frac12\mu^2\psi^2-\frac14\lambda_{\rm eff}\psi^4,
]
where
[
\kappa=\frac{\beta}{\alpha},\qquad
\mu^2=\frac{m_\phi^2}{\alpha},\qquad
\lambda_{\rm eff}=\frac{\lambda_\phi}{\alpha^2}.
]
The background Einstein equation depends on the constant terms only through
[
\Lambda_{\rm eff}=\Lambda+8\pi G\rho_\star.
]
Accordingly, for background-only inference, adopt the explicit convention (\rho_\star=0) and fit (\Lambda_{\rm eff}) rather than treating (\Lambda) and (\rho_\star) as independent parameters. This is a convention fixing a degeneracy, not a measurement of either bare constant.

A minimal candidate background parameterization is therefore (G,\Lambda_{\rm eff},\kappa,\mu^2,\lambda_{\rm eff}), plus the phase charge (Q_\theta), initial conditions for (\psi,\dot\psi), visible-sector densities, curvature choice, and the sound-horizon/early-universe prescription required by BAO. This list is not yet an identifiable or frozen fit: the selected observables, priors, boundary conditions, and possible further degeneracies must be analyzed before assigning numerical values. The phase charge can be zero, but that is a physical model choice and must not be silently imposed.

## Validation boundary

- Analytic reduction and continuity identity: checked by the derivation above.
- Automated symbolic regression tests: not yet added/run.
- Numerical Einstein-constraint preservation and grid/convergence tests: not run.
- Independent DESI raw-byte SHA-256 verification: still open.
- KiDS-Legacy archive inspection and per-file pins: still open.
- No DFM-MKC predictions, residuals, likelihoods, or model comparison are claimed.

## Data acquisition record

Official KiDS-Legacy science-data page: https://kids.strw.leidenuniv.nl/sciencedata.php
Official weak-lensing data-product page: https://kids.strw.leidenuniv.nl/DR5/legacy_wl.php
The official science-data page advertises a 125 MB gzip tarball containing posterior chains, data vectors, covariance matrices, redshift distributions, and CosmoSIS configurations. A download attempt from the official archive endpoint was unsuccessful in this execution environment. No archive bytes, member list, dimensions, ordering, units, or SHA-256 hashes are asserted here.

DESI pinned files remain as listed in `docs/status/DESI_DR2_BAO_DATA_PIN_2026_10_29.md`. Network access for independent raw downloads was unavailable in this execution environment; prior SHA-256 values are therefore not promoted to independent-download receipts.

## Next gates

1. Add executable symbolic checks for the field equations, phase current, continuity identity, and Friedmann constraint.
2. Freeze a convention and analyze identifiable combinations for the actual likelihood and priors.
3. Download the official KiDS archive in a network-enabled environment; inventory and hash each relevant file before parsing the README-defined ordering and units.
4. Re-download both DESI files from the pinned source and independently compare raw-byte SHA-256 values.
5. Implement and test the action-derived solver only after these gates are documented as passed.
