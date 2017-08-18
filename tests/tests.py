import unittest
import xmlrunner

# Test modules.
modules = [
'benchmark_decision_tree',
'benchmark_allkfn',
'benchmark_allknn',
'benchmark_allkrann',
'benchmark_ann',
'benchmark_det',
'benchmark_emst',
'benchmark_fastmks',
'benchmark_gmm',
'benchmark_hmm_generate',
'benchmark_hmm_loglik',
'benchmark_hmm_train',
'benchmark_hmm_viterbi',
'benchmark_ica',
'benchmark_kernel_pca',
'benchmark_kmeans',
'benchmark_lars',
'benchmark_linear_regression',
'benchmark_linear_ridge_regression',
'benchmark_local_coordinate_coding',
'benchmark_logistic_regression',
'benchmark_lasso',
'benchmark_lsh',
'benchmark_nbc',
'benchmark_nca',
'benchmark_nmf',
'benchmark_pca',
'benchmark_qda',
'benchmark_random_forest',
'benchmark_range_search',
'benchmark_sparse_coding',
'benchmark_svr',
'benchmark_adaboost',
'benchmark_svm',
'benchmark_lda'
]

def load_tests(loader, tests, pattern):
  suite = unittest.TestSuite()
  # Add the modules to the suite.
  for t in modules:
      suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

  return suite

if __name__ == '__main__':
  # Run all modules (Testsuite).
  unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
