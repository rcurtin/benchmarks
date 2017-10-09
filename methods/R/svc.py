'''
  @file svc.py
  Class to benchmark the R Support Vector Classification method.
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
from profiler import *
from definitions import *
from misc import *

import shlex
import subprocess
import re
import collections
import numpy as np

'''
This class implements the SVC benchmark.
'''
class SVC(object):

  '''
  Create the SVC instance.
  @param dataset - Input dataset to perform SVC on.
  @param timeout - The time until the timeout. Default no timeout.
  @param path - Path to the R executable.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, path=os.environ["R_PATH"],
      verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.path = path
    self.timeout = timeout
    self.build_opts = {}
    
  def __del__(self):
    Log.Info("Clean up.", self.verbose)
    filelist = ["predictions.csv", "log.txt"]
    for f in filelist:
      if os.path.isfile(f):
        os.remove(f)

  '''
  SVC. If the method has been successfully completed return
  the elapsed time in seconds.
  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform SVC.", self.verbose)

    # Get all the parameters.
    self.build_opts = {}
    if "c" in options:
      self.build_opts["C"] = float(options.pop("c"))
    else:
      self.build_opts["C"] = 1

    if "epsilon" in options:
      self.build_opts["epsilon"] = float(options.pop("epsilon"))
    else:
      self.build_opts["epsilon"] = 0.1


    if len(options) > 0:
      Log.Fatal("Unknown parameters: " + str(options))
      raise Exception("unknown parameters")

    if len(self.dataset) < 2:
      Log.Fatal("This method requires two or more datasets.")
      return -1

    # Split the command using shell-like syntax.
    cmd = shlex.split("libraries/bin/Rscript " + self.path + "svc.r" +
        " -t " + self.dataset[0] + " -T " +
        self.dataset[1] + " -c " + str(self.build_opts["C"]) + 
	" -e " + str(self.build_opts["epsilon"]))

    # Run command with the nessecary arguments and return its output as a byte
    # string. We have untrusted input so we disable all shell based features.
    try:
      s = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False,
          timeout=self.timeout)
    except subprocess.TimeoutExpired as e:
      Log.Warn(str(e))
      return -2
    except Exception as e:
      Log.Fatal("Could not execute command: " + str(cmd))
      return -1

    # Datastructure to store the results.
    metrics = {}
    # Parse data: runtime.
    timer = self.parseTimer(str(s))
    if timer != -1:
      metrics['Runtime'] = timer
      predictions = np.genfromtxt("predictions.csv", delimiter = ',')
      predictions = predictions[1:]
      truelabels = np.genfromtxt(self.dataset[2], delimiter = ',')
      confusionMatrix = Metrics.ConfusionMatrix(truelabels, predictions)
      metrics['ACC'] = Metrics.AverageAccuracy(confusionMatrix)
      metrics['MCC'] = Metrics.MCCMultiClass(confusionMatrix)
      metrics['Precision'] = Metrics.AvgPrecision(confusionMatrix)
      metrics['Recall'] = Metrics.AvgRecall(confusionMatrix)
      metrics['MSE'] = Metrics.SimpleMeanSquaredError(truelabels, predictions)

      Log.Info(("total time: %fs" % (metrics['Runtime'])), self.verbose)

    return metrics

  '''
  Parse the timer data form a given string.
  @param data - String to parse timer data from.
  @return - Namedtuple that contains the timer data or -1 in case of an error.
  '''
  def parseTimer(self, data):
    # Compile the regular expression pattern into a regular expression object to
    # parse the timer data.
    pattern = re.findall("(\d+\.\d+). *sec elapsed", data)
    return float(pattern[0])
