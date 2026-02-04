import numpy as np
import matplotlib.pyplot as plt

a = np.linspace(0.2, 1.0, 400)

# example parameters (edit later)
xi0, xia = 0.02, -0.03
at, Delta = 0.6, 0.04
xi_0, xi_1 = 0.02, 0.02

xi_lin = xi0 + xia*(1-a)
xi_switch = xi_0*(1+np.tanh((a-at)/Delta))/2 - xi_1*(1-np.tanh((a-at)/Delta))/2

plt.figure()
plt.plot(a, xi_lin, label="xi(a)=xi0+xia(1-a)")
plt.plot(a, xi_switch, label="tanh switch")
plt.xlabel("a")
plt.ylabel("xi(a)")
plt.legend()
plt.tight_layout()
plt.savefig("figures/xi_examples.pdf")

