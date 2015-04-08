# Lasso Plotter for Newsblaster
# Author: Ramzi Abdoch
#
# * Files in folder are of file_type .annotation

# SciKit Learn: Logistic Regression
from sklearn import linear_model
from sklearn.svm import l1_min_c

# Import MathPlotLib
import matplotlib.pyplot as plt

# Numpy
import numpy as np

# Utilities
import sys
import os
import random
import pickle

# HTMLVectorizer
from article_extractor import htmlvectorizer

# LR Weights
from lr_weights import LRWeights

class LassoPlotter():

	def __init__(self, data_path):
		self.lr_w = LRWeights()
		self.lr_w.sample(data_path)
		self.X = lr_w.X
		self.y = lr_w.y

	def plot(self):

		X = self.X
		y = self.y.reshape(self.y.shape[0])

		cs = l1_min_c(X, y, loss="log") * np.logspace(0,3)

		coefs_ = []

		for c in cs:
			print "Evaluating: C = ", c
			weights = self.lr_w.get_weights(y, c)
			coefs_.append(weights.ravel().copy())

		coefs_ = np.array(coefs_)
		plt.plot(np.log10(cs), coefs_)
		ymin, ymax = plt.ylim()
		plt.xlabel('log(C)')
		plt.ylabel('Coefficients')
		plt.title('Logistic Regression Path')
		plt.axis('tight')
		#plt.show()
		plt.savefig("lr_lasso.png")

		print "Done!"

def usage():
    print """
    python lasso_plot.py [folder_of_annotated_articles]
        Read in article files in the training set and
        train Logistic Regression Classifier. Then,
        determine weights of features for each class
        and plot v. c

    output:
		plot of changing (class, feature) pairs by class-conditional weight v. c (param for LR Classifier)
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: prepared training data
        usage()
        sys.exit(2)

    # Initialize NBClassifier()
    lp = LassoPlotter(sys.argv[1])
    # Run classify on the annotation_folder
    lp.plot()

