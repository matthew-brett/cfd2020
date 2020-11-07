#!/usr/bin/env python
""" Build OKpy exercise directory from directory template.
"""

import os
import os.path as op
import sys
import shutil
from argparse import ArgumentParser
import re
from subprocess import check_call, check_output

from jinja2 import Template

from rmdex.exerciser import (make_exercise, make_solution, write_utf8,
                             read_utf8)


HERE = op.dirname(op.realpath(__file__))
SITE_ROOT = op.realpath(op.join(HERE, '..'))
sys.path.append(HERE)

from cutils import cd, proc_config, build_url, good_fname, process_write_nb
import grade_oknb as gok


TEMPLATE_RE = re.compile(r'_template\.Rmd$')


def process_dir(path, grade=False, site_dict=None):
    site_dict = {} if site_dict is None else site_dict
    templates = [fn for fn in os.listdir(path) if TEMPLATE_RE.search(fn)]
    if len(templates) == 0:
        raise RuntimeError('No _template.Rmd in directory')
    if len(templates) > 1:
        raise RuntimeError('More than one _template.Rmd in directory')
    template_fname = op.join(path, templates[0])
    template = read_utf8(template_fname)
    if site_dict:
        template = Template(template).render(site=site_dict)
    exercise_fname = TEMPLATE_RE.sub('.Rmd', template_fname)
    write_utf8(exercise_fname, make_exercise(template))
    solution_fname = TEMPLATE_RE.sub('_solution.Rmd', template_fname)
    write_utf8(solution_fname, make_solution(template))
    process_write_nb(exercise_fname, execute=False)
    if grade:
        grades = gok.grade_nb_fname(solution_fname, path)
        gok.print_grades(grades)
        if not all(grades.values()):
            raise RuntimeError('One or more grades 0')


def clean_path(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(op.join(root, file))
        for d in dirs:
            if d != '.git':
                shutil.rmtree(op.join(root, d))
        break


def write_dir(path, out_path, clean=True):
    """ Copy exercise files from `path` to directory `out_path`

    `clean`, if True, will clean all files from the eventual output directory
    before copying.
    """
    if op.isdir(out_path) and clean:
        clean_path(out_path)
    else:
        os.makedirs(out_path)
    for dirpath, dirnames, filenames in os.walk(path):
        sub_dir = op.relpath(dirpath, path)
        dirnames[:] = [d for d in dirnames if good_fname(d)]
        filenames[:] = [f for f in filenames if good_fname(f)]
        if len(filenames) == 0:
            continue
        this_out_path = op.join(out_path, sub_dir)
        if not op.isdir(this_out_path):
            os.makedirs(this_out_path)
        for f in filenames:
            shutil.copy(op.join(dirpath, f), this_out_path)


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
    parser.add_argument('dir', help="Directory of exercise")
    parser.add_argument('--out-path',
                        help='Output path for exercise directory'
                        '(default from course config below)'
                       )
    parser.add_argument('--no-grade', action='store_true',
                        help='If specified, do not grade solution notebook')
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
    site_dict, out_path = proc_config(args.dir,
                                      args.site_config,
                                      args.out_path)
    in_dir = op.abspath(args.dir)
    process_dir(in_dir, not args.no_grade, site_dict)
    out_path = op.abspath(op.join(out_path, op.basename(in_dir)))
    write_dir(args.dir, out_path, clean=not args.no_clean)
    if args.push:
        push_dir(out_path, site_dict, args.strip)
    print(build_url(out_path, site_dict))


if __name__ == '__main__':
    main()
