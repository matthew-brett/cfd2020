# Test for build_exercise utilities

import os.path as op
import sys
import shutil
from zipfile import ZipFile

HERE = op.realpath(op.dirname(__file__))
sys.path.append(op.join(HERE, '..'))
DATA_DIR = op.join(HERE, 'data')
THREE_GIRLS = op.join(DATA_DIR, 'three_girls')


from tempfile import TemporaryDirectory
from build_exercise import process_nb, pack_exercise


def test_smoke():
    base_nb_root = 'three_girls_template'
    with TemporaryDirectory() as tmpdir:
        tmp_3g = op.join(tmpdir, 'three_girls')
        shutil.copytree(THREE_GIRLS, tmp_3g)
        tmp_nb_in = op.join(tmp_3g, base_nb_root + '.Rmd')
        tmp_nb_out = op.join(tmp_3g, base_nb_root + '.ipynb')
        assert op.isfile(tmp_nb_in)
        assert not op.isfile(tmp_nb_out)
        process_nb(tmp_nb_in)
        assert op.isfile(tmp_nb_out)
        pack_exercise(tmp_nb_in, tmpdir)
        zip_fname = op.join(tmpdir, 'three_girls.zip')
        with ZipFile(zip_fname, 'r') as zip_obj:
            z_list = sorted(zip_obj.namelist())
        # Template correctly excluded by matching rule.
        assert z_list == [
            'three_girls/',
            'three_girls/tests/',
            'three_girls/tests/__init__.py',
            'three_girls/tests/q_1_no_girls.py',
            'three_girls/tests/q_2_three_of_five.py',
            'three_girls/tests/q_3_three_or_fewer.py',
            'three_girls/tests/q_4_r_three_of_four.py',
            'three_girls/three_girls.ok']
