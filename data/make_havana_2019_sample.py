""" Make one random sample from Havana mathematics results.
"""

import numpy as np
import pandas as pd

df = pd.read_csv('havana_math_2019.csv').dropna()

# By exploring seeds I came to:
np.random.seed(101)

sample = df.sample(50, replace=False)
print('Mean', sample['mark'].mean())

sample.to_csv('havana_math_2019_sample.csv', index=None)
