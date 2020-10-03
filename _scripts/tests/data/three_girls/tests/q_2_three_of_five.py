test = {
  'name': 'Question no_girls',
  'points': 10,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # You need to set the value for 'p_3_of_5'
          >>> 'p_3_of_5' in vars()
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # You haven't changed the value for 'p_3_of_5'
          >>> # from its initial state (of ...)
          >>> p_3_of_5 != ...
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          # n = 10000
          # # Take 10000 samples of 10000 trials of this problem.
          # res = np.sum(np.random.binomial(5, 0.5, (n, n)) == 3, axis=1) / n
          # np.quantile(res, [0.001, 0.999])
          'code': r"""
          >>> 0.297 < p_3_of_5 < 0.327
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
