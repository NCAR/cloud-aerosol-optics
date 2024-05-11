import os
import sys
import argparse
import logging
import numpy as np
import pandas as pd
import xarray as xr

from analysis_utils import fill_date_template


def process_file(filename):
    logging.info(filename)


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
    parser.add_argument('--start', type=str,
        default='20080801',
        help='start date (yyyymmdd)')
    parser.add_argument('--end', type=str,
        default='20080801',
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

    dates = pd.date_range(start=args.start, end=args.end, freq='D')
    logging.info(dates)

    for date in dates:
        date_str = date.strftime('%Y-%m-%b-%d-%j')
        filename = fill_date_template(args.file_pattern, date_str)
        process_file(filename)

