#!/usr/bin/env python3
#
# Reads through a (!) sorted .csv document and returns the best wavelet and parameters
# according to the metrics. For sorting see sort_csv.py
#
# @author David Rubin, 2019
import os
import sys
import csv
import argparse


def main(args):
    """Read through a csv file and return the lines with best metrics (according to args)"""
    if not os.path.isfile(args.csv_file):
        print('Given argument ({}) is not a file.'.format(args.csv_file))
        sys.exit(1)
    top_metrics = {}
    taken = 0
    line_count = 1;
    with open(args.csv_file) as f:
        reader = csv.DictReader(f)

        # Read every line and store the appropriate ones (compression ratio should fall the further you read)
        for metric in reader:
            if float(metric['pearson correlation']) >= args.pearson and float(metric['nrmse']) <= args.nrmse:
                # Line fullfills the conditions
                top_metrics[line_count] = metric
                taken += 1
            # Increase the line count and check if we already have the limit of metrics taken
            line_count += 1
            if taken >= args.limit:
                break
    # Print out the metrics, if None were taken, print a custom message
    if taken == 0:
        print('None of the metrics satisfy the given conditions: Pearson coef.>={} and NRMSE<={}'.format(args.pearson,
                                                                                                         args.nrmse))
        return {}
    else:
        print('\nTOP {} metrics from {}'.format(taken, args.csv_file))
        print('\tWavelet\tThreshold\tLevels\tMode\tPearson cor.\t{:>8s}\tCompression'.format('NRMSE'))
        for _, metric in top_metrics.items():
            print('\t{:>7s}\t{:>9s}\t{:>6s}\t{}\t{:12.6f}\t{:1.6f}\t{:11.6f}'.format(
                metric['wavelet'], metric['threshold'], metric['levels'], metric['mode'],
                float(metric['pearson correlation']), float(metric['nrmse']), float(metric['compression ratio'])))
        print('\nConditions: Pearson >= {}\tand\tNRMSE <= {}'.format(args.pearson, args.nrmse))


if __name__ == '__main__':
    _parser = argparse.ArgumentParser("Return the best wavelet and parameters from a sorted .csv document")
    _parser.add_argument('csv_file', help='The .csv file (metrics from dwt.py)')
    _parser.add_argument('-p', '--pearson', help='The minimum Pearson coefficient value (inclusive)', type=float,
                         default=.99)
    _parser.add_argument('-e', '--nrmse', help='The maximum NRMSE value (inclusive)', type=float, default=.01)
    _parser.add_argument('-l', '--limit', help='Number of results to display', type=int, default=3)

    _args = _parser.parse_args()
    main(_args)
