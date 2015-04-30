#  Chain Logistic Regression Classifiers
#  Phase I - predict body
#  Phase II - predict title
#  @Author - Ramzi Abdoch

# Utiltities
import sys

# Numpy
import numpy as np

# Data Prep for Phase II
from dp_phaseII import DP2

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

    # Extract examples, gold labels, label encoder, and document indexes
    X = lr_w.X
    y = lr_w.y.copy()
    le = lr_w.le
    hv = lr_w.hv
    doc_idxs = lr_w.doc_idxs

    '''
    PHASE I - Body Classification
    '''

    # Sample y for y = "Body"
    body_class_idx = le.transform(['Body'])[0]
    body_idxs = np.where(y==body_class_idx)

    y_body = np.zeros_like(y)

    y_body[body_idxs] = body_class_idx

    # Get weights and bias of trained LR classifier for Body
    W_body, b_body = lr_w.get_weights(y_body)

    # Initialize lrclf
    clf = lrclf.LRClassifier()

    # Predict labels
    y_hat_body = clf.classify(X, W_body, b_body)

    # Calculate error of lrclf on y_body
    body_clf_error = accuracy_score(y_body, y_hat_body)

    '''
    PHASE II - Title Classification
    '''

    # Prepare data for Phase II
    dp2 = DP2()

    # Sample y for y = "Title"
    title_class_idx = le.transform(['Title'])[0]
    title_idxs = np.where(y==title_class_idx)

    y_title = np.zeros_like(y)
    y_title[title_idxs] = title_class_idx

    # Merge y_body and y_title
    y_tb_gold = y_title.copy()
    y_tb_gold[body_idxs] = body_class_idx

    # Combine y_hat_body with gold title labels (y_hat_title_body)
    y_tb_preds = y_hat_body.copy()
    y_tb_preds[title_idxs] = title_class_idx

    # Predict Title on new_X_y_title w/ lrclf trained on gold T's
    new_X, non_b_idxs_by_doc = dp2.get_new_feats(X, y_body, doc_idxs, body_class_idx, hv)
    non_b_idxs = np.where(y_tb_gold != body_class_idx)
    y_t_non_b_gold = y_tb_gold[non_b_idxs]

    # Verify that new_X.shape[0] == y_t_non_b_gold.shape[0]
    assert new_X.shape[0] == y_t_non_b_gold.shape[0]

    # Predict Titles
    W_t_no_b_gold, b_t_no_b_gold = lr_w.get_weights(y_t_non_b_gold)
    y_hat_t_no_b = clf.classify(new_X, W_t_no_b_gold, b_t_no_b_gold)

    # Find Title with highest probability
    #probs = argmax(clf.P, axis=1)

    # Predict Title on new_X_y_preds w/ lrclf trained on pred B's
    #new_X, non_b_idxs_by_doc = dp2.get_new_feats(X, y_hat_body, doc_idxs, body_class_idx, hv)

    # # Get weights of trained LR classifier on y_tb and y_hat_tb
    # W_tb_gold, b_tb_gold = lr_w.get_weights(y_tb_gold)
    # W_tb_preds, b_tb_preds = lr_w.get_weights(y_tb_preds)

    # # Predict labels
    # y_hat_tb = clf.classify(X, W_tb_gold, b)
    # y_hat_hat_tb = clf.classify(X, W_tb_preds, b)

    # # Calculate error of lrcf on y_tb_gold and y_tb_preds
    # tb_gold_error = accuracy_score(y_tb_gold, y_hat_tb)
    # tb_preds_error = accuracy_score(y_tb_preds, y_hat_hat_tb)
