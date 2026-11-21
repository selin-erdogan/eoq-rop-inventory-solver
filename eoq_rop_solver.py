import math
from scipy.stats import norm

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  >> Geçersiz giriş. Lütfen sayısal bir değer girin.")

def solve():
    print("=" * 60)
    print("   EOQ-ROP INVENTORY OPTIMIZATION SOFTWARE")
    print("=" * 60)

    # ── STEP 1: Costs & interest rate ────────────────────────────
    print("\n[1] COST PARAMETERS\n")
    c = get_float("   Unit cost (c)           : $")
    K = get_float("   Ordering cost (K)       : $")
    p = get_float("   Penalty cost (p)        : $")
    i = get_float("   Annual interest rate (i): ")   # e.g. 0.25

    h = c * i
    print(f"\n   >> Holding cost (h = c x i): ${h:.4f} per unit per year")

    # ── STEP 2: Lead time & demand parameters ────────────────────
    print("\n[2] LEAD TIME & DEMAND PARAMETERS\n")
    L_years = get_float("   Lead time (years)              : ")
    mu_L    = get_float("   Lead time demand - mean (mu_L) : ")
    sigma_L = get_float("   Lead time demand - std dev (sL): ")

    lam = mu_L / L_years   # annual demand
    print(f"\n   >> Annual demand (lambda = mu_L / L): {lam:.2f} units/year")

    # ── STEP 3: Iterative Q-R procedure ──────────────────────────
    print("\n" + "=" * 60)
    print("   ITERATION DETAILS")
    print("=" * 60)

    epsilon  = 0.5
    max_iter = 100

    Q = math.sqrt(2 * lam * K / h)   # initial EOQ
    iteration = 0

    while True:
        iteration += 1
        Q_prev = Q

        FR = 1 - (Q * h) / (p * lam)
        FR = max(0.0001, min(0.9999, FR))

        Z     = norm.ppf(FR)
        R     = mu_L + Z * sigma_L
        phi_Z = norm.pdf(Z)
        Phi_Z = norm.cdf(Z)
        nR    = phi_Z - Z * (1 - Phi_Z)
        Q     = math.sqrt(2 * lam * (K + p * nR) / h)

        print(f"\n  Iteration {iteration}:")
        print(f"    Q_prev  = {Q_prev:.4f}")
        print(f"    F(R)    = {FR:.6f}")
        print(f"    Z       = {Z:.4f}")
        print(f"    R       = {R:.4f}")
        print(f"    phi(Z)  = {phi_Z:.6f}")
        print(f"    n(R)    = {nR:.6f}")
        print(f"    Q_new   = {Q:.4f}")

        if abs(Q - Q_prev) < epsilon:
            print(f"\n  >> Converged after {iteration} iteration(s).")
            break
        if iteration >= max_iter:
            print(f"\n  >> Stopped: max iterations ({max_iter}) reached.")
            break

    # ── STEP 4: Performance measures ─────────────────────────────
    Q_star = Q
    R_star = R

    safety_stock   = Z * sigma_L
    annual_holding = h * (Q_star / 2 + Z * sigma_L)
    annual_setup   = K * (lam / Q_star)
    annual_penalty = p * (lam / Q_star) * nR * sigma_L
    total_cost     = annual_holding + annual_setup + annual_penalty
    avg_time_yr    = Q_star / lam
    avg_time_mo    = avg_time_yr * 12
    prob_no_so     = FR
    prop_unmet     = (nR * sigma_L) / Q_star

    print("\n" + "=" * 60)
    print("   RESULTS  —  All Performance Measures")
    print("=" * 60)
    print(f"\n  Optimal Lot Size      (Q*)  : {Q_star:.2f}  (~{round(Q_star)} units)")
    print(f"  Optimal Reorder Point (R*)  : {R_star:.2f}  (~{round(R_star)} units)")
    print(f"  Number of Iterations        : {iteration}")
    print(f"\n  Safety Stock (Z * sigma_L)  : {safety_stock:.4f} units")
    print(f"  Avg Annual Holding Cost     : ${annual_holding:.4f}")
    print(f"  Avg Annual Setup Cost       : ${annual_setup:.4f}")
    print(f"  Avg Annual Penalty Cost     : ${annual_penalty:.4f}")
    print(f"  Total Annual Cost           : ${total_cost:.4f}")
    print(f"  Avg Time Between Orders     : {avg_time_yr:.4f} yr  ({avg_time_mo:.4f} months)")
    print(f"  Prop. Cycles w/ No Stockout : {prob_no_so:.6f}  ({prob_no_so*100:.2f}%)")
    print(f"  Prop. Demands Not Met       : {prop_unmet:.6f}  ({prop_unmet*100:.4f}%)")
    print("=" * 60)

if __name__ == "__main__":
    solve()