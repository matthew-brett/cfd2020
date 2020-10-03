#!/usr/bin/env python
""" Check OK marks add up to given total
"""

import os.path as op
from argparse import ArgumentParser
from glob import glob


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('exercise_path',
                        help='Path to exercise')
    return parser


def marks_for(test_fname):
    env = {}
    with open(test_fname, 'rt') as fobj:
        code = fobj.read()
    exec(code, env)
    return env['test']['points']


def mark_total(path):
    search_glob = op.join(path, 'tests', 'q*.py')
    test_files = sorted(glob(search_glob))
    if len(test_files) == 0:
        raise RuntimeError(f'Found no test files with {search_glob}')
    total = 0
    for test_fname in test_files:
        total += marks_for(test_fname)
    return total


def main():
    args = get_parser().parse_args()
    print(mark_total(args.exercise_path))


if __name__ == '__main__':
    main()
