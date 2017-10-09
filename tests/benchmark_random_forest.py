'''
  @file benchmark_random_forest.py

  Test for the Random Forest scripts.
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
Test the scikit-learn RandomForest script.
'''
class RandomForest_SCIKIT_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv',
        'datasets/iris_labels.csv']

    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/scikit/random_forest.py")
    obj = getattr(module, "RANDOMFOREST")
    self.instance = obj(self.dataset, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the RunMetrics Function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "num_trees": 10 })
    self.assertTrue(result["Runtime"] > 0)
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)

'''
Test the SHOGUN-learn RandomForest script.
'''
class RandomForest_SHOGUN_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv',
        'datasets/iris_labels.csv']

    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/shogun/random_forest.py")
    obj = getattr(module, "RANDOMFOREST")
    self.instance = obj(self.dataset, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the RunMetrics Function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "num_trees": 10 })
    self.assertTrue(result["Runtime"] > 0)
    self.assertTrue(result["Avg Accuracy"] > 0)
    self.assertTrue(result["MultiClass Precision"] > 0)
    self.assertTrue(result["MultiClass Recall"] > 0)

'''
Test the Milk RandomForest script.
'''
class RandomForest_Milk_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv',
        'datasets/iris_labels.csv']

    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/milk/random_forest.py")
    obj = getattr(module, "RANDOMFOREST")
    self.instance = obj(self.dataset, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the RunMetrics Function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "num_trees": 10 })
    self.assertTrue(result["Runtime"] > 0)
'''
Test the weka RandomForest script.
'''
class RandomForest_WEKA_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.arff', 'datasets/iris_test.arff',
        'datasets/iris_labels.csv']

    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/weka/random_forest.py")
    obj = getattr(module, "RANDOMFOREST")
    self.instance = obj(self.dataset, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the RunMetrics Function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({})
    self.assertTrue(result["Runtime"] > 0)
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)

'''
Test the MATLAB RandomForest script.
'''
class RandomForest_MATLAB_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv',
        'datasets/iris_labels.csv']

    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/matlab/random_forest.py")
    obj = getattr(module, "RANDOMFOREST")
    self.instance = obj(self.dataset, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the RunMetrics Function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "num_trees": 10 })
    self.assertTrue(result["Runtime"] > 0)
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)

'''
Test the R  RandomForest script.
'''
class RandomForest_R_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv',
        'datasets/iris_labels.csv']

    self.verbose = False
    self.timeout = 500 #Changed because installing Packages might take time.

    module = Loader.ImportModuleFromPath("methods/R/random_forest.py")
    obj = getattr(module, "RANDOMFOREST")
    self.instance = obj(self.dataset, timeout=self.timeout)

  '''
  Test the constructor.
  '''
  def test_Constructor(self):
    self.assertEqual(self.instance.timeout, self.timeout)
    self.assertEqual(self.instance.dataset, self.dataset)

  '''
  Test the RunMetrics Function.
  '''
  def test_RunMetrics(self):
    result = self.instance.RunMetrics({ "num_trees": 10 })
    self.assertTrue(result["Runtime"] > 0)
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)


if __name__ == '__main__':
  unittest.main()
