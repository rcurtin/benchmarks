'''
  @file allknn.py
  @author Marcus Edel

  All K-Nearest-Neighbors with mlpy.
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
import mlpy

'''
This class implements the All K-Nearest-Neighbors benchmark.
'''
class ALLKNN(object):

  '''
  Create the All K-Nearest-Neighbors benchmark instance.

  @param dataset - Input dataset to perform All K-Nearest-Neighbors on.
  @param timeout - The time until the timeout. Default no timeout.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.timeout = timeout

  '''
  Use the mlpy libary to implement All K-Nearest-Neighbors.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def AllKnnMlpy(self, options):
    @timeout_decorator.timeout(self.timeout)
    def RunAllKnnMlpy():
      totalTimer = Timer()

      # Load input dataset.
      # If the dataset contains two files then the second file is the query
      # file.
      Log.Info("Loading dataset", self.verbose)
      if len(self.dataset) == 2:
        referenceData = np.genfromtxt(self.dataset[0], delimiter=',')
        queryData = np.genfromtxt(self.dataset[1], delimiter=',')
      else:
        referenceData = np.genfromtxt(self.dataset, delimiter=',')

      # Labels are the last row of the dataset.
      labels = referenceData[:, (referenceData.shape[1] - 1)]
      referenceData = referenceData[:,:-1]

      try:
        with totalTimer:
          # Get all the parameters.
          if not "k" in options:
            Log.Fatal("Required option: Number of furthest neighbors to find.")
            return -1
          else:
            k = options.pop("k")
            if (k < 1 or k > referenceData.shape[0]):
              Log.Fatal("Invalid k: " + k + "; must be greater than 0 "
                + "and less or equal than " + str(referenceData.shape[0]))
              return -1

          if len(options) > 0:
            Log.Fatal("Unknown parameters: " + str(options))
            raise Exception("unknown parameters")

          # Perform All K-Nearest-Neighbors.
          model = mlpy.KNN(k)
          model.learn(referenceData, labels)

          if len(self.dataset) == 2:
            out = model.pred(queryData)
          else:
            out = model.pred(referenceData)
      except Exception as e:
        return -1

      return totalTimer.ElapsedTime()

    try:
      return RunAllKnnMlpy()
    except timeout_decorator.TimeoutError:
      return -1


  '''
  Perform All K-Nearest-Neighbors. If the method has been successfully completed
  return the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform ALLKNN.", self.verbose)

    results = self.AllKnnMlpy(options)
    if results < 0:
      return results

    return {'Runtime' : results}
