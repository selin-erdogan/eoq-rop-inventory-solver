# EOQ / ROP Inventory Solver

A command-line tool that finds the optimal **order quantity (Q\*)** and **reorder point (R\*)** for a stochastic continuous-review inventory model (Q–R policy) with normally distributed lead-time demand. Written in Python for the **CP-4** course term project.

## How it works
1. Reads costs (unit cost, ordering cost, penalty cost, interest rate) and demand parameters (lead time, mean and standard deviation of lead-time demand).
2. Starts from the classic EOQ, `Q = sqrt(2·λ·K / h)`.
3. Iterates until Q converges:
   - `F(R) = 1 − Q·h / (p·λ)`, `Z = Φ⁻¹(F(R))`, `R = μ_L + Z·σ_L`
   - normal loss function `n(R) = φ(Z) − Z·(1 − Φ(Z))`
   - `Q = sqrt(2·λ·(K + p·n(R)) / h)`
4. Prints every iteration and the final performance measures: safety stock, annual holding / setup / penalty cost, total annual cost, average time between orders, probability of no stockout in a cycle and proportion of demand not met.

## Run
```bash
pip install -r requirements.txt
python eoq_rop_solver.py
```

## Tech
Python 3, SciPy (`scipy.stats.norm`)
