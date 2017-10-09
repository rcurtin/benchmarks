'''
  @file sparse_coding.py
  @author Marcus Edel

  Sparse Coding with scikit.
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

import numpy as np
from sklearn.decomposition import SparseCoder

'''
This class implements the Sparse Coding benchmark.
'''
class SparseCoding(object):

  '''
  Create the Sparse Coding benchmark instance.

  @param dataset - Input dataset to perform Sparse Coding on.
  @param timeout - The time until the timeout. Default no timeout.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.timeout = timeout

  '''
  Use the scikit libary to implement Sparse Coding.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def SparseCodingScikit(self, options):
    @timeout_decorator.timeout(self.timeout)
    def RunSparseCodingScikit():
      totalTimer = Timer()

      # Load input dataset.
      inputData = np.genfromtxt(self.dataset[0], delimiter=',')
      dictionary = np.genfromtxt(self.dataset[1], delimiter=',')

      # Get all the parameters.
      opts = {}
      if "lambda" in options:
        opts["transform_alpha"] = options.pop("lambda")
      if "max_iterations" in options:
        opts["max_iter"] = options.pop("max_iterations")
      opts["transform_algorithm"] = "lars"
      opts["dictionary"] = dictionary

      if len(options) > 0:
        Log.Fatal("Unknown parameters: " + str(options))
        raise Exception("unknown parameters")

      try:
        with totalTimer:
          # Perform Sparse Coding.
          model = SparseCoder(**opts)
          code = model.transform(inputData)
      except Exception as e:
        return -1

      return totalTimer.ElapsedTime()

    try:
      return RunSparseCodingScikit()
    except timeout_decorator.TimeoutError:
      return -1

  '''
  Perform Sparse Coding. If the method has been successfully completed
  return the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform Sparse Coding.", self.verbose)

    if len(self.dataset) != 2:
      Log.Fatal("This method requires two datasets.")
      return -1

    results = self.SparseCodingScikit(options)
    if results < 0:
      return results

    return {'Runtime' : results}
