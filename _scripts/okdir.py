#!/usr/bin/env python
""" Create default OKpy directory
"""

import os
import os.path as op
import shutil
from argparse import ArgumentParser


TEMPLATE_OK = '''
{{
  "name": "{name_no_underscores}",
  "src": [
    "{name}.ipynb"
  ],
  "tests": {{
      "tests/q*.py": "ok_test"
  }},
  "protocols": [
      "file_contents",
      "grading",
      "backup"
  ]
}}
'''


def check_out_dir(out_dir, clobber=False):
    if op.exists(out_dir):
        if not clobber:
            return False
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    return True


def write_dir(out_dir):
    tests_dir = op.join(out_dir, 'tests')
    os.makedirs(tests_dir)
    with open(op.join(tests_dir, '__init__.py'), 'wt') as fobj:
        fobj.write('# Init for tests')
    name = op.basename(out_dir)
    name_no_underscores = name.replace('_', ' ')
    out_fname = op.join(out_dir, f'{name}.ok')
    with open(out_fname, 'wt') as fobj:
        fobj.write(TEMPLATE_OK.format(**locals()))
    with open(op.join(out_dir, '.gitignore'), 'wt') as fobj:
        fobj.write(f'{name}.Rmd\n')
        fobj.write(f'{name}.ipynb\n')
        fobj.write(f'{name}_solution.Rmd\n')


def main():
    parser = ArgumentParser()
    parser.add_argument('out_dir', help='Output directory for exercise')
    parser.add_argument('--clobber', action='store_true',
                        help='If set, delete existing directory')
    args = parser.parse_args()
    out_dir = args.out_dir
    if not check_out_dir(out_dir, args.clobber):
        raise RuntimeError(
            f'Directory {out_dir} already exists, --clobber not set')
    write_dir(out_dir)


if __name__ == '__main__':
    main()
