import matplotlib.pyplot as plt
import numpy as np
y_knots = [21.85, 23.27, 19.82, 28.13]
x_knots = list(range(len(y_knots)))
x = np.linspace(0, len(y_knots) - 1, 1000)

poly_deg = len(y_knots) - 1
coefs = np.polyfit(x_knots, y_knots, poly_deg)
y_poly = np.polyval(coefs, x)

plt.plot(x_knots, y_knots, "o", label="data points")
plt.plot(x, y_poly, label="polynomial fit")
plt.ylabel(r'$\frac{\kappa}{C} \rho$')
plt.legend()
plt.show()