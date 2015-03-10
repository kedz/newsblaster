import pickle
import sys
import os

# HTMLVectorizer
from article_extractor import htmlvectorizer

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

		# Build X & Y
		X = list()
		y = list()

		# Get Matrix of Vectors for all files
		hv_result = hv.fit_transform(an_files)
		X = hv_result[0]
		y = hv_result[1]

		# Turn y into numpy array
		y = np.array(y)

		return X, y

def usage():
    print """

    output:
		sorted set of class-conditional weights for each feature in the training set
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly one argument: the folder of annotated articles
        usage()
        sys.exit(2)

    # Initialize NBClassifier()
    dp = DataPrep()
    # Run classify on the annotation_folder
    [X, y] = dp.prep(sys.argv[1])

    filename = sys.argv[2]

    with open(filename, "w") as f:
		pickle.dump([X, y], f)



