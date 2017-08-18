'''
  @file benchmark_nmf.py
  @author Marcus Edel

  Test for the Non-negative Matrix Factorization scripts.
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
Test the mlpack Non-negative Matrix Factorization script.
'''
class NMF_MLPACK_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = 'datasets/wine.csv'
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/mlpack/nmf.py")
    obj = getattr(module, "NMF")
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
    result = self.instance.RunMetrics({ "rank": 6, "update_rules": "multdist" })
    self.assertTrue(result["Runtime"] > 0)

  '''
  Test the destructor.
  '''
  def test_Destructor(self):
    del self.instance

    clean = True
    filelist = ["gmon.out", "W.csv", "H.csv"]
    for f in filelist:
      if os.path.isfile(f):
        clean = False

    self.assertTrue(clean)

'''
Test the scikit Non-negative Matrix Factorization script.
'''
class NMF_SCIKIT_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = 'datasets/wine.csv'
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/scikit/nmf.py")
    obj = getattr(module, "NMF")
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
    result = self.instance.RunMetrics({ "rank": 6 })
    self.assertTrue(result["Runtime"] > 0)

'''
Test the matlab Non-negative Matrix Factorization script.
'''
class NMF_MATLAB_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = 'datasets/wine.csv'
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/matlab/nmf.py")
    obj = getattr(module, "NMF")
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
    result = self.instance.RunMetrics({ "rank": 6, "update_rules": "multdist" })
    self.assertTrue(result["Runtime"] > 0)

if __name__ == '__main__':
  unittest.main()
