#!/usr/bin/env python2.7

import unittest

if __name__ == "__main__":
  suite = unittest.TestSuite()
  all_tests = unittest.defaultTestLoader.discover('', pattern='*_tests.py')
  for all_test_suite in all_tests:
    for test_suite in all_test_suite:
      suite.addTests(test_suite)

  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)