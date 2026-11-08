# BBN numerical receipts — 2026-11-08

**STATUS:** User-reported macOS computation results, independently cross-checked for internal numerical consistency in this GitHub preservation step. **Not a physics proof. Not a Mac rerun.**

## Scope

These receipts support a **separate early-universe scalar expansion study** and are included as supporting research evidence in draft PR #334. They are **not** a derivation of the diamond–graphite EFT coupling; canonical DFM–MKC V1 remains unchanged. No direct visible-matter scalar coupling is introduced by these files.

## Cases and provenance

| Experiment | Code/model | Network | Mac outcome | Numerical evidence |
|---|---|---:|---|---|
| `alterbbn_t6_proxy_stdout.txt` | AlterBBN, temporary bounds patch, extra density ∝ T^6 | 26 nuclides / 100 reactions | 7/7 completed | SHA-256 of `scan.c` and `results.csv` as reported |
| `primat_large_baseline_stdout.txt` | PRIMAT 0.3.3, η=6.10×10⁻¹⁰, τₙ=880.3 s | 59 nuclides / 429 reactions | two tolerance runs | CNO relative difference 4.294772652e-6 |
| `primat_stiff_a_minus_6_stdout.txt` | PRIMAT 0.3.3, scalar energy ∝ a(T)⁻⁶ | 59 nuclides / 429 reactions | 5/5 completed | baseline reproduced; r10=1 CNO difference 1.593391330e-8 |
| `primat_isotope_stdout.txt` | isotope composition of PRIMAT large network | 59 tracked nuclides | isotope audit complete | C12 share 71.805223%; C13 share 18.748786% |

Machine-readable reported values and source-hash strings are in `experiment_receipts.json`. Each `*_stdout.txt` is a **transcribed excerpt**, with machine-specific temporary path prefixes removed; none is presented as the original byte-for-byte Mac log.

## Main numerical comparisons

- Standard PRIMAT CNO/H: **7.818942835819604 × 10⁻¹⁶**; standard AlterBBN CNO_raw/H: **6.03243032298 × 10⁻¹⁶**. The ratio is **1.2961513713691886**, but the source reaction tables and unstable-isotope conventions differ.
- PRIMAT's standard a(T) history plus added `rho_phi ∝ a^-6` gives CNO/H **7.849345721840598 × 10⁻¹⁶** at r10=1 versus **7.818942835819604 × 10⁻¹⁶** at r10=0, about **+0.389%**.
- At r10=3, CNO/H is **7.910101108050993 × 10⁻¹⁶**, approximately **+1.166%**, with helium `Yp=0.24813640473355256` and D/H `2.4678575545559443e-05`. The same model does not establish improvement over standard BBN.
- Carbon-12 accounts for ~71.8% and carbon-13 ~18.75% of the baseline CNO number abundance. The stable-isotope response is small and monotonic for the tested cases.

## Physics limitations and open boundary

1. The AlterBBN density law `T^6` is an approximation, not the properly entropy-adjusted scalar evolution; `CNO_raw_H` includes unstable nuclei.
2. The PRIMAT `a^-6` screen uses the **standard** temperature–scale-factor relation and standard neutrino-decoupling history; an independent scalar contribution is added to the Friedmann rate. Full dynamical feedback and modified neutrino decoupling remain **OPEN**.
3. The PRIMAT r10 normalization uses ideal `g*=10.75` at 10 MeV; it is not automatically identical to AlterBBN's radiation normalization.
4. Both code versions and Mac source-file SHA-256 strings are **reported by the user**, not independently replayed from the Mac within this checkpoint. Actual Mac `scan.c`, `check.py`, `test.py`, `results.csv`, and original `results.json` files are **not included**. This is a result-preservation checkpoint, **not** a self-contained reproducibility archive.
5. Neither the BBN results nor the separate conditional diamond–graphite EFT establishes a carbon-specific gravitational interaction. `CARBON_GRAVITY := OPEN`.

## Checks performed on the transcriptions

For this preservation step, case counts (7/2/5), repeated PRIMAT baselines, CNO tolerance ratio, PRIMAT/AlterBBN ratio, monotonic CNO in each reported positive-parameter sweep, isotope C12 fractions and checksum-string formats were checked in memory; this validates **internal consistency only**. Original source files and local Mac Git status were **not inspected**.

**Repository policy:** These are additional files only, under `research/receipts/bbn_20261108/`; the canonical action and the `main` branch are not modified.
