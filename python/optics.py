"""
optics.py
"""
import os
import sys
import argparse
import logging
import yaml
import pprint

import numpy as np
import xarray as xr

import opac

from utils import log_normal, chebyshev_bilinear_fit
from plot_utils import plot_size_dist, plot_refindex


def read_cam_bands_sw(config):

    wvn_sw_edge = np.array(config['CAM_SW'])
    n_sw = len(wvn_sw_edge) - 1
    i_band = np.arange(n_sw)
    i_band[0] = n_sw

    wvn_sw_mid = (wvn_sw_edge[0:n_sw-1] + wvn_sw_edge[1:n_sw]) / 2

    wvl_sw_edge = 1.0e4 / wvn_sw_edge
    wvl_sw_mid = 1.0e4 / wvn_sw_mid

    for i, wvn_min, wvn_max \
        in zip(i_band, wvn_sw_edge[0:n_sw], wvn_sw_edge[1:n_sw+1]):
        logging.debug('band %2.2d, wvn = [%7.1f, %7.1f] cm-1'
            % (i, wvn_min, wvn_max))

    for i, wvl_max, wvl_min, wvl_mid \
        in zip(i_band, wvl_sw_edge[0:n_sw], wvl_sw_edge[1:n_sw+1], wvl_sw_mid):
        logging.debug('band %2.2d, wvl = [%5.2f, %5.2f, %5.2f] um'
            % (i, wvl_max, wvl_mid, wvl_min))

    return wvl_sw_edge, wvl_sw_mid


def process_opac(config):

    for aerosol_type in config['OPAC']:
        filename = os.path.expandvars(config['OPAC'][aerosol_type]['filename'])
        logging.debug(aerosol_type)
        opac.read_opac(filename)


def process_aerosol(config, type_str):
    type_name = os.path.expandvars(config['Types'][type_str]['name'])
    logging.debug(type_name)
    filename = os.path.expandvars(config['Types'][type_str]['filename'])
    logging.debug(filename)
    ds = xr.open_dataset(filename)

    density = config['Types'][type_str]['density']
    logging.debug('density:%4.2f g cm-3' % density)
    hygroscopicity = config['Types'][type_str]['hygroscopicity']
    logging.debug(('hygroscopicity:', hygroscopicity))

    """
    i_vis = 6
    logging.debug('refreal:%6.4f', ds['refreal'].values[0, 0, i_vis])
    logging.debug('refimag:%6.4f', ds['refimag'].values[0, 0, i_vis])
    """

    aerosol_data = dict()
    aerosol_data['type_name'] = type_name
    aerosol_data['density'] = density
    aerosol_data['hygroscopicity'] = hygroscopicity
    aerosol_data['plot_color'] = config['Types'][type_str]['plot_color']

    if type_str == 'WAT':
        aerosol_data['wvl'] = ds['wavelength1'].values[:]
        aerosol_data['refreal'] = ds['watern'].values[:]
        aerosol_data['refimag'] = np.abs(ds['wateri'].values[:])
    elif type_str == 'ICE':
        aerosol_data['wvl'] = ds['wavelength1'].values[:]
        aerosol_data['refreal'] = ds['icen'].values[:]
        aerosol_data['refimag'] = np.abs(ds['icei'].values[:])
    else:
        aerosol_data['wvl'] = 1.0e6 * ds['lambda'].values[:]
        aerosol_data['refreal'] = ds['refreal'].values[0, 0, :]
        aerosol_data['refimag'] = np.abs(ds['refimag'].values[0, 0, :])

    return aerosol_data


def print_mode_info(config, mam_str, mode_str, aerosol_data):

    pp = pprint.PrettyPrinter(depth=4)

    filename = os.path.expandvars(config[mam_str][mode_str]['filename'])
    mode_name = config[mam_str][mode_str]['name']
    logging.debug(filename)
    ds = xr.open_dataset(filename)

    dgnum = ds['dgnum'].values * 1.0e6
    dgnumlo = ds['dgnumlo'].values * 1.0e6
    dgnumhi = ds['dgnumhi'].values * 1.0e6
    sigmag = ds['sigmag'].values

    print('\n')
    print(mode_str)
    pp.pprint(config[mam_str][mode_str])
    print('dgnum:%7.4f um' % dgnum)
    print('dgnumlo:%7.4f um' % dgnumlo)
    print('dgnumhi:%7.4f um' % dgnumhi)
    print('sigmag:%5.2f um' % sigmag)
    print('rhcrystal:%5.2f' % ds['rhcrystal'].values)
    print('rhdeliques:%5.2f' % ds['rhdeliques'].values)


