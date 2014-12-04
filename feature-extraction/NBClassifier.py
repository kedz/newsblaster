# Naive Bayes Classifier for Newsblaster
# Author: Ramzi Abdoch
# 
# Usage:
#	- python NBClassifier.py <folder_name>
#
# Output:
#   - Results of classifier on training data in folder
#   - Files in folder are of file_type .annotation

# SciKit Learn: Naive Bayes + Classification Reporting
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# To iterate through folder
import sys
import os

# HTMLVectorizer
from article_extractor import htmlvectorizer

# Initialize HTMLVectorizer
hv = htmlvectorizer.HTMLVectorizer()

# Files to open
an_files = list()

# Build list of dicts from .annotation files in folder (argv)
for filename in os.listdir(sys.argv[1]):
    path = os.path.join(sys.argv[1], filename)
    an_files.append(path)

# Build X & Y
X = list()
Y = list()

# Get Matrix of Vectors for all files
for annotation in an_files:
	hv_result = hv.fit_transform(annotation)
	X.append(hv_result[0])
	Y.append(hv_result[1])

#############
## TESTING ##
#############

print "X", X
#print "Y", Y

# Run SciKit Naive Bayes Classifier
clf = MultinomialNB()
clf.fit(X, Y)

# Run the classifier over the training data and report success
Y_pred = clf.predict(X)

print classification_report(Y, Y_pred)
