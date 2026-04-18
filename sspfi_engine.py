#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SSPFI Protocol Engine for SU(2) Lattice Gauge Theory
====================================================
This module provides a deterministic measure-theoretic approach for symmetry 
restoration in Non-Abelian Gauge Theories using the Symmetric Seed Purity 
Fixed-Point Identity (SSPFI).

Author: Cyris C.
Date: April 2026
"""

import numpy as np
import csv
import statistics
import argparse
import time
from typing import Tuple, List

# =============================================================================
# SU(2) Algebra & Group Helpers
# =============================================================================

def random_su2() -> np.ndarray:
    """Generates a random SU(2) matrix uniformly distributed."""
    x = np.random.normal(size=4)
    x /= np.linalg.norm(x)
    a, b, c, d = x
    return np.array([
        [a + 1j*b, -c + 1j*d],
        [c + 1j*d,  a - 1j*b]
    ], dtype=np.complex128)

def proj_su2(M: np.ndarray) -> np.ndarray:
    """
    Robust SU(2) projection via SVD to avoid branch cut singularities.
    Projects an arbitrary 2x2 complex matrix back to the SU(2) manifold.
    """
    U, _, Vh = np.linalg.svd(M)
    res = U @ Vh
    # Ensure determinant is +1 (SU(2) requirement)
    if np.real(np.linalg.det(res)) < 0:
        U[:, 1] *= -1
        res = U @ Vh
    return res

def group_distance(U: np.ndarray) -> float:
    """Calculates the distance of an SU(2) matrix from the identity matrix."""
    return 0.5 * abs(2.0 - np.real(np.trace(U)))

# =============================================================================
# Lattice Observables
# =============================================================================

def avg_plaquette(lattice: np.ndarray) -> float:
    """
    Computes the average plaquette (gauge invariant observable) <P> 
    for the entire 2D lattice.
    """
    L = lattice.shape[0]
    total = 0.0
    count = 0
    for i in range(L):
        for j in range(L):
            Ux = lattice[i, j, 0]
            Uy_ip1_j = lattice[(i+1) % L, j, 1]
            Ux_i_jp1 = lattice[i, (j+1) % L, 0]
            Uy_ij = lattice[i, j, 1]
            
            # Plaquette calculation: U_p = U_x(x) * U_y(x+x^) * U_x^dagger(x+y^) * U_y^dagger(x)
            Up = Ux @ Uy_ip1_j @ Ux_i_jp1.conj().T @ Uy_ij.conj().T
            P = 0.5 * np.real(np.trace(Up))
            total += P
            count += 1
    return total / count

# =============================================================================
# SSPFI Protocol Core
# =============================================================================

def synthetic_seed(F_pool: List[np.ndarray], nmix: int = 5) -> np.ndarray:
    """
    Constructs a new synthetic seed by combining random matrices from the 
    fixed-point pool using Dirichlet weights, followed by an SU(2) projection.
    """
    if len(F_pool) == 0:
        raise ValueError("Empty fixed-point pool.")
        
    k = min(nmix, len(F_pool))
    idx = np.random.choice(len(F_pool), k, replace=False)
    weights = np.random.dirichlet(np.ones(k))
    
    M = np.zeros((2, 2), dtype=np.complex128)
    for w, ii in zip(weights, idx):
        M += w * F_pool[ii]
        
    return proj_su2(M)

def sspfi_step(lattice: np.ndarray, alpha: float, tol: float, nmix: int) -> Tuple[np.ndarray, bool]:
    """
    Executes a single iteration of the SSPFI protocol on the lattice.
    Identifies the fixed-point pool and deterministically updates the measure.
    """
    L = lattice.shape[0]
    F = []
    
    # 1. Harvest the Fixed-Point Pool (Manifold locking)
    for i in range(L):
        for j in range(L):
            for mu in range(2):
                U = lattice[i, j, mu]
                if group_distance(U) < tol:
                    F.append(U.copy())
                    
    if len(F) == 0:
        return lattice, False

    # 2. In-place measure update (Reflection Involution)
    for i in range(L):
        for j in range(L):
            for mu in range(2):
                if np.random.rand() > alpha:
                    S = synthetic_seed(F, nmix)
                    lattice[i, j, mu] = proj_su2(0.5 * lattice[i, j, mu] + 0.5 * S)
                    
    return lattice, True

# =============================================================================
# Experiment Driver
# =============================================================================

def run_experiment(L: int = 24, alpha: float = 0.6, tol: float = 0.075, 
                   nmix: int = 5, Niter: int = 40, seed: int = None) -> Tuple[float, float, int]:
    """Runs a full symmetry restoration experiment on a 2D SU(2) lattice."""
    if seed is not None:
        np.random.seed(seed)
        
    # Initialize maximum entropy noise lattice
    lattice = np.zeros((L, L, 2, 2, 2), dtype=np.complex128)
    for i in range(L):
        for j in range(L):
            for mu in range(2):
                lattice[i, j, mu] = random_su2()

    P0 = avg_plaquette(lattice)
    steps_taken = 0
    
    for it in range(Niter):
        lattice, cont = sspfi_step(lattice, alpha, tol, nmix)
        steps_taken += 1
        if not cont:
            break
            
    P_final = avg_plaquette(lattice)
    return P0, P_final, steps_taken

# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSPFI Engine for Deterministic Symmetry Restoration")
    parser.add_argument("-n", "--num_experiments", type=int, default=50, help="Number of experimental runs")
    parser.add_argument("-L", "--lattice_size", type=int, default=24, help="Lattice dimension L x L")
    parser.add_argument("--alpha", type=float, default=0.6, help="Weight parameter alpha")
    parser.add_argument("--tol", type=float, default=0.075, help="Fixed-point tolerance")
    parser.add_argument("--output", type=str, default="sspfi_results_svd_fixed.csv", help="Output CSV filename")
    
    args = parser.parse_args()

    print(f"--- Starting SSPFI Protocol ---")
    print(f"Lattice: {args.lattice_size}x{args.lattice_size} SU(2)")
    print(f"Experiments: {args.num_experiments} | Alpha: {args.alpha} | Tol: {args.tol}\n")

    start_time = time.time()
    results = []
    
    for s in range(args.num_experiments):
        current_seed = 12345 + s
        P0, P_final, steps = run_experiment(L=args.lattice_size, alpha=args.alpha, 
                                            tol=args.tol, seed=current_seed)
        results.append((current_seed, P0, P_final, steps))
        
        # Print progress every 10 runs
        if (s + 1) % 10 == 0 or s == 0:
            print(f"Run {s+1}/{args.num_experiments} | Seed: {current_seed} | P_final: {P_final:.6f} | Steps: {steps}")

    P_finals = [r[2] for r in results]
    steps_list = [r[3] for r in results]
    
    print("\n--- Experiment Summary ---")
    print(f"Mean P_final: {statistics.mean(P_finals):.8f}")
    print(f"Std  P_final: {statistics.pstdev(P_finals):.8f}")
    print(f"Total Time:   {time.time() - start_time:.2f} seconds")

    # Save to CSV
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seed", "P0", "P_final", "steps"])
        for row in results:
            writer.writerow(row)
            
    print(f"\nResults successfully saved to {args.output}")