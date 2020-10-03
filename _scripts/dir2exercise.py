#!/usr/bin/env python
""" Build OKpy exercise directory from directory template.
"""

import os
import os.path as op
import sys
import shutil
from argparse import ArgumentParser
import re

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
    """ Copy exercise files from `path` to subdirectory of `out_path`

    `clean`, if True, will clean all files from the eventual output directory
    before copying.
    """
    ex_name = op.split(path)[-1]
    ex_out = op.join(out_path, ex_name)
    if op.isdir(ex_out) and clean:
        clean_path(ex_out)
    else:
        os.makedirs(ex_out)
    for dirpath, dirnames, filenames in os.walk(path):
        sub_dir = op.relpath(dirpath, path)
        dirnames[:] = [d for d in dirnames if b_e.good_fname(d)]
        filenames[:] = [f for f in filenames if b_e.good_fname(f)]
        if len(filenames) == 0:
            continue
        this_out_path = op.join(ex_out, sub_dir)
        if not op.isdir(this_out_path):
            os.makedirs(this_out_path)
        for f in filenames:
            shutil.copy(op.join(dirpath, f), this_out_path)


def find_site_config(dir_path, filenames=('course.yml', '_config.yml')):
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


def main():
    parser = ArgumentParser()
    parser.add_argument('dir', help="Directory of exercise")
    parser.add_argument('--out-path',
                        help='Output path for exercise directory'
                        '(default from course config below)'
                       )
    parser.add_argument('--no-grade', action='store_true',
                        help='If specified, do not grade solution notebook')
    parser.add_argument('--site-config',
                        help='Path to configuration file for course '
                        '(default finds {course,_config}.yml, in dir, parents)'
                       )
    args = parser.parse_args()
    if args.site_config is None:
        args.site_config = find_site_config(args.dir)
    site_dict = get_site_dict(args.site_config) if args.site_config else {}
    if args.out_path is None:
        args.out_path = site_dict['org_path']
    if args.out_path is None:
        raise RuntimeError(
            'Must specify out path or "org_path" in config file')
    process_dir(args.dir, not args.no_grade, site_dict)
    write_dir(args.dir, args.out_path)


if __name__ == '__main__':
    main()
