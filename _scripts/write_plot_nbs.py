#!/usr/bin/env python
""" Make notebooks for grading plots
"""

import os
import os.path as op
from argparse import ArgumentParser
import base64
from urllib.parse import quote as urlq

import nbformat
import nbformat.v4 as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import jupytext

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


def get_plot(cell):
    if not cell['cell_type'] == 'code':
        return None
    for output in cell['outputs']:
        if output['output_type'] != 'display_data':
            continue
        if not 'data' in output:
            continue
        if not 'image/png' in output['data']:
            continue
        return base64.b64decode(output['data']['image/png'])
    return None


def write_plot_nb(nb_fname, out_path=None, exe_path=None):
    nb_dir = op.dirname(nb_fname)
    nb_base = op.splitext(op.basename(nb_fname))[0]
    out_path = nb_dir if out_path is None else out_path
    exe_path = nb_dir if exe_path is None else exe_path
    # Execute
    nb = jupytext.read(nb_fname)
    ex_nb = execute_nb(nb, exe_path)
    # Write plots as maybe SVG
    cell_plots = [get_plot(c) for c in ex_nb['cells']]
    plot_fnames = []
    for i, p in enumerate(cell_plots):
        if p is None:
            continue
        out_fname = op.join(out_path, f'{nb_base}_plot_{i:02d}.png')
        with open(out_fname, 'wb') as fobj:
            fobj.write(p)
        plot_fnames.append(out_fname)

    # Make, write new notebook.
    plot_nb = nbf.new_notebook()
    cells = plot_nb['cells']
    ncc = nbf.new_code_cell
    cells.append(ncc('plot_marks = []'))
    # Two cells per plot.
    # First cell displays plot
    # Second has 'plot_marks.append(None)`
    for plot_fname in plot_fnames:
        img_url = urlq(op.basename(plot_fname))
        cells.append(nbf.new_markdown_cell(f'![]({img_url})'))
        cells.append(ncc('plot_marks.append(None)'))
    cells.append(ncc('assert None not in plot_marks'))
    cells.append(ncc('for mark in plot_marks:\n    print(mark)'))
    out_fname = op.join(out_path, f'{nb_base}_plots.ipynb')
    nbformat.write(plot_nb, out_fname)


def main():
    args = get_args()
    if args.out_path and not op.isdir(args.out_path):
        os.makedirs(args.out_path)
    for nb_fname in args.nb_fnames:
        write_plot_nb(nb_fname, args.out_path)


if __name__ == '__main__':
    main()
