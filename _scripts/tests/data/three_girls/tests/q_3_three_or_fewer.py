
test = {
  'name': 'Question three_or_fewer',
  'points': 15,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # You need to set the value for 'p_3_or_fewer'
          >>> 'p_3_or_fewer' in vars()
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # You haven't changed the value for 'p_3_or_fewer'
          >>> # from its initial state (of ...)
          >>> p_3_or_fewer != ...
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          # n = 10000
          # # Take 10000 samples of 10000 trials of this problem.
          # res = np.sum(np.random.binomial(5, 0.5, (n, n)) <= 3, axis=1) / n
          # np.quantile(res, [0.001, 0.999])
          'code': r"""
          >>> 0.8 < p_3_or_fewer < 0.825
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