def process_mam(config, mam_str, mode_str, mixture_str, aerosol_data):

    filename = os.path.expandvars(config[mam_str][mode_str]['filename'])
    mode_name = config[mam_str][mode_str]['name']
    logging.debug(filename)
    ds = xr.open_dataset(filename)
    logging.debug(ds['extpsw'].dims)
    logging.debug(ds['extpsw'].shape)
    # ('sw_band', 'mode', 'refindex_im', 'refindex_real', 'coef_number')

    band_vis = 10

    logging.debug(mode_name)
    dgnum = ds['dgnum'].values * 1.0e6
    dgnumlo = ds['dgnumlo'].values * 1.0e6
    dgnumhi = ds['dgnumhi'].values * 1.0e6
    sigmag = ds['sigmag'].values
    logging.debug('dgnum:%7.4f um' % dgnum)
    logging.debug('dgnumlo:%7.4f um' % dgnumlo)
    logging.debug('dgnumhi:%7.4f um' % dgnumhi)
    logging.debug('sigmag:%5.2f um' % sigmag)
    logging.debug('rhcrystal:%5.2f' % ds['rhcrystal'].values)
    logging.debug('rhdeliques:%5.2f' % ds['rhdeliques'].values)

    refindex_real_vis = ds['refindex_real_sw'][band_vis-1,:]
    refindex_im_vis = ds['refindex_im_sw'][band_vis-1,:]
    extpvis = ds['extpsw'][band_vis-1,0,:,:,:]

    N = 100
    RH_OPAC_list = [0, 50, 70, 80, 90, 95, 98, 99]

    B_coeff_mean = np.zeros(3)
    vol_mean = 0.0
    for aerosol_type in config['Mixtures'][mixture_str]:
        mass_fraction = config['Mixtures'][mixture_str][aerosol_type]
        density = aerosol_data[aerosol_type]['density']
        B_coeff = np.array(aerosol_data[aerosol_type]['hygroscopicity'])
        # print(aerosol_type, mass_fraction, density, B_coeff)
        B_coeff_mean += (mass_fraction / density) * B_coeff
        vol_mean += mass_fraction / density
    B_coeff_mean /= vol_mean
    # print(B_coeff_mean)

    f_D_dict = dict()

    x_a = 1.0 / (np.log(dgnumhi) - np.log(dgnumlo))
    x_b = np.log(dgnumhi) + np.log(dgnumlo)

    for RH in RH_OPAC_list:
        relhum = 0.01 * RH
        B = B_coeff_mean[0] + B_coeff_mean[1] * relhum + B_coeff_mean[2] * relhum**2
        dgwet = dgnum * (1 - B / np.log(relhum))**(1.0/3.0)
        D, f_D = log_normal(dgwet, sigmag, dgnumlo, dgnumhi, N, normalize=True)
        f_D_dict[RH] = f_D
        x = x_a * (2 * np.log(dgwet) - x_b)
        # print(RH, dgwet, x)
        # chebyshev_bilinear_fit(
        #     refindex_im_vis, refindex_real_vis, extpvis)

    # plot_size_dist(D, f_D_dict)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--bands', type=str,
        default='bands.yaml',
        help='yaml bands file')
    parser.add_argument('--aerosol', type=str,
        default='aerosol.yaml',
        help='yaml aerosol file')
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)

    """
    Read YAML config
    """
    with open(args.bands, 'r') as f:
        bands_config = yaml.safe_load(f)
    with open(args.aerosol, 'r') as f:
        aerosol_config = yaml.safe_load(f)

    # wvl_sw_edge, wvl_sw_mid = read_cam_bands_sw(bands_config)

    aerosol_type_data = dict()

    for aerosol_type in ['WAT', 'ICE', 'SS', 'SU', 'POM', 'SOA', 'BC', 'DU']:
        aerosol_type_data[aerosol_type] \
            = process_aerosol(aerosol_config, aerosol_type)

    # plot_refindex(aerosol_type_data)

    for mode in ['Mode1', 'Mode2', 'Mode3', 'Mode4']:
        print_mode_info(aerosol_config, 'MAM4', mode, aerosol_type_data)

