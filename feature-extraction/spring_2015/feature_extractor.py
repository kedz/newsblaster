# Feature Extractor for Newsblaster
# Lasso Regularization to determine key features
# Author: Ramzi Abdoch

# Utilities
import sys

# Pickle
import pickle

# LR Weights - Scikit Learn Implementation of Logistic Regression
from lr_weights import LRWeights

class FeatureExtractor():

    def __init__(self, hv, le):
        self.hv = hv
        self.le = le

    def get_non_0_weights(self, weight_matrix):
        results = list()

        # iterate through classes
        for i in range(len(weight_matrix)):
            # iterate through features
            for j in range(len(weight_matrix[i])):
                # check if weight is non-zero

                print weight_matrix[i][j]

                if(weight_matrix[i][j] != 0):
                    # Triple of [class][feature][weight]
                    cls = self.le.classes_[i]
                    feat = self.hv.v.get_feature_names()[j]

                    triple = tuple([cls,feat,weight_matrix[i][j]])
                    results.append(triple)

        return results

def usage():
    print """
    python feature_extractor.py [prepared_training_data]
        Read in the training set and train Logistic
        Regression Classifier. Then, determine weights of
        features for each class and return non-zero features.

    output:
        (class, feature, weight) triples
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the folder of annotated articles
        usage()
        sys.exit(2)

    # Initialize LRWeights
    lr_w = LRWeights()

    # Sample Training Data
    lr_w.sample(sys.argv[1])

    # Get weights of trained LR classifier
    X = lr_w.X
    y = lr_w.y

    ## TODO ##
    ## Have yet to empirically discover best C ##

    ## Need to setup pipeline   ##
    ## to determine value for c ##
    ## using cross-validation   ##

    weights, intercept = lr_w.get_weights(y)
    hv = lr_w.hv
    le = lr_w.le

    # Initialize FeatureExtractor()
    fe = FeatureExtractor(hv, le)

    # Get non-zero weights
    for item in fe.get_non_0_weights(weights):
        print item

