import matplotlib.pyplot as plt
import numpy as np
import typer

app = typer.Typer()


def model(x, p):
    return x ** (2 * p + 1) / (1 + x ** (2 * p))


pparam = {"xlabel": "Voltage (mV)", "ylabel": r"Current ($\mu$A)"}

x = np.linspace(0.75, 1.25, 201)

# with plt.style.context(["science"]):
#     fig, ax = plt.subplots()
#     for p in [10, 15, 20, 30, 50, 100]:
#         ax.plot(x, model(x, p), label=p)
#     ax.legend(title="Order")
#     ax.autoscale(tight=True)
#     ax.set(**pparam)
#     fig.savefig("figures/fig1.pdf")
#     fig.savefig("figures/fig1.jpg", dpi=300)

# with plt.style.context(["science", "ieee"]):
#     fig, ax = plt.subplots()
#     for p in [10, 20, 40, 100]:
#         ax.plot(x, model(x, p), label=p)
#     ax.legend(title="Order")
#     ax.autoscale(tight=True)
#     ax.set(**pparam)
#     # Note: $\mu$ doesn't work with Times font (used by ieee style)
#     ax.set_ylabel(r"Current (\textmu A)")
#     fig.savefig("figures/fig2a.pdf")
#     fig.savefig("figures/fig2a.jpg", dpi=300)


with plt.style.context(["science", "ieee"]):
    fig, ax = plt.subplots()
    for p in [10, 20, 40, 100]:
        ax.plot(x, model(x, p), label=p)
    ax.legend(title="Order")
    ax.autoscale(tight=True)
    ax.set(**pparam)
    # Note: $\mu$ doesn't work with Times font (used by ieee style)
    ax.set_ylabel(r"Current (\textmu A)")
    import tikzplotlib

    tikzplotlib.save("test.tex")
    # fig.savefig("figures/fig2a.pdf")
    # fig.savefig("figures/fig2a.jpg", dpi=300)
