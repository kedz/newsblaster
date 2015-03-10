# Naive Bayes Classifier for Newsblaster
# Author: Ramzi Abdoch
#
# Usage:
#	- NBClassifier.classify(folder_path)
#
# Output:
#   - Results of classifier on training data in folder
#
# * Files in folder are of file_type .annotation

# SciKit Learn: Naive Bayes + Classification Reporting
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn.metrics import classification_report

# Numpy
import numpy as np

# To iterate through folder
import sys
import os

# HTMLVectorizer
from article_extractor import htmlvectorizer

class NBClassifier():

	def classify(self, folder):

		# Initialize HTMLVectorizer
		hv = htmlvectorizer.HTMLVectorizer()

		# Files to open
		an_files = list()

		# Build list of dicts from .annotation files in folder (argv)
		for filename in os.listdir(folder):
			path = os.path.join(folder, filename)
			an_files.append(path)

		# Build X & Y
		X = list()
		y = list()

		# Get Matrix of Vectors for all files
		hv_result = hv.fit_transform(an_files)
		X = hv_result[0]
		y = hv_result[1]

		# Turn y into numpy array
		y = np.array(y)

		#############
		## TESTING ##
		#############

		# n - 1 fold cross validation (leave-one-out)
		kf = KFold(len(y), n_folds=len(y) - 1, shuffle=True)
		print kf

		for train_index, test_index in kf:
			print("TRAIN:", train_index, "TEST:", test_index)
			X_train, X_test = X[train_index], X[test_index]
			y_train, y_test = y[train_index], y[test_index]

		# Run SciKit Naive Bayes Classifier
		clf = MultinomialNB()
		clf.fit(X_train, y_train)

		# Run the classifier over the training data and report success
		y_pred = clf.predict(X_test)

		print classification_report(y_test, y_pred)

def usage():
    print """
    python NBClassifier.py [folder_of_annotated_articles]
        Read in article files in the training set and
        train Naive Bayes Classifier. Then, predict tags for 
        each example and compare against training set.
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the folder of annotated articles
        usage()
        sys.exit(2)

    # Initialize NBClassifier()
    n = NBClassifier()
    # Run classify on the annotation_folder
    n.classify(sys.argv[1])
