""" Test grade_oknb
"""

import os.path as op
from glob import glob

from grade_oknb import get_tests_points, grade_nb_fname

HERE = op.dirname(__file__)
NB_DIR = op.join(HERE, 'data', 'three_girls')
TESTS = sorted(glob(op.join(NB_DIR, 'tests', 'q*.py')))


def test_get_tests_points():
    assert get_tests_points(TESTS) == {
        'q_1_no_girls': 5,
        'q_2_three_of_five': 10,
        'q_3_three_or_fewer': 15,
        'q_4_r_three_of_four': 20,
    }


def test_solution():
    solution_fname = op.join(NB_DIR, 'three_girls_template.Rmd')
    grades, messages = grade_nb_fname(solution_fname, NB_DIR)
    assert sum(grades.values()) == 50
    solution_fname = op.join(NB_DIR, 'three_girls_solution_minus_15.Rmd')
    grades, messages = grade_nb_fname(solution_fname, NB_DIR)
    assert sum(grades.values()) == 35
