'''
  @file kmeans.py
  @author Marcus Edel

  K-Means Clustering with shogun.
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

import shlex
import subprocess
import re
import collections

import numpy as np
from modshogun import EuclideanDistance, RealFeatures, KMeans, Math_init_random

'''
This class implements the K-Means Clustering benchmark.
'''
class KMEANS(object):

  '''
  Create the K-Means Clustering benchmark instance.

  @param dataset - Input dataset to perform K-Means Clustering on.
  @param timeout - The time until the timeout. Default no timeout.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.timeout = timeout

  '''
  Use the shogun libary to implement K-Means Clustering.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def KMeansShogun(self, options):
    @timeout_decorator.timeout(self.timeout)
    def RunKMeansShogun():
      totalTimer = Timer()

      # Load input dataset.
      # If the dataset contains two files then the second file is the centroids
      # file.
      Log.Info("Loading dataset", self.verbose)
      if len(self.dataset) == 2:
        data = np.genfromtxt(self.dataset[0], delimiter=',')
        centroids = np.genfromtxt(self.dataset[1], delimiter=',')
      else:
        data = np.genfromtxt(self.dataset[0], delimiter=',')

      # Gather parameters.
      if "clusters" in options:
        clusters = int(options.pop("clusters"))
      elif len(self.dataset) != 2:
        Log.Fatal("Required option: Number of clusters or cluster locations.")
        return -1
      if "max_iterations" in options:
        maxIterations = int(options.pop("max_iterations"))
      seed = None
      if "seed" in options:
        seed = int(options.pop("seed"))

      if len(options) > 0:
        Log.Fatal("Unknown parameters: " + str(options))
        raise Exception("unknown parameters")

      if seed:
        Math_init_random(seed)
      try:
        dataFeat = RealFeatures(data.T)
        distance = EuclideanDistance(dataFeat, dataFeat)

        # Create the K-Means object and perform K-Means clustering.
        with totalTimer:
          if len(self.dataset) == 2:
            model = KMeans(clusters, distance, centroids.T)
          else:
            model = KMeans(clusters, distance)

          model.set_max_iter(m)
          model.train()

          labels = model.apply().get_labels()
          centers = model.get_cluster_centers()
      except Exception as e:
        return -1

      return totalTimer.ElapsedTime()

    try:
      return RunKMeansShogun()
    except timeout_decorator.TimeoutError:
      return -1

  '''
  Perform K-Means Clustering. If the method has been successfully
  completed return the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform K-Means.", self.verbose)

    results = self.KMeansShogun(options)
    if results < 0:
      return results

    return {'Runtime' : results}

  '''
  Return the elapsed time in seconds.

  @param timer - Namedtuple that contains the timer data.
  @return Elapsed time in seconds.
  '''
  def GetTime(self, timer):
    return timer.total_time
