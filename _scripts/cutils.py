""" Course utility functions
"""

import os
import os.path as op
from glob import iglob
import urllib.parse
from contextlib import contextmanager

import yaml


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
    repo_url = urllib.parse.quote(f'{site_dict["git_root"]}/{repo}')
    hub_suffix = 'hub/user-redirect/git-pull?repo='
    return f'{site_dict["jh_root"]}/{hub_suffix}{repo_url}&subPath={nb_basen}'
