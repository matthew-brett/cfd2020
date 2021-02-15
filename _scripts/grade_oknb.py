#!/usr/bin/env python
""" Print results of grading notebook
"""

import os
import os.path as op
from glob import glob
from argparse import ArgumentParser

import numpy as np

from nbconvert.preprocessors import ExecutePreprocessor
import nbformat.v4 as nbf
DEFAULT_NB_VERSION = 4

try:
    import jupytext
except ImportError:
    jupytext = None


def as_nb(fname, as_version=DEFAULT_NB_VERSION):
    if jupytext:
        return jupytext.read(fname, as_version=as_version)
    return nbf.read(fname, as_version=as_version)


def name_from_fn(test_fn):
    return op.splitext(op.basename(test_fn))[0]


def _gcc(code, cell_name):
    return nbf.new_code_cell(code, metadata={'gok_name': cell_name})


def create_test_cells(tests):
    cells = []
    cells.append(_gcc('_tdict = {}', 'dict_init'))
    for test_fname in tests:
        test_name = name_from_fn(test_fname)
        tns = f"'{test_name}'"
        cells.append(
            _gcc(f"_tdict[{tns}] = ok.grade({tns})['failed']", test_name))
    cells.append(
        _gcc("_ = [print(f'{tn}, {_tdict[tn]}') for tn in sorted(_tdict)]",
             'scores'))
    return cells


def execute_nb(nb, path, timeout=240):
    storage_path = op.join(path, '.ok_storage')
    if op.exists(storage_path):
        os.unlink(storage_path)
    ep = ExecutePreprocessor(timeout=timeout)
    ep.preprocess(nb, {'metadata': {'path': path}})
    return nb


def merge_stdouts(cell):
    merged = []
    for output in cell['outputs']:
        assert output['name'] == 'stdout'
        merged.append(output['text'])
    return ''.join(merged)


def get_gok_cells(cells):
    gok_cells = {}
    for cell in cells:
        gok_name = cell.get('metadata', {}).get('gok_name')
        if gok_name:
            assert gok_name not in gok_cells
            gok_cells[gok_name] = cell
    return gok_cells


def get_test_fails(nb):
    gok_cells = get_gok_cells(nb.cells)
    scores = gok_cells['scores']
    assert scores['cell_type'] == 'code'
    test_outs = merge_stdouts(scores)
    fails = {}
    for line in test_outs.splitlines():
        name, fail_count = line.split(',')
        output = None
        fail_count = int(fail_count)
        if fail_count:
            output = merge_stdouts(gok_cells[name])
        fails[name] = {'count': fail_count, 'output': output}
    return fails


def get_test_points(test_fname):
    ws = {}
    with open(test_fname, 'rt') as fobj:
        exec(fobj.read(), {}, ws)
    return ws['test']['points']


def get_tests_points(tests):
    return {name_from_fn(fn): get_test_points(fn) for fn in tests}


def grade_nb(nb, wd):
    # Add test cells to notebook
    test_glob = op.join(wd, 'tests', 'q*.py')
    tests = sorted(glob(test_glob))
    nb.cells += create_test_cells(tests)
    # Execute notebook
    nb = execute_nb(nb, wd)
    # Collect output from executed notebook.
    fails = get_test_fails(nb)
    # Points if all correct.
    full_points = get_tests_points(tests)
    # Get grades
    grades = {}
    messages = {}
    for tn in full_points:
        if tn not in fails:
            grades[tn] = np.nan
            continue
        if fails[tn]['count'] == 0:  # No errors
            grades[tn] = full_points[tn]
            continue
        grades[tn] = 0
        messages[tn] = fails[tn]['output']
    return grades, messages


def grade_nb_fname(nb_fname, wd=None):
    wd = op.dirname(nb_fname) if wd is None else wd
    nb = as_nb(nb_fname)
    return grade_nb(nb, wd)


def print_grades(grades):
    for tn in sorted(grades):
        print(f'{tn}: {grades[tn]}')
    print(f'Total: {sum(grades.values())}')


def print_messages(messages):
    for tn in sorted(messages):
        print(tn)
        print(messages[tn])


def get_args():
    parser = ArgumentParser(__doc__)
    parser.add_argument('nb_fname', nargs='+',
                        help='Path to notebook')
    parser.add_argument('-n', '--no-messages', action='store_true',
                        help='If set, do not show grading messages')
    parser.add_argument('--cwd',
                        help='Path in which to run notebook; '
                       'default is directory containing notebook(s)')
    return parser.parse_args()


def show_grade(nb_fname, wd, show_messages=True):
    """ Print notebook filename and grades for each question
    """
    try:
        grades, messages = grade_nb_fname(nb_fname, wd)
    except Exception as exc:
        print(nb_fname)
        print(exc)
        return
    print(nb_fname)
    print_grades(grades)
    if show_messages:
        print_messages(messages)
    print()


def main():
    args = get_args()
    for nb_fname in args.nb_fname:
        show_grade(nb_fname, args.cwd, not args.no_messages)


if __name__ == '__main__':
    main()
