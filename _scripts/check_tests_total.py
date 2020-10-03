#!/usr/bin/env python
""" Check total points for tests in test directory
"""

import os.path as op
from glob import glob
from argparse import ArgumentParser


def fname2points(fname):
    with open(fname, 'rt') as fobj:
        ns = {}
        exec(fobj.read(), ns)
    return ns['test']['points']


def get_args():
    parser = ArgumentParser(__doc__)
    parser.add_argument('tests_dir',
                        help='Path to notebook test directory')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    print(args)
    fnames = sorted(glob(op.join(args.tests_dir, 'q*.py')))
    total = 0
    for fn in fnames:
        points = fname2points(fn)
        print(f'{fn}: {points}')
        total += points
    print(f'Total for tests dir {args.tests_dir}: {total}')


if __name__ == '__main__':
    main()
