""" Course utility functions
"""

import os
import os.path as op
from glob import iglob
import shutil
import re
import urllib.parse
from contextlib import contextmanager

import yaml

import nbformat
import jupytext
from nbconvert.preprocessors import ExecutePreprocessor


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


def proc_config(in_path=None, site_config=None, out_path=None):
    if site_config is None:
       site_config = find_site_config(in_path)
    site_dict = get_site_dict(site_config) if site_config else {}
    if out_path is None:
        out_path = site_dict.get('org_path')
    if out_path is None:
        raise RuntimeError(
            'Must specify out path or "org_path" in config file\n'
            f'Config file is {site_config}'
        )
    return site_dict, out_path


def find_notebook(path):
    ipynbs = list(iglob(op.join(path, '*.ipynb')))
    rmds = list(iglob(op.join(path, '*.Rmd')))
    both = ipynbs + rmds
    if len(both) == 0:
        raise RuntimeError(f'Cannot find notebook files in {path}')
    if len(both) == 1:
        return both[0]
    if len(ipynbs) == 1 and len(rmds) == 1:
        # Look for one pair of matching ipynb and Rmd files.
        ipynb, rmd = both
        if op.splitext(ipynb)[0] == op.splitext(rmd)[0]:
            return ipynb
    fns = '\n'.join(both)
    raise RuntimeError(f'Too many notebook files in {path}:\n{fns}')


def build_url(fn, site_dict):
    if op.isdir(fn):
        fn = find_notebook(fn)
    nb_path, nb_basen = op.split(op.abspath(fn))
    root, ext = op.splitext(nb_basen)
    if ext not in ('.Rmd', '.ipynb'):
        raise RuntimeError(f'Is {fn} really a notebook?')
    repo = op.basename(nb_path)
    s_d = site_dict
    repo_url = urllib.parse.quote(
        f'{s_d["git_root"]}/{s_d["org_name"]}/{repo}')
    hub_suffix = 'hub/user-redirect/git-pull?repo='
    return f'{site_dict["jh_root"]}/{hub_suffix}{repo_url}&subPath={nb_basen}'


def execute_nb(nb, path, nbargs=None):
    nbargs = {} if nbargs is None else nbargs
    ep = ExecutePreprocessor(**nbargs)
    ep.preprocess(nb, {'metadata': {'path': path}})
    return nb


def clear_outputs(nb):
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            cell['outputs'] = []
    return nb


def path_of(fname):
    return op.split(op.abspath(fname))[0]


def clear_directory(fname):
    path = path_of(fname)
    for basename in ('.ok_storage',):
        pth = op.join(path, basename)
        if op.exists(pth):
            os.unlink(pth)
    pycache = op.join(path, 'tests', '__pycache__')
    if op.isdir(pycache):
        shutil.rmtree(pycache)


def ipynb_fname(fname):
    froot, ext = op.splitext(fname)
    return froot + '.ipynb'


HTML_COMMENT_RE = re.compile(r'<!--(.*?)-->', re.M | re.DOTALL)


def clear_md_comments(nb):
    """ Strip HTML comments using regexp
    """
    for cell in nb['cells']:
        if cell['cell_type'] != 'markdown':
            continue
        cell['source'] = HTML_COMMENT_RE.sub('', cell['source'])
    return nb


def write_nb(nb, fname):
    with open(fname, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)



def process_nb(fname, execute=False):
    clear_directory(fname)
    nb = jupytext.read(fname)
    if execute:
        nb = execute_nb(nb, path_of(fname))
    nb = clear_outputs(nb)
    nb = clear_md_comments(nb)
    write_nb(nb, ipynb_fname(fname))
