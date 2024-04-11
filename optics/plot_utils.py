import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')


def plot_size_dist(D, f_D, D_min=0.01, D_max=4.0):
    for RH in f_D:
        print(RH)
        plt.semilogx(D, f_D[RH], color=(0,0,0.01*RH))
        plt.xlim([D_min, D_max])

    plt.show()


def plot_refindex(aerosol_type_data):

    fig, ax = plt.subplots(2, 2, sharex='col', sharey='row')

    ax[0, 0].plot([0.55, 0.55], [1, 2.5], color='black', linewidth=1)
    ax[0, 0].set_xlim([0, 5])
    ax[0, 0].set_ylim([1, 2.5])
    ax[0, 0].set_title('SW Real Index of Refraction')
    ax[0, 0].set_xticks([0.55, 1, 2, 3, 4])
    ax[0, 0].set_xticklabels(['0.55', '1', '2', '3', '4'])

    ax[0, 1].set_xlim([5, 40])
    ax[0, 1].set_title('LW Real Index of Refraction')
    ax[0, 1].set_ylabel(r'$n_R$')

    ax[1, 0].plot([0.55, 0.55], [0, 1], color='black', linewidth=1)
    ax[1, 0].set_xlim([0, 5])
    ax[1, 0].set_ylim([0, 1])
    ax[1, 0].set_title('SW Imaginary Index')
    ax[1, 0].set_xlabel(r'$\lambda$ ($\mu$m)')

    ax[1, 1].set_xlim([5, 40])
    ax[1, 1].set_title('LW Imaginary Index')
    ax[1, 1].set_xlabel(r'$\lambda$ ($\mu$m)')
    ax[1, 1].set_ylabel(r'$n_I$')

    for aerosol_type in aerosol_type_data:
        aerosol_data = aerosol_type_data[aerosol_type]

        print('wvl', aerosol_data['wvl'])
        print(aerosol_type + ' real', aerosol_data['refreal'])
        print(aerosol_type + ' imag', aerosol_data['refimag'])

        ax[0, 0].plot(
            aerosol_data['wvl'], aerosol_data['refreal'],
            label=aerosol_type, color=aerosol_data['plot_color'])

        ax[0, 1].plot(
            aerosol_data['wvl'], aerosol_data['refreal'],
            label=aerosol_type, color=aerosol_data['plot_color'])

        ax[1, 0].plot(
            aerosol_data['wvl'], aerosol_data['refimag'],
            label=aerosol_type, color=aerosol_data['plot_color'])

        ax[1, 1].plot(
            aerosol_data['wvl'], aerosol_data['refimag'],
            label=aerosol_type, color=aerosol_data['plot_color'])

    ax[1, 0].legend(loc='upper left')

    plt.savefig('refindex.pdf')
    plt.show()

