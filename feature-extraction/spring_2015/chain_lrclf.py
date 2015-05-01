#  Chain Logistic Regression Classifiers
#  Phase I - predict body
#  Phase II - predict title
#  @Author - Ramzi Abdoch

# Utiltities
import sys

# Numpy
import numpy as np

# Data Prep for Phase I
from dataprep import DataPrep()

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

    dp = DataPrep()

    # Run prep on the annotation_folder
    [X, y, hv, le, doc_idxs, all_bows] = dp.prep(sys.argv[1])

    # Initialize Feature Extractor
    lr_w = LRWeights()

    # Sample Training Data
    lr_w.no_pickle_sample(X, y, hv, le, doc_idxs, all_bows)

    # Extract sampled examples, gold labels
    sample_X = lr_w.X
    sample_y = lr_w.y
    sample_original_docs = lr_w.original_docs

    '''
    PHASE I - Body Classification
    '''

    # Find all examples where y == "Body"
    body_class_idx = le.transform(['Body'])[0]
    body_idxs = np.where(sample_y==body_class_idx)

    # Find all examples where y !== "Body"
    non_body_idxs = np.where(sample_y!=body_class_idx)

    # Tranform none_class_idx for use in upcoming classification and create empty_y
    none_class_idx = le.transform(['None'])[0]
    empty_y = np.zeros_like(sample_y)
    empty_y[np.arange(0, len(empty_y) + 1)] = none_class_idx

    # Create empty array and fill w/ gold body tags
    y_body = empty_y.copy()
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
    new_X, new_y, non_b_idxs = dp2.gen_new_feats(sample_X, sample_y, original_docs, body_class_idx, title_class_idx, hv, bowser)

    # Find all examples where y == "Title"
    title_class_idx = le.transform(['Title'])[0]
    title_idxs = np.where(y==title_class_idx)

    # Create empty array and fill w/ gold title tags
    y_title = empty_y.copy()
    y_title[title_idxs] = title_class_idx

    # Create new_Y with all gold T's
    new_y = list()

    # Iterate through non_body_idxs, and add label if y == Title
    for idx in non_body_idxs:
        if y[idx] == title_class_idx:
            new_y.append(y[idx])
        else:
            new_y.append(none_class_idx)

    # Predict Title (Binary Prediction) w/ lrclf trained on
    # new_X and new_Y. new_x has new features from dp_phaseII
    # and new_Y has all non_body_idxs where y=="Title"
    W_title, b_title = lr_w.get_weights(new_y)

    '''
    --------------------------------------------
          vvvvvvvvvvvv OUT OF DATE vvvvvvvvv
    --------------------------------------------
    '''

    # Merge y_body and y_title
    y_tb_gold = y_title.copy()
    y_tb_gold[body_idxs] = body_class_idx

    # Combine y_hat_body with gold title labels (y_hat_title_body)
    y_tb_preds = y_hat_body.copy()
    y_tb_preds[title_idxs] = title_class_idx


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
