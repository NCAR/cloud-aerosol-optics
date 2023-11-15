import logging
import matplotlib.pyplot as plt 
import numpy as np


def chebyshev_bilinear_fit(u_table, v_table, coeff, u, v, x):
    """
    T_0 = 1
    T_1 = x
    T_2 = 2 x^2 - 1
    T_3 = 4 x^3 - 3 x
    T_4 = 8 x^4 - 8 x^2 + 1
    """
    pass


def log_normal(mu_g, sigma_g, x_min, x_max, N, normalize=False):
    """
    f(x) = 1 / (x log(sigma_g) sqrt(2 pi))
           exp( - (log(x) - log(mu_g))^2 / (2 log^2(sigma_g)) )
    """
    x = np.linspace(x_min, x_max, N)
    # logging.debug(x)
    f = np.exp( - (np.log(x) - np.log(mu_g))**2 / (2 * (np.log(sigma_g))**2) ) \
      / (x * np.log(sigma_g) * np.sqrt(2 * np.pi))
    if normalize:
        f /= f.max()
    # logging.debug(f)
    return x, f


def saturation_vapor_pressure_simple(T):
    """
    Feynman Volume I equation 45.15, Wallace and Hobbs problem 2.25

    e = const exp(- L / (R T))
    e_0 = const exp(- L / (R T_0))
    e = e_0 exp(- (L / R) (1 / T - 1 / T_0))
    """
    e_0 = 6.112  # mb
    T_0 = 273.15 # K
    L   = 2.5e6  # J kg-1
    R_v = 461    # J K-1 kg-1
    return e_0 * np.exp(- (L / R_v) * (1 / T - 1 / T_0))


def saturation_vapor_pressure_empirical(T):
    return 6.112 * np.exp(17.67 * (T - 273.15) / (T - 29.65))


def water_fraction():
    """
    volume mixing ratio q_j / rho_j for species j
    sum_j (all species except water) q_j / rho_j = vmr = (dry volume mixing ratio)
    vmr_wet = vmr_dry * (r_w / r_d)^3
    q_w / rho_w = vmr_wet - vmr_dry
    """
    pass


def kohler(T, B, r_d, r_w):
    """
    A = 2 M_w sigma / (R T rho_w)
    M_w molecular weight water
    sigma surface tension water
    R ideal gas constant
    log(RH) = A / r_w - B r_d^3 / (r_w^3 - r_d^3)

    A ~ 0
    x = r_w / r_d
    log(RH) / B = - 1 / (x^3 - 1) 
    x^3 - 1 = - B / log(RH)
    x = [1 - B / log(RH)]^(1/3)
    """
    M_w = 18.016  # kg kmol-1
    rho_w = 1.0e3 # kg m-3
    sigma = 0.076 # J m-2
    R = 8.3143e3  # J K-1 kmol-1

    # kg kmol-1 J m-2 / (J kmol-1 kg m-3)
    A = 2 * M_w * sigma / (R * rho_w * T) 
    print('A', A)
    logging.debug('%.2e m' % A)

    log_RH = A / r_w - B * r_d**3 / (r_w**3 - r_d**3) 
    return log_RH


if __name__ == '__main__':

    T = np.arange(0, 51, 1) + 273.15
    e_sat = saturation_vapor_pressure_empirical(T) 
    e_sat_simple = saturation_vapor_pressure_simple(T) 
    plt.plot(T, e_sat, color='k')
    plt.plot(T, e_sat_simple, color='b')
    plt.show()
