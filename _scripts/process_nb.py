#!/usr/bin/env python
""" Process notebook for distribution
"""

import os.path as op
import sys
from argparse import ArgumentParser


HERE = op.dirname(op.realpath(__file__))
SITE_ROOT = op.realpath(op.join(HERE, '..'))
sys.path.append(HERE)

from cutils import process_nb, write_nb


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('notebook',
                        help='Notebook to process')
    parser.add_argument('out_notebook',
                        help='Output path for processed notebook')
    parser.add_argument('--execute', action='store_true',
                        help='If specified, execute notebook before processing')
    return parser


def main():
    args = get_parser().parse_args()
    nb = process_nb(args.notebook, execute=args.execute)
    write_nb(nb, args.out_notebook)


if __name__ == '__main__':
    main()
