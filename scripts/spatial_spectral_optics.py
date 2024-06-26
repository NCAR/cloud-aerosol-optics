import os
import sys
import argparse
import logging
import yaml
import numpy as np
import pandas as pd
import xarray as xr
from pprint import pprint

from analysis_utils import fill_date_template


def read_aerosol_optics(filename):

    logging.info(filename)
    with open(args.aerosol, 'r') as f:
        aerosol_config = yaml.safe_load(f)
        pprint(aerosol_config)

    file_su = os.path.expandvars(
        aerosol_config['Types']['SU']['filename'])
    logging.info(file_su)
    ds_su = xr.open_dataset(file_su)
    pprint(ds_su)

    file_oc = os.path.expandvars(
        aerosol_config['Types']['POM']['filename'])
    logging.info(file_oc)
    ds_oc = xr.open_dataset(file_oc)
    pprint(ds_oc)

    file_bc = os.path.expandvars(
        aerosol_config['Types']['BC']['filename'])
    logging.info(file_bc)
    ds_bc = xr.open_dataset(file_bc)
    pprint(ds_bc)

    file_du = os.path.expandvars(
        aerosol_config['Types']['DU']['filename'])
    logging.info(file_du)
    ds_du = xr.open_dataset(file_du)
    pprint(ds_du)

    file_ss = os.path.expandvars(
        aerosol_config['Types']['SS']['filename'])
    logging.info(file_ss)
    ds_ss = xr.open_dataset(file_ss)
    pprint(ds_ss)

    return ds_su, ds_oc, ds_bc, ds_du, ds_ss


def process_file(filename, ds_su, ds_oc, ds_bc, ds_du, ds_ss):
    logging.info(filename)
    ds = xr.open_dataset(filename)
    pprint(ds['SO4'])

    # tau_ext_su = ds_su


if __name__ == '__main__':

    """
    Parse command line arguments
    """     
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    parser.add_argument('--datadir', type=str,
        default=os.path.join(os.getenv('HOME'), 'Data'),
        help='top-level data directory (default $HOME/Data)')
    parser.add_argument('--aerosol', type=str,
        default=os.path.join('..', 'optics', 'aerosol.yaml'),
        help='yaml aerosol file')
    parser.add_argument('--start', type=str,
        default='20080701',
        help='start date (yyyymmdd)')
    parser.add_argument('--end', type=str,
        default='20080701',
        help='end date (yyyymmdd)')
    parser.add_argument('--file_pattern', type=str,
        default=os.path.join('MERRA2_inst3', 'aer_Nv',
            'MERRA2_300.inst3_3d_aer_Nv.YYYYMMDD.nc4'))
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)

    ds_su, ds_oc, ds_bc, ds_du, ds_ss \
        = read_aerosol_optics(args.aerosol)

    dates = pd.date_range(start=args.start, end=args.end, freq='D')
    logging.info(dates)

    for date in dates:
        date_str = date.strftime('%Y-%m-%b-%d-%j')
        filepath = os.path.join(args.datadir,
            fill_date_template(args.file_pattern, date_str))
        process_file(filepath, ds_su, ds_oc, ds_bc, ds_du, ds_ss)

