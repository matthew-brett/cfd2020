
test = {
  'name': 'Question r_three_of_four',
  'points': 20,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # You need to set the value for 'p_r3_of_4'
          >>> 'p_r3_of_4' in vars()
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # You haven't changed the value for 'p_r3_of_4'
          >>> # from its initial state (of ...)
          >>> p_r3_of_4 != ...
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          # n = 10000
          # # Take 10000 samples of 10000 trials of this problem.
          # res = np.sum(np.random.binomial(4, 0.487, (n, n)) == 3, axis=1) / n
          # np.quantile(res, [0.005, 0.995])
          'code': r"""
          >>> 0.226 < p_r3_of_4 < 0.248
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
