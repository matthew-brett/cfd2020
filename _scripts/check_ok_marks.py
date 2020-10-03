#!/usr/bin/env python
""" Check that marks noted in Rmd correspond to OKpy points
"""

import os.path as op
from glob import glob
import re
from argparse import ArgumentParser

from rnbgrader import loads
from rmdex.exerciser import read_utf8, question_chunks, get_marks


GRADE_RE = re.compile(r"""\.\s*grade\s*\(\s*['"](.*?)['"]\s*\)""")

# For tests
HERE = op.dirname(__file__)
NB_DIR = op.join(HERE, 'tests', 'data', 'three_girls')
TESTS = sorted(glob(op.join(NB_DIR, 'tests', 'q*.py')))


def ok_test_name(code):
    match = GRADE_RE.search(code)
    return None if match is None else match.groups()[0]


def load_test(test_fname):
    ns = {}
    with open(test_fname, 'rt') as fobj:
        exec(fobj.read(), ns)
    assert 'test' in ns
    return ns['test']


def check_points(rmd_fname, tests_path=None):
    if tests_path is None:
        tests_path = op.join(op.dirname(rmd_fname), 'tests')
    # Find chunks
    nb = loads(read_utf8(rmd_fname))
    chunks = nb.chunks
    # Identify questions
    questions = question_chunks(nb)
    # Detect mismatch
    mismatch = {}
    missing = []
    total = 0
    for question in questions:
        # Get marks allocated
        marks, out_of, r_total = [float(v) for v in get_marks(question.code)]
        total += marks
        assert total == r_total
        # Find following ok.grade chunk, if present.
        q_i = chunks.index(question)
        assert q_i >= 0
        test_name = ok_test_name(chunks[q_i + 1].code)
        if test_name is None:
            missing.append(chunks[q_i].code)
            continue
        # Load corresponding test
        test = load_test(op.join(tests_path, test_name + '.py'))
        # Check points same as marks allocated
        if test['points'] != marks:
            mismatch[test_name] = (test['points'], marks)
    return total, missing, mismatch


def test_ok_test_name():
    assert ok_test_name('ok.grade("foo")') == 'foo'
    assert ok_test_name('# A comment\nnb.grade("funny file")') == 'funny file'
    assert ok_test_name('# Three\nnb. grade (  "funny file" )  # Comments\n'
                        '# Here') == 'funny file'


def test_smoke():
    rmd_fname = op.join(NB_DIR, 'three_girls_template.Rmd')
    total, missing, mismatch = check_points(rmd_fname)
    assert missing, mismatch == ([], {})


def get_args():
    parser = ArgumentParser(__doc__)
    parser.add_argument('rmd_fname', help='Path to Rmd notebook')
    parser.add_argument('--tests-path',
                        help='Path to notebook test directory'
                       'default is "tests" directory in path of notebook(s)')
    args = parser.parse_args()
    if args.tests_path is None:
        args.tests_path = op.join(op.dirname(args.rmd_fname), 'tests')
    return args


def main():
    args = get_args()
    total, missing, mismatch = check_points(args.rmd_fname, args.tests_path)
    for miss in missing:
        print(f'Question chunk without ok test\n{miss}')
    if missing:
        print()
    for test_name, (in_test, in_file) in mismatch.items():
        print(f'Test {test_name} mismatch: {in_test} in test file; '
              f'{in_file} in notebook')
    print(f'Total: {total}')


if __name__ == '__main__':
    main()
