#!/usr/bin/env python
""" Build exercise
"""

import os
import os.path as op
import sys
from argparse import ArgumentParser
from shutil import make_archive

from rnbgrader.tmpdirs import in_dtemp

HERE = op.dirname(op.realpath(__file__))
SITE_ROOT = op.realpath(op.join(HERE, '..'))
sys.path.append(HERE)

from cutils import process_write_nb, path_of, write_dir


def pack_exercise(fname, out_path=None):
    if out_path is None:
        out_path = os.getcwd()
    in_path = path_of(fname)
    below_path, sdir_name = op.split(in_path)
    zip_froot = op.join(out_path, sdir_name)
    with in_dtemp():
        write_dir(in_path, sdir_name)
        make_archive(zip_froot, 'zip')


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('notebook', nargs='+',
                        help='Notebook(s) to clean')
    parser.add_argument('--execute', action='store_true',
                        help='If specified, execute notebooks before cleaning')
    parser.add_argument('--out-path', default=os.getcwd(),
                        help='Output path for zipped exercise (default pwd)')
    return parser


def main():
    args = get_parser().parse_args()
    for fname in args.notebook:
        process_write_nb(fname, execute=args.execute)
        pack_exercise(fname, args.out_path)


if __name__ == '__main__':
    main()
