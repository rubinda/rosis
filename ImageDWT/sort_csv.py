#!/usr/bin/env python3
#
# Sorts a csv document from dwt.py according to compression ratio, nrmse and pearson correlation
#
# @author David Rubin, 2019
import csv
import os
from sys import exit
import argparse


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('csv_file', help='the csv file produced in dwt.py (use wavelet "all")')
    args = _parser.parse_args()

    if not os.path.isfile(args.csv_file):
        print('Given argument ({}) is not a valid file'.format(args.csv_file))
        exit(1)

    with open(args.csv_file) as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        data_sorted = sorted(data, key=lambda result: (float(result['compression ratio']), float(result['nrmse']),
                                                       float(result['pearson correlation'])), reverse=True)
        # Print out the top 3 results
        print('Wavelet\t\tPearson c.\tNRMSE\tCompression')
        for row in data_sorted[:3]:
            print('{:7s}\t\t{:.4f}\t\t{:.4f}\t{:.4f}'.format(row['wavelet'], float(row['pearson correlation']),
                  float(row['nrmse']), float(row['compression ratio'])))

    # Rewrite the file with the sorted data
    with open(args.csv_file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data_sorted[0].keys())
        writer.writeheader()
        writer.writerows(data_sorted)