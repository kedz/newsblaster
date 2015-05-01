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

# Add above directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

# Pickle
import pickle

class LRWeights():

	def sample(self, path):
		with open(path, "r") as f:
			X, y, hv, le, doc_idxs, all_bows = pickle.load(f)
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
		self.doc_idxs = doc_idxs
		self.all_bows = all_bows

	def no_pickle_sample(self, X, y, hv, le, doc_idxs, all_bows):
		# Sklearn preprocessing label encoder

		# Find which class corresponds to None
		none_idx = le.transform(['None'])[0]
		none_idxs = np.where(y==none_idx)
		not_none_idxs = np.where(y!=none_idx)

		# Find all None labeled examples and their corresponding labels
		X_none = X[none_idxs]
		y_none = y[none_idxs]

		original_docs_none = list()

		for idx in not_none_idxs:
			closest_idx = (np.abs(doc_idxs-idx)).argmin()

			if doc_idxs[closest_idx] > idx:
				original_docs_none.append(idx - 1)
			else:
				original_docs_none.append(idx)

		# Find other labeled examples
		X_something = X[not_none_idxs]
		y_something = y[not_none_idxs]

		# Keep track of which document each example comes from to use proper count vectorizer
		original_docs_something = list()

		for idx in not_none_idxs:
			closest_idx = (np.abs(doc_idxs-idx)).argmin()

			if doc_idxs[closest_idx] > idx:
				original_docs_something.append(idx - 1)
			else:
				original_docs_something.append(idx)

		# Randomly sample # of other labels from examples labeled None
		indexes = range(X_none.shape[0])
		random.shuffle(indexes)

		# Choose (# of other labels) examples from X_none
		new_idxs = indexes[:X_something.shape[0]]
		X_none_sampled = X_none[new_idxs,:]
		y_none_sampled = y_none[new_idxs]

		original_docs_none_sampled = list()

		# Recover original docs
		for idx in new_idxs:
			original_docs_none_sampled.append(original_docs_none[idx])

		X_new = np.vstack([X_none_sampled, X_something])
		y_new = np.vstack([y_none_sampled[:,np.newaxis], y_something[:,np.newaxis]])
		original_docs_new = np.vstack([original_docs_none_sampled, original_docs_something])

		# Finally, shuffle the sampled result
		final_idxs = range(X_new.shape[0])
		random.shuffle(final_idxs)

		self.X = X_new[final_idxs, :]
		self.y = y_new[final_idxs]
		self.original_docs = original_docs_new[final_idxs]
		self.hv = hv
		self.le = le
		self.doc_idxs = doc_idxs
		self.all_bows = all_bows

	def get_weights(self, y, c=1):

		X = self.X
		y = y.reshape(y.shape[0])

		# Set LR params
		clf = linear_model.LogisticRegression(C=c, penalty='l1', tol=1e-6)

		clf.fit(X, y)

		return clf.coef_.copy(), clf.intercept_.copy()

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
    lr_weights = LRWeights()
    # Sample data
    lr_weights.sample(sys.argv[1])
    # Return weights of LR classifier trained on data in folder
    print lr_weights.get_weights(lr_weights.y)

