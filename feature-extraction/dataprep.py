# Data Preparation for Feature Extractor
# Author: Ramzi Abdoch
#
# * Files in folder are of file_type .annotation

# Utiltities
import pickle
import sys
import os

# HTMLVectorizer
from article_extractor import htmlvectorizer

# Sklearn Label Encoder (to keep labels consistent)
from sklearn.preprocessing import LabelEncoder

# Numpy
import numpy as np

class DataPrep():

    def prep(self, folder):
        # Initialize HTMLVectorizer
        hv = htmlvectorizer.HTMLVectorizer()

        # Files to open
        an_files = list()

        # Build list of dicts from .annotation files in folder (argv)
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            an_files.append(path)

        # Get Matrix of Vectors for all files
        [X, y, doc_idxs, bowser] = hv.fit_transform(an_files)

        le = LabelEncoder()
        y = le.fit_transform(y)

        # Turn y into numpy array
        y = np.array(y)

        return X, y, hv, le, doc_idxs, bowser

def usage():
    print """
    python dataprep.py [folder_of_annotated_articles] <filename_of_output>
        Read in the folder of annotated articles, then run the
        HTMLVectorizer, LabelEncoder, and Bowser to prepare training set.
        Pickle data and save as <filename_of_output>

    output:
        Training data set created from annotated HTML documents
        Format: Pickle'd [X (examples), y (labels), hv (HTMLVectorizer), le (LabelEncoder), doc_idxs (Beginning index of eaach document) , bowser (Bag of Words model for each document)]
    """

# Run the data preparation
if __name__ == "__main__":

    # Check correct usage
    if len(sys.argv)!=3:        # Expect exactly two arguments: the folder
        usage()                 # of annotated articles and output file name
        sys.exit(2)

    # Initialize DataPrep
    dp = DataPrep()

    # Run prep on the annotation_folder
    [X, y, hv, le, doc_idxs, bowser] = dp.prep(sys.argv[1])

    filename = sys.argv[2]

    # Write to file
    with open(filename, "w") as f:
        pickle.dump([X, y, hv, le, doc_idxs, bowser], f)
