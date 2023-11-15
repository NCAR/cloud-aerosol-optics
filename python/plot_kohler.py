import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')

from utils import kohler

T = 293.0
B = 1.0
plt.ylim(0.5, 1.03)
plt.xscale('log')
plt.xlabel('r_w (um)')
plt.ylabel('RH')

r_d = 1.0e-8
r_w = np.logspace(-8, -5, 1000)
log_RH = kohler(T, B, r_d, r_w)
RH = np.exp(log_RH)
log_RH_B = - B * r_d**3 / (r_w**3 - r_d**3) 
RH_B = np.exp(log_RH_B)
plt.plot(1.0e6 * r_w, RH, color='black')
plt.plot(1.0e6 * r_w, RH_B, '--', color='blue')
plt.text(0.02, 0.8, 'r_d = 0.01 um')

r_d = 1.0e-7
r_w = np.logspace(-7, -5, 1000)
log_RH = kohler(T, B, r_d, r_w)
RH = np.exp(log_RH)
log_RH_B = - B * r_d**3 / (r_w**3 - r_d**3) 
RH_B = np.exp(log_RH_B)
plt.plot(1.0e6 * r_w, RH, color='black')
plt.plot(1.0e6 * r_w, RH_B, '--', color='blue')
plt.text(0.2, 0.7, 'r_d = 0.1 um')

r_d = 1.0e-6
r_w = np.logspace(-6, -5, 1000)
log_RH = kohler(T, B, r_d, r_w)
RH = np.exp(log_RH)
log_RH_B = - B * r_d**3 / (r_w**3 - r_d**3) 
RH_B = np.exp(log_RH_B)
plt.plot(1.0e6 * r_w, RH, color='black')
plt.plot(1.0e6 * r_w, RH_B, '--', color='blue')
plt.text(1.5, 0.6, 'r_d = 1 um')

plt.title('B = 1    T = 20 C')
plt.savefig('kohler.png', dpi=300)

