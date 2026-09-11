import matplotlib.pyplot as plt
import numpy as np

S0 = 100
alpha = 0.5
beta = 0.05
pi_I = 0.30
pi_L = 0.70

f_P = {90: 0.10, 95: 0.20, 100: 0.40, 105: 0.20, 110: 0.10}


def pi_LB(x):
    return max(alpha - beta * x, 0)


def G(A, B):
    x_ask = A - S0
    x_bid = S0 - B
    return pi_L * (pi_LB(x_ask) * x_ask + pi_LB(x_bid) * x_bid)


def L(A, B):
    loss_ask = sum((P - A) * p for P, p in f_P.items() if P > A)
    loss_bid = sum((B - P) * p for P, p in f_P.items() if P < B)
    return pi_I * (loss_ask + loss_bid)


def evaluate(d):
    A, B = S0 + d, S0 - d
    g, l = G(A, B), L(A, B)
    return {"d": d, "A": A, "B": B, "G": g, "L": l, "pi": g - l}


if __name__ == "__main__":
    for d in [2, 5, 8]:
        r = evaluate(d)
        print(f"d={r['d']} | A={r['A']} B={r['B']} | "
              f"G={r['G']:.4f} L={r['L']:.4f} pi={r['pi']:.4f}")

    ds = np.arange(0, 10.01, 0.01)
    pis = np.array([evaluate(d)["pi"] for d in ds])

    idx_opt = np.argmax(pis)
    d_opt, pi_opt = ds[idx_opt], pis[idx_opt]
    print(f"\nOptimum: d={d_opt:.2f} | pi*={pi_opt:.3f}")

    candidates = [2, 5, 8]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ds, pis, color="gold", linewidth=2, label="pi(d)")

    for d in candidates:
        r = evaluate(d)
        ax.scatter(d, r["pi"], color="dodgerblue", marker="D", s=80, zorder=5)
        ax.annotate(f"d={d}", (d, r["pi"]), textcoords="offset points",
                    xytext=(-25, 10), ha="center")

    ax.scatter(d_opt, pi_opt, color="limegreen", marker="*", s=250, zorder=5)
    ax.annotate(f"optimum (d={d_opt:.2f}, pi*={pi_opt:.3f})",
                (d_opt, pi_opt), textcoords="offset points",
                xytext=(15, -25), ha="left")

    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_ylim(pis.min() - 0.15, pis.max() + 0.3)
    ax.set_xlabel("d (quote distance)")
    ax.set_ylabel("Dealer expected utility, pi(d)")
    ax.set_title("Dealer utility vs. quote distance")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("copeland_galai_plot.png", dpi=150)
