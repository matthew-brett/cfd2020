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
from cutils import find_site_config, get_site_dict
from dir2exercise import (process_dir, write_exercise_ipynb, grade_path,
                          write_dir)

import pytest


def test_find_site_config():
    rp = op.realpath
    eg_config = rp(op.join(DATA_DIR, 'course.yml'))
    with TemporaryDirectory() as tmpdir:
        assert find_site_config(tmpdir) is None
        # Check preference order
        for fn in ('course.yml', '_course.yml', '_config.yml')[::-1]:
            config_path = rp(op.join(tmpdir, fn))
            shutil.copy(eg_config, config_path)
            assert rp(find_site_config(tmpdir)) == config_path
    # Check prefer course.yml to _config.yml
    assert rp(find_site_config(DATA_DIR)) == eg_config
    # Starting at an empty directory finds one dir below.
    assert rp(find_site_config(op.join(DATA_DIR, 'empty_dir'))) == eg_config
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
        process_dir(tmp_3g)
        assert not op.isfile(tmp_ex_out)
        write_exercise_ipynb(tmp_3g)
        assert op.isfile(tmp_ex_out)
        grade_path(tmp_3g)
        tmp_out = op.join(tmpdir, 'out_path')
        write_dir(tmp_3g, tmp_out)
        assert op.isdir(tmp_out)
        assert op.isdir(op.join(tmp_out, 'tests'))
        all_files = [str(p) for p in Path(tmp_out).rglob('*')]
        z_list = sorted(op.relpath(f, tmp_out) for f in all_files)
        assert z_list == [
            'tests',
            'tests/__init__.py',
            'tests/q_1_no_girls.py',
            'tests/q_2_three_of_five.py',
            'tests/q_3_three_or_fewer.py',
            'tests/q_4_r_three_of_four.py',
            'three_girls.ipynb',
            'three_girls.ok']
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
        process_dir(tmp_3g)
        write_exercise_ipynb(tmp_3g)
        with pytest.raises(RuntimeError):
            grade_path(tmp_3g)
