# Test for cutils utilities

import os.path as op
import sys
import re

import jupytext

HERE = op.realpath(op.dirname(__file__))
sys.path.append(op.join(HERE, '..'))
DATA_DIR = op.join(HERE, 'data')
THREE_GIRLS = op.join(DATA_DIR, 'three_girls')


from cutils import process_nb


HTML_COMMENT_RE = re.compile(r'<!--(.*?)-->', re.M | re.DOTALL)


def test_comment_strip():
    base_nb_root = 'three_girls_template'
    nb_in_fname = op.join(THREE_GIRLS, base_nb_root + '.Rmd')
    nb = jupytext.read(nb_in_fname)
    json = jupytext.writes(nb, fmt='ipynb')
    assert len(HTML_COMMENT_RE.findall(json)) == 4
    clear_nb = process_nb(nb_in_fname)
    json = jupytext.writes(clear_nb, fmt='ipynb')
    assert len(HTML_COMMENT_RE.findall(json)) == 0
