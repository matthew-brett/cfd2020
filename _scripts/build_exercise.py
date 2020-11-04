#!/usr/bin/env python
""" Build exercise
"""

import os
import os.path as op
import sys
from argparse import ArgumentParser
from glob import glob
from zipfile import ZipFile


HERE = op.dirname(op.realpath(__file__))
SITE_ROOT = op.realpath(op.join(HERE, '..'))
sys.path.append(HERE)

from cutils import process_nb, path_of


def good_fname(fname):
    fn = op.basename(fname)
    froot, ext = op.splitext(fn)
    if froot.startswith('.'):
        return False
    if ext in ('.Rmd', '.pyc'):
        return False
    if froot.startswith('test_'):
        return False
    if froot.startswith('notes'):
        return False
    if froot.endswith('solution'):
        return False
    if froot.endswith('template'):
        return False
    if fn in ('__pycache__',
              'tests-extended',
              'Makefile'):
        return False
    return True


def pack_exercise(fname, out_path=None):
    path = path_of(fname)
    below_path, sdir_name = op.split(path)
    if out_path is None:
        out_path = os.getcwd()
    zip_fname = op.join(out_path, sdir_name + '.zip')
    listing = glob(op.join(path, '**'), recursive=True)
    files = [f for f in listing if good_fname(f)]
    with ZipFile(zip_fname, 'w') as zip_obj:
        for fn in files:
            arcname = op.relpath(fn, below_path)
            zip_obj.write(fn, arcname)


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
        process_nb(fname, execute=args.execute)
        pack_exercise(fname, args.out_path)


if __name__ == '__main__':
    main()
