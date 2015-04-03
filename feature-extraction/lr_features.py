# Logistic Regression Classifier for Newsblaster
# Lasso Regularization to determine key features
# Author: Ramzi Abdoch

# SciKit Learn: Logistic Regression
from sklearn import linear_model
from sklearn.cross_validation import KFold
from sklearn.svm import l1_min_c
from sklearn.metrics import classification_report

# MathPlotLib
import matplotlib.pyplot as plt

# Numpy
import numpy as np

# Utiltities
import sys
import os
import random
from datetime import datetime

# Pickle
import pickle

class LogRClassifier():

	def sample(self, path):
		with open(path, "r") as f:
			X, y, hv, le = pickle.load(f)
			print X.shape

		# Sklearn preprocessing label encoder

		# Find which class corresponds to None
		none_idx = le.transform(['None'])[0]

		# Find all None labeled examples and their corresponding labels
		X_none = X[np.where(y==none_idx)]
		y_none = y[np.where(y==none_idx)]

		# Find other labeled examples
		X_something = X[np.where(y!=none_idx)]
		y_something = y[np.where(y!=none_idx)]

		# Randomly sample # of other labels from examples labeled None
		indexes = range(X_none.shape[0])
		random.shuffle(indexes)

		new_idxs = indexes[:X_something.shape[0]]
		X_none_sampled = X_none[new_idxs,:]
		y_none_sampled = y_none[new_idxs]

		X_new = np.vstack([X_none_sampled, X_something])
		y_new = np.vstack([y_none_sampled[:,np.newaxis], y_something[:,np.newaxis]])

		final_idxs = range(X_new.shape[0])
		random.shuffle(final_idxs)

		self.X = X_new[final_idxs, :]
		self.y = y_new[final_idxs]
		self.hv = hv
		self.le = le

	def get_non_0_weights(self, weight_matrix, hv, le):
		results = list()

		# iterate through classes
		for i in range(len(weight_matrix)):
			# iterate through features
			for j in range(len(weight_matrix[i])):
				# check if weight is non-zero
				if(weight_matrix[i][j] != 0):
					# Triple of [class][feature][weight]
					cls = le.classes_[i]
					feat = hv.v.get_feature_names()[j]

					triple = tuple([cls,feat,weight_matrix[i][j]])
					results.append(triple)

		return results

	def get_weights(self):

		X = self.X
		y = self.y.reshape(self.y.shape[0])
		hv = self.hv
		le = self.le

		#cs = l1_min_c(X, y, loss="log") * np.logspace(0,3)
		cs = [1]

		# Start the clock
		start = datetime.now()

		clf = linear_model.LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
		coefs_ = []

		for c in cs:
			print "\n c = %f\n" % c
			clf.set_params(C=c)
			clf.fit(X, y)

			# Assert # of rows in weight matrix == # of categories

			normal_coef = clf.coef_.copy()
			coefs_.append(normal_coef.ravel())

		# Print duration
		print("This took %s" % str(datetime.now() - start))

		# Find non-zero coefficients
		print self.get_non_0_weights(normal_coef, hv, le)

		print "Done!"

def usage():
    print """
    python lr_features.py [folder_of_annotated_articles]
        Read in article files in the training set and
        train Logistic Regression Classifier. Then,
        determine weights of features for each class
        and sort.

    output:
		sorted set of class-conditional weights for each feature in the training set
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the folder of annotated articles
        usage()
        sys.exit(2)

    # Initialize NBClassifier()
    lr = LogRClassifier()
    # Sample data
    lr.sample(sys.argv[1])
    # Run classify on the annotation_folder
    lr.get_weights()

