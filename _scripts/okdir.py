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

TEMPLATE_TEMPLATE = """\
---
jupyter:
  jupytext:
    notebook_metadata_filter: all,-language_info
    split_at_heading: true
    text_representation:
      extension: .Rmd
      format_name: rmarkdown
      format_version: '1.1'
      jupytext_version: 1.2.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# {name}

```{{python}}
# Don't change this cell; just run it.
import numpy as np  # The array library.

# The OKpy testing system.
from client.api.notebook import Notebook
ok = Notebook('{name}.ok')
```

## Done.

Congratulations, you're done with the assignment!  Be sure to:

- **run all the tests** (the next cell has a shortcut for that).
- **Save and Checkpoint** from the `File` menu.

```{{python}}
# For your convenience, you can run this cell to run all the tests at once!
import os
_ = [ok.grade(q[:-3]) for q in os.listdir("tests") if q.startswith('q')]
```
"""


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
        for ext in ('Rmd', 'ipynb'):
            fobj.write(f'{name}.{ext}\n')
            fobj.write(f'{name}_solution.{ext}\n')
    with open(op.join(out_dir, f'{name}_template.Rmd'), 'wt') as fobj:
        fobj.write(TEMPLATE_TEMPLATE.format(**locals()))


def main():
    parser = ArgumentParser()
    parser.add_argument('out_dir', help='Output directory for exercise')
    parser.add_argument('--clobber', action='store_true',
                        help='If set, delete existing directory')
    args = parser.parse_args()
    out_dir = op.abspath(args.out_dir)
    if not check_out_dir(out_dir, args.clobber):
        raise RuntimeError(
            f'Directory {out_dir} already exists, --clobber not set')
    write_dir(out_dir)


if __name__ == '__main__':
    main()
