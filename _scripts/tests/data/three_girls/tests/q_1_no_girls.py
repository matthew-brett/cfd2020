test = {
  'name': 'Question no_girls',
  'points': 5,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # You need to set the value for 'p_no_girls'
          >>> 'p_no_girls' in vars()
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # You haven't changed the value for 'p_no_girls'
          >>> # from its initial state (of ...)
          >>> p_no_girls != ...
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          # n = 10000
          # # Take 10000 samples of 10000 trials of this problem.
          # res = np.sum(np.random.binomial(4, 0.5, (n, n)) == 0, axis=1) / n
          # np.quantile(res, [0.001, 0.999])
          'code': r"""
          >>> 0.055 < p_no_girls < 0.071
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
