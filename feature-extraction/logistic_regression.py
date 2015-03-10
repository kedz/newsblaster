# Logistic Regression Classifier for Newsblaster
# Author: Ramzi Abdoch
#
# * Files in folder are of file_type .annotation

# SciKit Learn: Logistic Regression
from sklearn import linear_model
from sklearn.cross_validation import KFold
from sklearn.svm import l1_min_c

# Import MathPlotLib
import matplotlib.pyplot as plt

# Numpy
import numpy as np

# To iterate through folder
import sys
import os

# HTMLVectorizer
from article_extractor import htmlvectorizer

class LogRClassifier():

	def get_weights(self, folder):

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

		cs = l1_min_c(X, y, loss="log") * np.logspace(0,3)

		#start = datetime.now()

		clf = linear_model.LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
		coefs_ = []
		for c in cs:
			print "ANOTHER ONE BITES THE DUST"
			clf.set_params(C=c)
			clf.fit(X, y)
			coefs_.append(clf.coef_.ravel().copy())

		#print("This took ", datetime.now() - start)

		coefs_ = np.array(coefs_)
		plt.plot(np.log10(cs), coefs_)
		ymin, ymax = plt.ylim()
		plt.xlabel('log(C)')
		plt.ylabel('Coefficients')
		plt.title('Logistic Regression Path')
		plt.axis('tight')
		plt.savefig("lr_lasso.png")

		# # Run SciKit Logistic Regression Classifier
		# clf = LogisticRegression(C=0.01, penalty="l1")
		# res = clf.fit_transform(X, y)

		# print res

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
    # Run classify on the annotation_folder
    lr.get_weights(sys.argv[1])

