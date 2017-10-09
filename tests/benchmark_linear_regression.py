'''
  @file benchmark_linear_regression.py
  @author Marcus Edel

  Test for the Simple Linear Regression Prediction scripts.
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
Test the mlpack Simple Linear Regression Prediction script.
'''
class LinearRegression_MLPACK_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/diabetes.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/mlpack/linear_regression.py")
    obj = getattr(module, "LinearRegression")
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
    result = self.instance.RunMetrics({})
    self.assertTrue(result["Runtime"] > 0)

  '''
  Test the destructor.
  '''
  def test_Destructor(self):
    del self.instance

    clean = True
    filelist = ["gmon.out", "parameters.csv"]
    for f in filelist:
      if os.path.isfile(f):
        clean = False

    self.assertTrue(clean)

'''
Test the weka Simple Linear Regression Prediction script.
'''
class LinearRegression_WEKA_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_test.arff']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/weka/linear_regression.py")
    obj = getattr(module, "LinearRegression")
    self.instance = obj(self.dataset, verbose=self.verbose, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.verbose, self.verbose)
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

'''
Test the shogun Simple Linear Regression Prediction script.
'''
class LinearRegression_SHOGUN_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/diabetes.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/shogun/linear_regression.py")
    obj = getattr(module, "LinearRegression")
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
    result = self.instance.RunMetrics({})
    self.assertTrue(result["Runtime"] > 0)

'''
Test the scikit Simple Linear Regression Prediction script.
'''
class LinearRegression_SCIKIT_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv', 'datasets/iris_labels.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/scikit/linear_regression.py")
    obj = getattr(module, "LinearRegression")
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
    result = self.instance.RunMetrics({})
    self.assertTrue(result["Runtime"] > 0)
    self.assertTrue(result["Simple MSE"] > 0)

'''
Test the mlpy Simple Linear Regression Prediction script.
'''
class LinearRegression_MLPY_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/diabetes.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/mlpy/linear_regression.py")
    obj = getattr(module, "LinearRegression")
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
    result = self.instance.RunMetrics({})
    print(result)
    self.assertTrue(result["Runtime"] > 0)

'''
Test the matlab Simple Linear Regression Prediction script.
'''
class LinearRegression_MATLAB_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/diabetes.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/matlab/linear_regression.py")
    obj = getattr(module, "LinearRegression")
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
    result = self.instance.RunMetrics({})
    self.assertTrue(result["Runtime"] > 0)

'''
Test the R Simple Linear Regression Prediction script.
'''
class LinearRegression_R_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/diabetes.csv']
    self.verbose = False
    self.timeout = 500 # Changed because installing Packages might take time.

    module = Loader.ImportModuleFromPath("methods/R/linear_regression.py")
    obj = getattr(module, "LinearRegression")
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
    result = self.instance.RunMetrics({})
    self.assertTrue(result["Runtime"] > 0)

if __name__ == '__main__':
  unittest.main()
