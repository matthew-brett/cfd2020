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


HERE = op.dirname(__file__)
NB_DIR = op.join(HERE, 'tests', 'data', 'three_girls')
TESTS = sorted(glob(op.join(NB_DIR, 'tests', 'q*.py')))


def as_nb(fname, as_version=DEFAULT_NB_VERSION):
    if jupytext:
        return jupytext.read(fname, as_version=as_version)
    return nbf.read(fname, as_version=as_version)


def name_from_fn(test_fn):
    return op.splitext(op.basename(test_fn))[0]


def create_test_cells(tests):
    cells = []
    lines = ['_tdict = {}']
    for test_fname in tests:
        tns = f"'{name_from_fn(test_fname)}'"
        lines.append(f"_tdict[{tns}] = ok.grade({tns})['failed']")
    cells.append(nbf.new_code_cell('\n'.join(lines)))
    cells.append(nbf.new_code_cell(
        "_ = [print(f'{tn}, {_tdict[tn]}') for tn in sorted(_tdict)]"))
    return cells


def execute_nb(nb, path, timeout=240):
    storage_path = op.join(path, '.ok_storage')
    if op.exists(storage_path):
        os.unlink(storage_path)
    ep = ExecutePreprocessor(timeout=timeout)
    ep.preprocess(nb, {'metadata': {'path': path}})
    return nb


def merge_stdouts(outputs):
    merged = []
    for output in outputs:
        assert output['name'] == 'stdout'
        merged.append(output['text'])
    return ''.join(merged)


def get_test_fails(nb):
    out_cell = nb.cells[-1]
    assert out_cell['cell_type'] == 'code'
    test_outs = merge_stdouts(out_cell['outputs'])
    fails = {}
    for line in test_outs.splitlines():
        name, fail_count = line.split(',')
        fails[name] = int(fail_count)
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
    full_points = get_tests_points(tests)
    # Get grades
    grades = {}
    for tn in full_points:
        if tn in fails:
            grade = full_points[tn] if fails[tn] == 0 else 0
        else:
            grade = np.nan
        grades[tn] = grade
    return grades


def grade_nb_fname(nb_fname, wd=None):
    wd = op.dirname(nb_fname) if wd is None else wd
    nb = as_nb(nb_fname)
    return grade_nb(nb, wd)


def print_grades(grades):
    for tn in sorted(grades):
        print(f'{tn}: {grades[tn]}')
    print(f'Total: {sum(grades.values())}')


def test_get_tests_points():
    assert get_tests_points(TESTS) == {
        'q_1_no_girls': 5,
        'q_2_three_of_five': 10,
        'q_3_three_or_fewer': 15,
        'q_4_r_three_of_four': 20,
    }


def test_solution():
    solution_fname = op.join(NB_DIR, 'three_girls_template.Rmd')
    grades = grade_nb_fname(solution_fname, NB_DIR)
    assert sum(grades.values()) == 50
    solution_fname = op.join(NB_DIR, 'three_girls_solution_minus_15.Rmd')
    grades = grade_nb_fname(solution_fname, NB_DIR)
    assert sum(grades.values()) == 35


def get_args():
    parser = ArgumentParser(__doc__)
    parser.add_argument('nb_fname', nargs='+',
                        help='Path to notebook')
    parser.add_argument('--cwd',
                        help='Path in which to run notebook; '
                       'default is directory containing notebook(s)')
    return parser.parse_args()


def show_grade(nb_fname, wd):
    """ Print notebook filename and grades for each question
    """
    try:
        grades = grade_nb_fname(nb_fname, wd)
    except Exception as exc:
        print(nb_fname)
        return
    print(nb_fname)
    print_grades(grades)
    print()


def main():
    args = get_args()
    for nb_fname in args.nb_fname:
        show_grade(nb_fname, args.cwd)


if __name__ == '__main__':
    main()
