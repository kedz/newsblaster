#  Test Logistic Regression Classifier
#  @Author - Ramzi Abdoch

# Utiltities
import sys

# Logistic Regression Classifier
# + Scikit Learn LR Classifier to get weights
import lr_classifier as lrclf
from lr_weights import LRWeights

# Calculate error
from sklearn.metrics import accuracy_score

def usage():
    print """
    python test_lrclf.py [prepared_training_data]
        Read in the training set and train Logistic Regression
        Classifier. Then, determine weights of features for
        each class and predict labels for all training examples.
        Finally, calculate the error of our LR Classifier.

    output:
        predictions for each example in the training set
    """

# Run the classifier
if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the prepared training data
        usage()
        sys.exit(2)

    # Initialize Feature Extractor
    lr_w = LRWeights()
    # Sample Training Data
    lr_w.sample(sys.argv[1])
    # Get weights of trained LR classifier
    X = lr_w.X
    y = lr_w.y

    W, b = lr_w.get_weights(y)

    clf = lrclf.LRClassifier()

    y_hat = clf.classify(X, W, b)

    print accuracy_score(y, y_hat)

