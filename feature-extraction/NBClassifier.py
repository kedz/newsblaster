# SciKit Learn: Naive Bayes + Classification Reporting
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# To iterate through folder
import sys
import os

# HTMLVectorizer
from article_extractor import HTMLVectorizer

# Initialize HTMLVectorizer
hv = HTMLVectorizer()

# Files to open
an_files = list()

# Build list of dicts from .annotation files in folder (argv)
for filename in os.listdir(sys.argv[1]):
    path = os.path.join(sys.argv[1], filename)
    an_files.append(path)

# 
X = hv.fit_transform()
