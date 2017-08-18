'''
  @file elastic_net.py
  @author Marcus Edel

  Elastic Net Classifier with scikit.
'''

import os
import sys
import inspect

# Import the util path, this method even works if the path contains symlinks to
# modules.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
  os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../util")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

#Import the metrics definitions path.
metrics_folder = os.path.realpath(os.path.abspath(os.path.join(
  os.path.split(inspect.getfile(inspect.currentframe()))[0], "../metrics")))
if metrics_folder not in sys.path:
  sys.path.insert(0, metrics_folder)

from log import *
from timer import *
from definitions import *
from misc import *

import numpy as np
from sklearn.linear_model import ElasticNet as SElasticNet

'''
This class implements the Elastic Net Classifier benchmark.
'''
class ElasticNet(object):

  '''
  Create the Elastic Net Classifier benchmark instance.

  @param dataset - Input dataset to perform ElasticNet on.
  @param timeout - The time until the timeout. Default no timeout.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.timeout = timeout
    self.model = None
    self.predictions = None
    self.build_opts = {}

  '''
  Build the model for the Elastic Net Classifier.

  @param data - The train data.
  @param labels - The labels for the train set.
  @return The created model.
  '''
  def BuildModel(self, data, labels):
    # Create and train the classifier.
    elasticNet = SElasticNet(**self.build_opts)
    elasticNet.fit(data, labels)
    return elasticNet

  '''
  Use the scikit libary to implement the Elastic Net Classifier.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def ElasticNetScikit(self, options):
    def RunElasticNetScikit(q):
      totalTimer = Timer()

      Log.Info("Loading dataset", self.verbose)
      trainData, labels = SplitTrainData(self.dataset)
      testData = LoadDataset(self.dataset[1])

      self.build_opts = {}
      if "rho" in options:
        self.build_opts["rho"] = float(options.pop("rho"))
      if "alpha" in options:
        self.build_opts["alpha"] = float(options.pop("alpha"))
      if "max_iterations" in options:
        self.build_opts["max_iter"] = int(options.pop("max_iterations"))
      if "tolerance" in options:
        self.build_opts["tol"] = float(options.pop("tolerance"))
      if "selection" in options:
        self.build_opts["selection"] = str(options.pop("selection"))
        if self.build_opts["selection"] not in ['cyclic','random']:
          Log.Fatal("Invalid selection: " + self.build_opts["selection"]
                    + ". Must be either cyclic or random")
          q.put(-1)
          return -1

      if len(options) > 0:
        Log.Fatal("Unknown parameters: " + str(options))
        raise Exception("unknown parameters")

      try:
        with totalTimer:
          self.model = self.BuildModel(trainData, labels)
          # Run Elastic Net Classifier on the test dataset.
          self.predictions = self.model.predict(testData)
      except Exception as e:
        Log.Debug(str(e))
        q.put([-1])
        return -1

      time = totalTimer.ElapsedTime()
      if len(self.dataset) > 1:
        q.put([time, self.predictions])
      else:
        q.put([time])

      return time

    result = timeout(RunElasticNetScikit, self.timeout)
    # Check for error, in this case the list doesn't contain extra information.
    if len(result) > 1:
       self.predictions = result[1]

    return result[0]

  '''
  Perform the Elastic Net Classifier. If the method has been
  successfully completed return the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform Elastic Net.", self.verbose)

    results = None
    if len(self.dataset) >= 2:
      results = self.ElasticNetScikit(options)

      if results < 0:
        return results
    else:
      Log.Fatal("This method requires two datasets.")


    # Datastructure to store the results.
    metrics = {'Runtime' : results}

    if len(self.dataset) >= 3:

      truelabels = LoadDataset(self.dataset[2])

      confusionMatrix = Metrics.ConfusionMatrix(truelabels, self.predictions)
      metrics['ACC'] = Metrics.AverageAccuracy(confusionMatrix)
      metrics['MCC'] = Metrics.MCCMultiClass(confusionMatrix)
      metrics['Precision'] = Metrics.AvgPrecision(confusionMatrix)
      metrics['Recall'] = Metrics.AvgRecall(confusionMatrix)
      metrics['MSE'] = Metrics.SimpleMeanSquaredError(truelabels, self.predictions)

    return metrics

