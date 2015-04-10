#  Test Logistic Regression Classifier
#  @Author - Ramzi Abdoch

# Utiltities
import sys

# Numpy
import numpy as np

# Logistic Regression Classifier
# + Scikit Learn LR Classifier to get weights
import lr_classifier as lrclf
from lr_weights import LRWeights

# Calculate error
from sklearn.metrics import accuracy_score

def usage():
    print """
    python chain_lrclf.py [prepared_training_data]
       **TODO** DESCRIPTION

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

    # Extract examples, gold labels, and label encoder
    X = lr_w.X
    y = lr_w.y.copy()
    le = lr_w.le

    '''
    PHASE I - Body Classification
    '''

    # Sample y for y = "Body"
    body_class_idx = le.transform(['Body'])[0]
    body_idxs = np.where(y==body_class_idx)

    y_body = np.zeros(len(y))

    print 'Size of X :', X.shape
    print 'Length of y :', len(y), len(y_body)

    print 'Lenght of body_idxs', len(body_idxs)

    for item in body_idxs:
        print item

    y_body[body_idxs] = body_class_idx

    # Get weights of trained LR classifier for Body
    W_body = lr_w.get_weights(y_body)

    # Set bias parameter
    b = 1

    # Initialize lrclf
    clf = lrclf.LRClassifier()

    # Predict labels
    y_hat_body = clf.classify(X, W_body, b)

    # Calculate error of lrclf on y_body
    body_clf_error = accuracy_score(y_body, y_hat_body)

    '''
    PHASE II - Title Classification
    '''

    # Sample y for y = "Title"
    title_class_idx = le.transform(['Title'])[0]
    title_idxs = np.where(y==title_class_idx)
    y_title = np.zeros(len(y))
    y_title[title_idxs] = title_class_idx

    # Merge y_body and y_title
    y_tb_gold = y_title.copy()
    y_tb_gold[body_idxs] = body_class_idx

    # Combine y_hat_body with gold title labels (y_hat_title_body)
    y_tb_preds = y_hat_body.copy()
    y_tb_preds[title_idxs] = title_class_idx

    # Get weights of trained LR classifier on y_tb and y_hat_tb
    W_tb_gold = lr_w.get_weights(y_tb_gold)
    W_tb_preds = lr_w.get_weights(y_tb_preds)

    # Predict labels
    y_hat_tb = clf.classify(X, W_tb_gold, b)
    y_hat_hat_tb = clf.classify(X, W_tb_preds, b)

    # Calculate error of lrcf on y_tb_gold and y_tb_preds
    tb_gold_error = accuracy_score(y_tb_gold, y_hat_tb)
    tb_preds_error = accuracy_score(y_tb_preds, y_hat_hat_tb)
