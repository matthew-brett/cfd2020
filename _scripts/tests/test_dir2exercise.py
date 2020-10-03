# Test for dir2exercise utilities

import os.path as op
import sys
import shutil
from pathlib import Path

HERE = op.realpath(op.dirname(__file__))
sys.path.append(op.join(HERE, '..'))
DATA_DIR = op.join(HERE, 'data')
THREE_GIRLS = op.join(DATA_DIR, 'three_girls')


from tempfile import TemporaryDirectory
from dir2exercise import (find_site_config, get_site_dict, process_dir,
                          write_dir)

import pytest


def test_find_site_config():
    rp = op.realpath
    with TemporaryDirectory() as tmpdir:
        assert find_site_config(tmpdir) is None
    # Finding _config.yml in main repo directory.
    assert rp(find_site_config('.')) == rp(op.join('..', '_config.yml'))
    # Check prefer course.yml to _config.yml
    exp_fn = rp(op.join(DATA_DIR, 'course.yml'))
    assert rp(find_site_config(DATA_DIR)) == exp_fn
    # Starting at an empty directory finds one dir below.
    assert rp(find_site_config(op.join(DATA_DIR, 'empty_dir'))) == exp_fn
    # Single config in directory.
    ed_pth = op.join(DATA_DIR, 'exercise_dir')
    assert rp(find_site_config(ed_pth)) == rp(op.join(ed_pth, '_config.yml'))


def test_get_site_dict():
    # Check prefer course.yml to _config.yml
    fn1 = op.realpath(op.join(DATA_DIR, 'course.yml'))
    assert get_site_dict(fn1) == {'baseurl': 'https://foo.github.com/bar',
                                  'baz': 'bong'}
    fn2 = op.realpath(op.join(DATA_DIR, '_config.yml'))
    assert (get_site_dict(fn2)['baseurl'] ==
            'https://matthew-brett.github.io/cfd2019')


def test_smoke_and_fails():
    base_nb_root = 'three_girls'
    with TemporaryDirectory() as tmpdir:
        tmp_3g = op.join(tmpdir, 'three_girls')
        shutil.copytree(THREE_GIRLS, tmp_3g)
        tmp_nb_in = op.join(tmp_3g, base_nb_root + '_template.Rmd')
        tmp_ex_out = op.join(tmp_3g, base_nb_root + '.ipynb')
        assert op.isfile(tmp_nb_in)
        assert not op.isfile(tmp_ex_out)
        process_dir(tmp_3g, grade=True)
        assert op.isfile(tmp_ex_out)
        tmp_out = op.join(tmpdir, 'out_path')
        write_dir(tmp_3g, tmp_out)
        ex_out = op.join(tmp_out, 'three_girls')
        assert op.isdir(ex_out)
        assert op.isdir(op.join(ex_out, 'tests'))
        all_files = [str(p) for p in Path(ex_out).rglob('*')]
        z_list = sorted(op.relpath(f, tmp_out) for f in all_files)
        assert z_list == [
            'three_girls/tests',
            'three_girls/tests/__init__.py',
            'three_girls/tests/q_1_no_girls.py',
            'three_girls/tests/q_2_three_of_five.py',
            'three_girls/tests/q_3_three_or_fewer.py',
            'three_girls/tests/q_4_r_three_of_four.py',
            'three_girls/three_girls.ipynb',
            'three_girls/three_girls.ok']
        # Test failing exercise causes error.
        bad_ex_fname = op.join(tmp_3g, 'tests', 'q_5.py')
        with open(bad_ex_fname, 'wt') as fobj:
            fobj.write('''
test = {
  'name': 'Question 5',
  'points': 20,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> False
          True
          """,
          'hidden': False,
          'locked': False
        },
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}''')
        with pytest.raises(RuntimeError):
            process_dir(tmp_3g, grade=True)
