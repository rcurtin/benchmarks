'''
  @file SVR.py
  @author Saurabh Mahindre

  SVR Regression with scikit.
'''

import os
import sys
import inspect
import timeout_decorator

# Import the util path, this method even works if the path contains symlinks to
# modules.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
  os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../util")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from log import *
from timer import *
from misc import *

import numpy as np
from sklearn.svm import SVR as SSVR

'''
This class implements the SVR Regression benchmark.
'''
class SVR(object):

  '''
  Create the SVR Regression benchmark instance.

  @param dataset - Input dataset to perform Least Angle Regression on.
  @param timeout - The time until the timeout. Default no timeout.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.timeout = timeout

  '''
  Use the scikit libary to implement svr Regression.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def SVRScikit(self, options):
    @timeout_decorator.timeout(self.timeout)
    def RunSVRScikit():
      totalTimer = Timer()

      # Load input dataset.
      Log.Info("Loading dataset", self.verbose)
      # Use the last row of the training set as the responses.
      X, y = SplitTrainData(self.dataset)

      # Get all the parameters.
      opts = {}
      if "c" in options:
        opts["C"] = float(options.pop("c"))
      if "epsilon" in options:
        opts["epsilon"] = float(options.pop("epsilon"))
      if "gamma" in options:
        opts["gamma"] = float(options.pop("gamma"))
      opts["kernel"] = "rbf"

      if len(options) > 0:
        Log.Fatal("Unknown parameters: " + str(options))
        raise Exception("unknown parameters")

      try:
        with totalTimer:
          # Perform SVR.
          model = SSVR(**opts)
          model.fit(X, y)
      except Exception as e:
        return -1

      return totalTimer.ElapsedTime()

    try:
      return RunSVRScikit()
    except timeout_decorator.TimeoutError:
      return -1

  '''
  Perform SVR Regression. If the method has been successfully completed
  return the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform SVR.", self.verbose)

    results = self.SVRScikit(options)
    if results < 0:
      return results

    return {'Runtime' : results}
