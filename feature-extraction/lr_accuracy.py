# Logistic Regression Classifier for Newsblaster
# Accuracy Report
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

class LogRClassifier():

	def sample(self, path):
		with open(path, "r") as f:
			X, y = pickle.load(f)
			print X.shape

		X_none = X[np.where(y=="None")]
		y_none = y[np.where(y=="None")]
		X_something = X[np.where(y!="None")]
		y_something = y[np.where(y!="None")]

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

	def get_weights(self):

		X = self.X
		y = self.y.reshape(self.y.shape[0])

		cs = l1_min_c(X, y, loss="log") * np.logspace(0,3)

		# Start the clock
		start = datetime.now()

		clf = linear_model.LogisticRegression(C=1.0, penalty='l1', tol=1e-6)

		for c in cs:
			print "\n c = %f\n" % c
			clf.set_params(C=c)

			# Run Logistic Regression
			clf.fit(X, y)

			# Get avg. accuracy for model for each c
			print "Accuracy = %f" % clf.score(X,y)

		# Print duration
		print("This took %s" % str(datetime.now() - start))

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

