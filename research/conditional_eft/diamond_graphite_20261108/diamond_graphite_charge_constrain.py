#!/usr/bin/env python3
"""Conditional carbon allotrope scalar-charge calculation; stdlib only.

Based on specified low-energy EFT and literature input intervals.
No molecular electronic-structure solve; no full EFT global likelihood.
"""
from fractions import Fraction as F
from decimal import Decimal, getcontext
from itertools import product
from pathlib import Path
from math import isfinite
import hashlib
import json

getcontext().prec = 55
D = Decimal
checks = 0

# Identity for q_D=(m'+eps_D')/(m+eps_D), q_G analogous.
# EXACT symbolic rational verification over an adversarial grid.
for m, epsD, epsG, epsDp, epsGp, mp in product(
    (100, 1000, 10000), (-2,-1,0,1,2), (-2,-1,0,1,2),
    (-3,-1,0,1,3), (-3,-1,0,1,3), (-3,-1,0,1,3)
):
    lhs = F(mp+epsDp, m+epsD) - F(mp+epsGp, m+epsG)
    rhs = F(m*(epsDp-epsGp)-mp*(epsD-epsG)+epsDp*epsG-epsGp*epsD,
            (m+epsD)*(m+epsG))
    assert lhs == rhs, (m, epsD, epsG, epsDp, epsGp, mp)
    checks += 1

# Special case: universal rescaling of every energy => zero charge difference.
for m, ed, eg, d in product((10,100,1000), (-2,-1,0,1,2),
                             (-2,-1,0,1,2),(-3,-1,0,1,3)):
    qd=F(m*d+ed*d,m+ed)
    qg=F(m*d+eg*d,m+eg)
    assert qd==d and qg==d and qd-qg==0
    checks +=1

rational_checks = checks  # All exact Fraction equality assertions above.

# Ranges from Popov et al. 2019 zero-T paper (not a statistical confidence interval)
c = D('299792458')
M_C_per_mol = D('0.012') # kg/mol for isotopically pure carbon-12
rest_kJ_per_mol = M_C_per_mol*c*c/D('1000')
E0 = [D('1.39'),D('1.55')]  # diamond minus graphite, kJ/mol
ZPE= [D('0.77'),D('1.15')] # diamond minus graphite, kJ/mol
A_m=[(E0[0]+ZPE[0]/2)/rest_kJ_per_mol,
     (E0[1]+ZPE[1]/2)/rest_kJ_per_mol]
A_a=[2*E0[0]/rest_kJ_per_mol,2*E0[1]/rest_kJ_per_mol]
assert D(0)<A_m[0]<A_m[1]<A_a[1]
checks +=1

# MICROSCOPE Ti-Pt conservative 2x combined one-sigma envelope (NOT a likelihood).
eta_envelope=(D('1.5')+D('2')*(D('2.3')**2+D('1.5')**2).sqrt())*D('1e-15')
QeEarth=D('1.90e-3')   # Cyncynates & Simon 2025 toy Earth composition
QePtMinusTi=D('-1.94e-3') # 2025 published Pt-Ti alloys
# Scalar potential V=-GmMm/r (1+2 qA qB e^-mu*r), hence eta=2 qE Deltaq for long range.
# If ALL independent low-energy couplings but d_alpha vanish, then
# q_E≈QeEarth*d_alpha, DeltaqTiPt≈QePtMinusTi*d_alpha.
d_alpha_bound=(eta_envelope/(2*QeEarth*abs(QePtMinusTi))).sqrt()
# Remaining carbon atomic d_C has tiny electromagnetic sensitivity QeC ~ 1e-3;
# using A_alpha without subtraction is an upper bound within this approximate
# atomic-charge model if 0<d_C/d_alpha<<2.
structural_dq_bound=A_a[1]*d_alpha_bound
eta_dg_bound=2*QeEarth*A_a[1]*(d_alpha_bound**2)
# These are three derived Decimal quantities, not three assertions.

