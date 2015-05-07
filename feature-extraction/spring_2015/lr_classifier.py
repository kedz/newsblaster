# Implementation of Logistic Regression Classifier
# Author: Ramzi Abdoch

# Numpy
import numpy as np

class LRClassifier():

	# X = examples
	# W = weights (from scikit-learn)
	# b = bias

	def classify(self, X, W, b):
		A = 1 / (1 + np.exp(-(X.dot(W.T) + b)))

		print "LRCLF RUN COMPLETE"

		return np.where(A > .5, 0, 1)

		# Make more robust #



