# SSPFI Protocol: Deterministic Symmetry Restoration Engine

[![Paper: SSPFI Formalization](https://img.shields.io/badge/Paper-SSPFI_Formalization-blue.svg)](https://www.researchgate.net/publication/403885690_The_Symmetric_Seed_Purity_Fixed-Point_Identity_SSPFI_A_Rigorous_Measure-Theoretic_Formalization_with_Examples_Regularization_and_Extensions)
[![Paper: Gauge Theory Application](https://img.shields.io/badge/Paper-Symmetry_Restoration-red.svg)](https://www.researchgate.net/publication/403898896_Deterministic_Symmetry_Restoration_in_Non-Abelian_Gauge_Theories_A_Measure-Theoretic_Approach_via_the_SSPFI_Protocol)

This repository contains the official computational engine and numerical verification suite for the **Symmetric Seed Purity Fixed-Point Identity (SSPFI)** framework. 

The SSPFI protocol provides a deterministic, measure-theoretic alternative to traditional stochastic cooling or diffusive gradient flows in lattice gauge theory. By treating symmetry restoration as a contraction mapping on standard Borel spaces, this engine achieves exact mathematical vacuum recovery ($\langle P \rangle \rightarrow 1 - \mathcal{O}(10^{-15})$) with absolute stability.

## 📚 Theoretical Foundation

This engine implements the mathematical frameworks detailed in the following manuscripts:

1. **[The Symmetric Seed Purity Fixed-Point Identity (SSPFI)](https://www.researchgate.net/publication/403885690)**: 
   *Establishes the rigorous measure-theoretic formalization, recursive probability space construction, and weak convergence theorems.*

2. **[Deterministic Symmetry Restoration in Non-Abelian Gauge Theories](https://www.researchgate.net/publication/403898896)**: 
   *Demonstrates the application of SSPFI to $SU(2)$ gauge fields, achieving rapid vacuum recovery from maximum entropy noise.*

## 🚀 Key Features

* **Deterministic Symmetry Restoration**: Replaces computationally expensive stochastic processes with a high-efficiency fixed-point iteration.
* **Robust SVD-based Projection**: Implements "Manifold Locking" via Singular Value Decomposition (SVD), effectively bypassing branch-cut singularities inherent in traditional polar decomposition.
* **Synthetic Seed Construction**: Uses Dirichlet-weighted convex combinations from the fixed-point pool to facilitate global symmetry transitions without topological bottlenecks.
* **In-place Measure Updates**: Employs the "Reflection Involution" strategy to preserve spatial coherence during the restoration cycle.

## 🛠 Methodology: The SSPFI Cycle

The engine executes a recursive **Harvest-and-Update** cycle:
1.  **Harvesting**: Identifies group elements within a defined tolerance ($\tau$) of the identity manifold.
2.  **Synthesis**: Generates a synthetic seed ($S$) from the harvested fixed-point pool.
3.  **Update**: Performs the deterministic update: $\mu_{n+1} = \alpha \mu_n + (1-\alpha) S$.
4.  **Projection**: Re-projects all updated elements strictly back onto the $SU(2)$ manifold.



## 💻 Installation & Usage

### Requirements
* Python 3.8+
* NumPy

```bash
pip install numpy