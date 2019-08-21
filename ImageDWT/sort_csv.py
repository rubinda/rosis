#!/usr/bin/env python3
#
# Sorts a csv document from dwt.py according to compression ratio, nrmse and pearson correlation
#
# @author David Rubin, 2019
import os
import csv
import glob
from sys import exit
import argparse


def sort_csv(filename, verbose=False):
    """Sorts and rewrites the csv file"""
    if not os.path.isfile(filename):
        print('Given argument ({}) is not a valid file'.format(args.csv_file))
        exit(1)

    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        data_sorted = sorted(data, key=lambda result: (float(result['compression ratio']), float(result['nrmse']),
                                                       float(result['pearson correlation'])), reverse=True)
        if verbose:
            # Print out the top 3 results
            print('Wavelet\t\tPearson c.\tNRMSE\tCompression')
            for row in data_sorted[:3]:
                print('{:7s}\t\t{:.4f}\t\t{:.4f}\t{:.4f}'.format(row['wavelet'], float(row['pearson correlation']),
                                                                 float(row['nrmse']), float(row['compression ratio'])))

        # Rewrite the file with the sorted data
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data_sorted[0].keys())
        writer.writeheader()
        writer.writerows(data_sorted)


def sort_dir_files(directory, verbose=False):
    """
    Sort all .csv files in a directory

    :returns Number of csv files sorted
    """
    if not os.path.isdir(directory):
        print('Given argument ({}) is not a valid directory.'.format(directory))
        exit(1)
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    if len(csv_files) < 1:
        print('Given directory has no .csv files')
        return 0

    for f in csv_files:
        sort_csv(f, verbose)

    return len(csv_files)


if __name__ == '__main__':
    _parser = argparse.ArgumentParser(description='Sort single/multiple .csv files by compression ratio, '
                                                  'nrmse and pearson correlation.')
    _group = _parser.add_mutually_exclusive_group(required=True)
    _group.add_argument('-f', '--csv_file', help='the .csv file produced in dwt.py (use wavelet "all")')
    _group.add_argument('-d', '--dir', help='Directory that has .csv files')
    _parser.add_argument('-v', '--verbose', help='Print top 3 lines for each .csv file',
                         action='store_true', default=False)
    args = _parser.parse_args()

    if args.csv_file:
        # Sort a single file only
        sort_csv(args.csv_file, args.verbose)
    elif args.dir:
        # Sort all .csv files inside the directory
        sort_dir_files(args.dir, args.verbose)
    else:
        # Argparse already handles this situation.
        print('No option selected (use -h for help)')
        exit(0)
