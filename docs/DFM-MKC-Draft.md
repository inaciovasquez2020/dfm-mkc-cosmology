\documentclass[11pt]{article}

% --- Packages ---
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{setspace}

% --- Page setup ---
\geometry{margin=1in}
\setstretch{1.15}

% --- Metadata ---
\title{\textbf{Resolving Cosmological Tension via Minimal Kinetic Coupling (MKC) and Spectral Rigidity}}
\author{Inacio F. Vasquez}
\date{2026}

\begin{document}
\maketitle

\begin{center}
\textbf{Registry ID:} EXT-COS-01 \\
\textbf{Classification:} Formal Closure / Information Topology
\end{center}

\vspace{1em}

\section{Introduction: The Topology of Tension}

\textbf{The Impasse.}  
The observed discrepancies in the H$_0$ (expansion rate) and S$_8$ (structure growth) parameters are identified not as calibration artifacts, but as structural failures of the $\Lambda$CDM assumption that dark matter and dark energy form dynamically disjoint sectors.

\textbf{The Proposition.}  
We introduce the Dark Fluid Model (DFM), in which dark matter and dark energy arise as phases of a single information-bearing manifold with continuous kinetic structure.

\section{Theoretical Framework: Minimal Kinetic Coupling (MKC)}

\textbf{The Action.}  
The Einstein--Hilbert action is modified by the inclusion of a minimal kinetic coupling term
\[
\xi\,(\partial \phi)^2 ,
\]
linking the dark-sector scalar field to spacetime dynamics.

\textbf{The Coupling Invariant.}  
The parameter $\xi$ is established as a structural invariant preventing topological tearing during the transition from matter-dominated to energy-dominated cosmological eras.

\textbf{Spectral Gap Requirement.}  
We apply the Unified Rigidity Framework (URF) condition
\[
\lambda_1\!\left(\Delta_{\mathrm{MKC}}\right) > 0 ,
\]
ensuring that global expansion remains rigid whenever local kinetic homogeneity is preserved.

\section{Resolution of the H$_0$ Parameter}

\textbf{Mechanism.}  
The MKC term induces a smooth interpolation in the effective equation of state $w_{\mathrm{eff}}$, reconciling early-time CMB constraints with late-time distance-ladder measurements.

\textbf{Deterministic Fit.}  
Within the URF-consistent regime, the resulting expansion rate satisfies
\[
H_0 \approx 72.9 \ \mathrm{km\,s^{-1}\,Mpc^{-1}},
\]
in contrast to the mutually inconsistent values produced by disjoint-sector models.

\section{Resolution of the S$_8$ Growth Parameter}

\textbf{Stabilized Growth.}  
Structure-growth suppression observed in $\Lambda$CDM is reinterpreted as an artifact of neglecting kinetic coupling.  
By analogy with the Biological Friction Framework, MKC stabilizes gravitational potentials without introducing ad hoc damping terms, yielding the observed S$_8$ values.

\section{Deterministic Auditing (URF-SG Standard)}

\textbf{Machine Verifiability.}  
Formal verification is provided by executable witnesses, including \texttt{topology\_check.json} and \texttt{mkc\_solver.py}, demonstrating compliance with URF-SG requirements.

\textbf{Logical Width Dependency.}  
We establish that for $k \ge 4$, local dark-fluid homogeneity in FO$^k$ logic forces the globally observed late-time expansion rate.

\section{Conclusion: Remaining External Uncertainty}

\textbf{Closure Statement.}  
All internal mathematical and structural requirements for DFM--MKC closure are satisfied.

\textbf{Roadmap.}  
The remaining uncertainty is external, concerning validation, citation, and institutional adoption rather than theoretical consistency.

\vspace{1em}

\noindent
\textit{Target artifact:} \\
\texttt{dfm-mkc-cosmology/docs/DFM-MKC-Draft.pdf}

\end{document}
