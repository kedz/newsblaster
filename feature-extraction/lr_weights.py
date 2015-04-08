# Logistic Regression Classifier for Newsblaster
# Lasso Regularization to determine key features
# Author: Ramzi Abdoch

# SciKit Learn: Logistic Regression
from sklearn import linear_model

# Numpy
import numpy as np

# Utiltities
import sys
import os
import random
from datetime import datetime

# Pickle
import pickle

class LRWeights():

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

	def get_weights(self, y, c=1):

		X = self.X
		y = y.reshape(y.shape[0])

		# Set LR params
		clf = linear_model.LogisticRegression(C=c, penalty='l1', tol=1e-6)

		clf.fit(X, y)

		return clf.coef_.copy()

def usage():
    print """
    python lr_weights.py [prepared_training_data]
        Read in the training set and train Logistic
        Regression Classifier. Then, determine weights
        of features for each class and return.

    output:
		set of class-conditional weights for each feature in the training set
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the folder of annotated articles
        usage()
        sys.exit(2)

    # Initialize Logistic Regression
    lr_weights = FeatureExtractor()
    # Sample data
    lr_weights.sample(sys.argv[1])
    # Return weights of LR classifier trained on data in folder
    print lr_weights.get_weights(1)

