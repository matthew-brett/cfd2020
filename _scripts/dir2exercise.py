#!/usr/bin/env python
""" Build OKpy exercise directory from directory template.
"""

import os
import os.path as op
import sys
import shutil
from argparse import ArgumentParser
from subprocess import check_call, check_output


HERE = op.dirname(op.realpath(__file__))
SITE_ROOT = op.realpath(op.join(HERE, '..'))
sys.path.append(HERE)

from cutils import (cd, proc_config, build_url, check_repo, process_dir,
                    write_exercise_ipynb, grade_path, write_dir)


def strip_repo_at(path):
    with cd(path):
        origin_url = check_output(
            ['git', 'remote', 'get-url', 'origin'], text=True).strip()
        if len(origin_url) == 0:
            raise RuntimeError('Could not find origin URL')
        shutil.rmtree('.git')
        check_call(['git', 'init'])
        check_call(['git', 'remote', 'add', 'origin', origin_url])


def push_dir(path, site_dict, strip=False):
    with cd(path):
        ex_name = op.basename(path)
        has_history = op.isdir('.git')
        if has_history:
            if strip:
                strip_repo_at('.')
        else:  # No history
            check_call(['git', 'init'])
            check_call(['hub', 'create',
                        f"{site_dict['org_name']}/{ex_name}"])
        check_call(['git', 'add', '.'])
        if len(check_output(['git', 'diff', '--staged'])) == 0:
            print('No changes to commit')
            return
        check_call(['git', 'commit', '-m', 'Update from template'])
        check_call(['git', 'push', 'origin', 'master'] +
                   (['--force'] if strip else []))


def main():
    parser = ArgumentParser()
    parser.add_argument('dir', help="Directory of exercise", nargs='?',
                        default=os.getcwd())
    parser.add_argument('--out-path',
                        help='Output path for exercise directory'
                        '(default from course config below)'
                       )
    parser.add_argument('--no-grade', action='store_true',
                        help='If specified, do not grade solution notebook')
    parser.add_argument('--rmd', action='store_true',
                        help='If specified, use Rmd exercise file rather than '
                        'ipynb (for now, implies --no-grade)')
    parser.add_argument('--push', action='store_true',
                        help='If specified, push exercise to remote')
    parser.add_argument('--strip', action='store_true',
                        help='If specified, strip exercise history')
    parser.add_argument('--no-clean', action='store_true',
                        help='If specified, do not delete existing exercise '
                             'files in output directory')
    parser.add_argument('--site-config',
                        help='Path to configuration file for course '
                        '(default finds {course,_config}.yml, in dir, parents)'
                       )
    args = parser.parse_args()
    if args.rmd:  # We can't grade rmds, thus far.
        args.no_grade = True
    site_dict, out_path = proc_config(args.dir,
                                      args.site_config,
                                      args.out_path)
    in_dir = op.abspath(args.dir)
    check_repo(in_dir, not args.rmd)
    process_dir(in_dir, site_dict=site_dict)
    if not args.rmd:
        write_exercise_ipynb(in_dir)
    if not args.no_grade:
        grade_path(in_dir)
    out_path = op.abspath(op.join(out_path, op.basename(in_dir)))
    write_dir(args.dir, out_path, clean=not args.no_clean,
              exclude_exts=() if args.rmd else ('.Rmd',))
    if args.push:
        push_dir(out_path, site_dict, args.strip)
    print(build_url(out_path, site_dict))


if __name__ == '__main__':
    main()
