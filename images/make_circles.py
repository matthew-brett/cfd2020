""" Generates PNGs for permutation_ideas page
"""

import os.path as op
from itertools import cycle
from collections import Counter
from numpy.random import permutation, seed

import numpy as np
import pandas as pd

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


HERE = op.dirname(__file__)


class BallShower:

    def __init__(self, rows, cols,
                 ball_txt_fontsize=16,
                 ball_txt_color='white'):
        self.rows = rows
        self.cols = cols
        self.ball_txt_fontsize=ball_txt_fontsize
        self.ball_txt_color=ball_txt_color
        diameter = 1 / self.rows
        self.radius = diameter / 2
        self.centers_x = np.arange(self.rows) * diameter + self.radius
        self.centers_y = (np.arange(self.cols) * diameter + self.radius)[::-1]
        self._ax = None
        self._balls = []

    def ball_center(self, ball_no):
        ball_row = ball_no // self.cols
        ball_col = ball_no % self.cols
        return self.centers_x[ball_col], self.centers_y[ball_row]

    def ball_edges(self, ball_no):
        c_x, c_y = self.ball_center(ball_no)
        r = self.radius
        return (((c_x - r,  c_x - r), (c_y - r, c_y + r)),
                ((c_x - r,  c_x + r), (c_y + r, c_y + r)),
                ((c_x - r,  c_x + r), (c_y - r, c_y - r)),
                ((c_x + r,  c_x + r), (c_y - r, c_y + r)),
               )

    def _round_edge(self, edge, precision):
        return tuple(tuple(np.round(cs, precision)) for cs in edge)

    def bounding_edges(self, ball_nos, precision=6):
        all_edges = sum([self.ball_edges(b) for b in ball_nos], ())
        all_edges = [self._round_edge(es, precision) for es in all_edges]
        edge_counts = Counter(all_edges)
        return tuple(e for e, c in edge_counts.items() if c == 1)

    def ball_figure(self, balls, ax=None):
        if ax is None:
            plt.figure()
            ax = plt.gca()
        for ball_no, ball in enumerate(balls):
            c_x, c_y = self.ball_center(ball_no)
            bugs, color = balls[ball_no]
            p = mpatches.Circle((c_x, c_y), self.radius, color=color)
            plt.text(c_x, c_y,
                     bugs,
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize=self.ball_txt_fontsize,
                     color=self.ball_txt_color)
            ax.add_patch(p)
        ax.axis('off')
        self._balls = balls
        self._ax = ax

    def plot_bb(self, ball_nos, color='red', linewidth=4):
        for xs, ys in self.bounding_edges(ball_nos):
            self._ax.plot(xs, ys, color=color, linewidth=linewidth)

    def mean_for(self, ball_nos, plot_ball, color='black'):
        values = [self._balls[i][0] for i in ball_nos]
        mu = np.mean(values)
        c_x, c_y = self.ball_center(plot_ball)
        self._ax.text(c_x, c_y,
                      'mean = {:.2f}'.format(mu),
                      horizontalalignment='center',
                      verticalalignment='center',
                      fontsize=self.ball_txt_fontsize,
                      color=color)
        return mu


mosquitoes = pd.read_csv(op.join('..', 'data', 'mosquito_beer.csv'))
afters = mosquitoes[mosquitoes['test'] == 'after']
beers = afters[afters['group'] == 'beer']
waters = afters[afters['group'] == 'water']
beer_activated = list(beers['activated'])
n_beer = len(beer_activated)
beer_balls = list(zip(beer_activated, cycle(['#cc9900'])))

water_activated = list(waters['activated'])
water_balls = list(zip(water_activated, cycle(['#33bbff'])))
balls = np.array(beer_balls + water_balls, dtype=object)
n_balls = len(balls)

bshower = BallShower(7, 7)
beer_nos = range(n_beer)
water_nos = range(n_beer, n_balls)
empty_ball = n_balls + 2

bshower.ball_figure(balls)
plt.savefig('just_balls.png')

bshower.plot_bb(beer_nos)
beer_m = bshower.mean_for(beer_nos, empty_ball)
plt.savefig('beer_mean.png')

bshower.ball_figure(balls)
bshower.plot_bb(water_nos)
water_m = bshower.mean_for(water_nos, empty_ball)
plt.savefig('water_mean.png')
print(f'Actual difference: {beer_m - water_m:0.2f}')

seed(42)

for i in range(2):
    shuffled = permutation(balls)
    bshower.ball_figure(shuffled)
    plt.savefig(f'fake_balls{i}.png')
    bshower.plot_bb(beer_nos)
    fb_m = bshower.mean_for(beer_nos, empty_ball)
    plt.savefig(f'fake_beer_mean{i}.png')

    bshower.ball_figure(shuffled)
    bshower.plot_bb(water_nos)
    fw_m = bshower.mean_for(water_nos, empty_ball)
    plt.savefig(f'fake_water_mean{i}.png')

    print(f'Fake difference {i}: {fb_m - fw_m:0.2f}')
