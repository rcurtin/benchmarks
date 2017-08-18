'''
  @file benchmark_range_search.py
  @author Marcus Edel

  Test for the Range Search scripts.
'''

import unittest

import os, sys, inspect

# Import the util path, this method even works if the path contains
# symlinks to modules.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
  os.path.split(inspect.getfile(inspect.currentframe()))[0], '../util')))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from loader import *

'''
Test the mlpack Range Search script.
'''
class RANGESEARCH_MLPACK_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = 'datasets/wine.csv'
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/mlpack/range_search.py")
    obj = getattr(module, "RANGESEARCH")
    self.instance = obj(self.dataset, verbose=self.verbose, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    # The mlpack script should set the description value.
    self.assertTrue(self.instance.description != "")
    self.assertEqual(self.instance.verbose, self.verbose)
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the 'RunMetrics' function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "max": 0.02 })
    self.assertTrue(result["Runtime"] > 0)

  '''
  Test the destructor.
  '''
  def test_Destructor(self):
    del self.instance

    clean = True
    filelist = ["gmon.out", "distances.csv", "neighbors.csv"]
    for f in filelist:
      if os.path.isfile(f):
        clean = False

    self.assertTrue(clean)

'''
Test the matlab Range Search script.
'''
class RANGESEARCH_MATLAB_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = 'datasets/wine.csv'
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/matlab/range_search.py")
    obj = getattr(module, "RANGESEARCH")
    self.instance = obj(self.dataset, verbose=self.verbose, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.verbose, self.verbose)
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the 'RunMetrics' function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "max": 0.02 })
    self.assertTrue(result["Runtime"] > 0)

if __name__ == '__main__':
  unittest.main()