# Construct cancellation direction, proving Ti-Pt alone cannot constrain a full EFT.
QmePtMinusTi=D('-3.13e-5')
d_alpha=D('1')
d_me=-QePtMinusTi/QmePtMinusTi*d_alpha
microscope_channel=QePtMinusTi*d_alpha+QmePtMinusTi*d_me
assert abs(microscope_channel) < D('1e-50')
# d_C is not independent and here is a small atomic response (illustrative,
# no full hadronic matching); for establishing a nonparallel structural axis
# its precise value is not required.
structural_linear=A_m[0]*d_me+A_a[0]*d_alpha
assert structural_linear!=0
checks+=2

receipt={
    'status':'COMPUTATION_PASS_CONDITIONAL',
    'exact_arithmetic_checks':rational_checks,
    'additional_decimal_assertions':checks-rational_checks,
    'derived_bound_calculations':3,
    'energy_inputs_source':'Popov et al 2019, DOI:10.1039/C8CP07592A',
    'earth_dilaton_charges_source':'Cyncynates & Simon 2025, DOI:10.1103/8mc9-6cmr, Table I',
    'experiment_source':'MICROSCOPE final 2022, DOI:10.1103/PhysRevLett.129.121102',
    'rest_energy_kJ_per_mol':str(rest_kJ_per_mol),
    'zero_T_total_kJ_per_mol':[str(x) for x in E0],
    'zero_T_zp_kJ_per_mol':[str(x) for x in ZPE],
    'coeff_d_me_minus_d_C':[str(x) for x in A_m],
    'coeff_d_alpha':[str(x) for x in A_a],
    'microscope_conservative_two_sigma_envelope':str(eta_envelope),
    'Qe_earth_assumption':str(QeEarth),
    'Qe_Pt_minus_Ti_assumption':str(QePtMinusTi),
    'max_abs_d_alpha_one_operator_long_range':str(d_alpha_bound),
    'max_abs_Deltaq_one_operator_long_range_approx':str(structural_dq_bound),
    'max_abs_eta_diamond_graphite_one_operator_long_range_approx':str(eta_dg_bound),
    'cancellation_d_me_div_d_alpha':str(d_me),
    'cancellation_microscope_channel':str(microscope_channel),
    'cancellation_structural_direction_toy':str(structural_linear),
    'limitations':[
       'Only canonical normalisation and low-energy linear EFT, not DFM-MKC V1.',
       'Condensed-matter Born-Oppenheimer/harmonic scaling; neglects relativistic, finite-T, and higher EFT operator effects.',
       'Literature energy intervals are not rigorous error bars; electronic energy sign has disputed calculations.',
       'Earth model and MICROSCOPE charge table are approximations; envelope is not statistical 95% posterior.',
       'One-operator numerical bound assumes ultra-long scalar range, no screening, no tuning, no independent couplings.',
       'No experimental bound on Delta q for unrestricted five-parameter EFT.',
       'No DFT/phonon matrix elements calculated from first principles.'
    ],
}
out=Path(__file__).with_name('diamond_graphite_charge_constraint_receipt.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print('EXACT_RATIONAL_CHECKS :=',rational_checks)
print('DECIMAL_ASSERTIONS :=',checks-rational_checks)
print('DERIVED_BOUND_CALCULATIONS :=',3)
print('A_M_INTERVAL :=',*[str(x) for x in A_m])
print('A_ALPHA_INTERVAL :=',*[str(x) for x in A_a])
print('MICROSCOPE_ENVELOPE :=',eta_envelope)
print('D_ALPHA_BOUND_ONE_OPERATOR :=',d_alpha_bound)
print('DELTA_Q_BOUND_ONE_OPERATOR :=',structural_dq_bound)
print('ETA_DG_BOUND_ONE_OPERATOR :=',eta_dg_bound)
print('CANCELLATION_DIRECTION :=',d_me)
print('CANCELLATION_STRUCTURAL_NONZERO :=',structural_linear)
for p in (Path(__file__),out):print('SHA256 :=',hashlib.sha256(p.read_bytes()).hexdigest(),p)
