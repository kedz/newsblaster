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

from sklearn.metrics import classification_report

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

	def no_pickle_sample(self, X, y, le):		# Note: all_text is changed to simply text
		# Sklearn preprocessing label encoder

		# Find which class corresponds to None
		none_idx = le.transform(['None'])[0]
		none_idxs = np.where(y==none_idx)
		something_idxs = np.where(y!=none_idx)

		# Find all None labeled examples and their corresponding labels
		X_none = X[none_idxs]
		y_none = y[none_idxs]
		#text_none = all_text[none_idxs]

		## DEBUG ##
		print  '''
			LRWeights #1 - X_none, y_none, text_none
		'''

		# Find other labeled examples
		X_something = X[something_idxs]
		y_something = y[something_idxs]
		#text_something = all_text[something_idxs]

		## DEBUG ##
		print  '''
			LRWeights #2 - X_something, y_something, text_something
		'''

		# Randomly sample # of other labels from examples labeled None
		indexes = range(X_none.shape[0])
		random.shuffle(indexes)

		# Choose (# of other labels) examples from X_none
		new_idxs = indexes[:X_something.shape[0]]
		new_idxs = np.array(new_idxs)
		something_idxs = np.array(something_idxs[0])

		X_none_sampled = X_none[new_idxs,:]
		y_none_sampled = y_none[new_idxs]

		## DEBUG ##
		print  '''
			LRWeights #3 - Sampling done
		'''

		X_new = np.vstack([X_none_sampled, X_something])
		y_new = np.append(y_none_sampled, y_something)

		sampled_original_idxs = np.append(new_idxs, something_idxs)

		# Finally, shuffle the sampled result
		final_idxs = range(X_new.shape[0])
		random.shuffle(final_idxs)

		## OUTPUT ##
		self.X = X_new[final_idxs, :]
		self.y = y_new[final_idxs]
		self.original_idxs = sampled_original_idxs[final_idxs]

		## DEBUG ##
		print "LR_W NO PICKLE SAMPLE COMPLETE"

	def get_weights(self, X, y, c=1):
		y = y.reshape(y.shape[0])

		# Set LR params
		clf = linear_model.LogisticRegression(C=c, penalty='l2', tol=1e-6, class_weight='auto')

		clf.fit(X, y)

		print classification_report(y, clf.predict(X))

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

