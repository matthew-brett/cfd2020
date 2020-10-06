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
from contextlib import contextmanager

import yaml
from jinja2 import Template

from rmdex.exerciser import (make_exercise, make_solution, write_utf8,
                             read_utf8)


HERE = op.dirname(op.realpath(__file__))
SITE_ROOT = op.realpath(op.join(HERE, '..'))
sys.path.append(HERE)

import build_exercise as b_e
import grade_oknb as gok


TEMPLATE_RE = re.compile('_template\.Rmd$')


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def get_site_dict(site_config):
    with open(site_config, 'r') as ff:
        site = yaml.load(ff.read(), Loader=yaml.SafeLoader)
    # Get full baseurl from _config.yml format.
    if not site['baseurl'].startswith('http') and 'url' in site:
        site['baseurl'] = site['url'] + site['baseurl']
    for path_key in ('org_path',):
        if path_key in site:
            site[path_key] = op.expanduser(site[path_key])
    return site


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
    b_e.process_nb(exercise_fname, execute=False)
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
        dirnames[:] = [d for d in dirnames if b_e.good_fname(d)]
        filenames[:] = [f for f in filenames if b_e.good_fname(f)]
        if len(filenames) == 0:
            continue
        this_out_path = op.join(out_path, sub_dir)
        if not op.isdir(this_out_path):
            os.makedirs(this_out_path)
        for f in filenames:
            shutil.copy(op.join(dirpath, f), this_out_path)


def find_site_config(dir_path, filenames=('course.yml',
                                          '_course.yml',
                                          '_config.yml')):
    """ Iterate to parents to locate one of filenames specified in `filenames`.
    """
    dir_path = op.realpath(dir_path)
    while True:
        for fn in filenames:
            pth = op.join(dir_path, fn)
            if op.isfile(pth):
                return pth
        prev_dir_path = dir_path
        dir_path = op.realpath(op.join(dir_path, '..'))
        if (dir_path == prev_dir_path or  # We hit root.
            not prev_dir_path.startswith(dir_path)): # We hit fs boundary.
            break
    return None


def push_dir(path, site_dict):
    with cd(path):
        ex_name = op.basename(path)
        if not op.isdir('.git'):
            check_call(['git', 'init'])
            check_call(['hub', 'create',
                        f"{site_dict['org_name']}/{ex_name}"])
        check_call(['git', 'add', '.'])
        if len(check_output(['git', 'diff', '--staged'])) == 0:
            print('No changes to commit')
            return
        check_call(['git', 'commit', '-m', 'Update from template'])
        check_call(['git', 'push', 'origin', 'master'])


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
    parser.add_argument('--no-clean', action='store_true',
                        help='If specified, do not delete existing exercise '
                             'files in output directory')
    parser.add_argument('--site-config',
                        help='Path to configuration file for course '
                        '(default finds {course,_config}.yml, in dir, parents)'
                       )
    args = parser.parse_args()
    if args.site_config is None:
        args.site_config = find_site_config(args.dir)
    site_dict = get_site_dict(args.site_config) if args.site_config else {}
    if args.out_path is None:
        args.out_path = site_dict.get('org_path')
    if args.out_path is None:
        raise RuntimeError(
            'Must specify out path or "org_path" in config file\n'
            f'Config file is {args.site_config}'
        )
    in_dir = op.abspath(args.dir)
    process_dir(in_dir, not args.no_grade, site_dict)
    out_path = op.abspath(op.join(args.out_path, op.basename(in_dir)))
    write_dir(args.dir, out_path, clean=not args.no_clean)
    if args.push:
        push_dir(out_path, site_dict)


if __name__ == '__main__':
    main()
