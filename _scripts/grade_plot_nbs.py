#!/usr/bin/env python
""" Grade notebooks for grading plots
"""

import os
import os.path as op
from argparse import ArgumentParser

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

EXE_PRE = ExecutePreprocessor()


def get_args():
    parser = ArgumentParser(__doc__)
    parser.add_argument('nb_fnames', nargs='+',
                        help='Paths to notebooks')
    parser.add_argument('--out-path',
                        help='Path to write plot notebooks '
                        '(default is notebook directory)')
    parser.add_argument('--ext-path',
                        help='Path to execute notebooks '
                        '(default is notebook directory)')
    args = parser.parse_args()
    return args


def execute_nb(nb, path):
    storage_path = op.join(path, '.ok_storage')
    if op.exists(storage_path):
        os.unlink(storage_path)
    EXE_PRE.preprocess(nb, {'metadata': {'path': path}})
    return nb


def get_plot_grades(nb_fname):
    nb = nbformat.read(nb_fname, 4)
    exe_nb = execute_nb(nb, op.dirname(nb_fname))
    out_cell = exe_nb.cells[-1]
    assert out_cell['cell_type'] == 'code'
    outputs = out_cell['outputs']
    assert len(outputs) == 1
    assert outputs[0]['name'] == 'stdout'
    test_outs = outputs[0]['text']
    return [float(L) for L in test_outs.splitlines()]


def main():
    args = get_args()
    for nb_fname in args.nb_fnames:
        grades = get_plot_grades(nb_fname)
        print(nb_fname)
        for g in grades:
            print(g)
        print(f'Total: {sum(grades)}')


if __name__ == '__main__':
    main()
