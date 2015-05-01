# Logistic Classification Reports for Newsblaster
# Classification Report with 5 folds
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

# Utilities
import sys
import os
import random
from datetime import datetime

# Pickle
import pickle

# HTMLVectorizer
from article_extractor import htmlvectorizer

class LogRClassifier():

	def sample(self, path):
		with open(path, "r") as f:
			X, y, hv, le = pickle.load(f)
			print X.shape

		# Find which class corresponds to None
		none_idx = le.classes_.index('None')

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

	def get_weights(self, n_folds=5):

		X = self.X
		y = self.y.reshape(self.y.shape[0])
		hv = self.hv
		le = self.le

		#cs = l1_min_c(X, y, loss="log") * np.logspace(0,3)
		cs = [.001, .01, .1, 1]

		# Start the clock
		start = datetime.now()

		clf = linear_model.LogisticRegression(C=1.0, penalty='l1', tol=1e-6)

		for c in cs:

			coefs = []
			coefs_sum = np.zeros((len(le.classes_), X.shape[1]), dtype=np.float64)
			print "\n c = %f\n" % c
			clf.set_params(C=c)

			# 5-fold classification for each c
			kf = KFold(len(y), n_folds=n_folds, shuffle=True)

			for train_index, test_index in kf:
				#print("TRAIN:", train_index, "TEST:", test_index)
				X_train, X_test = X[train_index], X[test_index]
				y_train, y_test = y[train_index], y[test_index]

				# Run Logistic Regression
				clf.fit(X_train, y_train)

				print clf.raw_coef_
				print clf.raw_coef_.shape

				coefs_sum += clf.coef_

			coefs_avg = coefs_sum / float(n_folds)

			# Run the classifier over the training data and report success
			y_pred = clf.predict(X_test)

			print classification_report(y_test, y_pred)

		# Print duration
		print("This took ", datetime.now() - start)

		print "Done!"

def usage():
    print """
    python log_reg.py [folder_of_annotated_articles]
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

