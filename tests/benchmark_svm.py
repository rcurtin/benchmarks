'''
  @file benchmark_svm.py
  Test for the svm scripts.
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
Test the scikit svm script.
'''

class SVM_SCIKIT_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv','datasets/iris_test.csv','datasets/iris_labels.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/scikit/svm.py")
    obj = getattr(module, "SVM")
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
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)

'''
Test the matlab Parametric Support Vector Classifier script.
'''
class SVC_MATLAB_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv', 'datasets/iris_labels.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/matlab/svc.py")
    obj = getattr(module, "SVC")
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
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)

'''
Test the dlibml Parametric Support Vector Classifier script.
'''
class SVM_DLIBML_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv', 'datasets/iris_labels.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/dlibml/SVM.py")
    obj = getattr(module, "SVM")
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
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)

'''
Test the R Parametric Support Vector Classifier script.
'''
class SVC_R_TEST(unittest.TestCase):

  '''
  Test initialization.
  '''
  def setUp(self):
    self.dataset = ['datasets/iris_train.csv', 'datasets/iris_test.csv', 'datasets/iris_labels.csv']
    self.verbose = False
    self.timeout = 240

    module = Loader.ImportModuleFromPath("methods/R/svc.py")
    obj = getattr(module, "SVC")
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
    self.assertTrue(result["ACC"] > 0)
    self.assertTrue(result["Precision"] > 0)
    self.assertTrue(result["Recall"] > 0)


if __name__ == '__main__':
  unittest.main()
