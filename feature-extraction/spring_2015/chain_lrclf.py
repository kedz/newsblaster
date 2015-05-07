#  Chain Logistic Regression Classifiers
#  Phase I - predict body
#  Phase II - predict title
#  @Author - Ramzi Abdoch

# Utiltities
import sys

# Numpy
import numpy as np

# Data Prep for Phase I
from dataprep import DataPrep

# Data Prep for Phase II
from dp_phaseII import DP2

# Logistic Regression Classifier
# + Scikit Learn LR Classifier to get weights
import lr_classifier as lrclf
from lr_weights import LRWeights
from sklearn import linear_model

# Calculate error
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

def usage():
    print """
    python chain_lrclf.py [prepared_training_data]
       **TODO** DESCRIPTION

    output:
        predictions for each example in the training set
    """

# Run the classifier
if __name__ == "__main__":

    print '''
    PHASE O - Data Prep
    '''

    if len(sys.argv)!=2: # Expect exactly one argument: the prepared training data
        usage()
        sys.exit(2)

    dp = DataPrep()

    # Run prep on the annotation_folder
    [X, y, hv, le, doc_idxs, all_bows] = dp.prep(sys.argv[1])
    all_text = dp.all_text

    # Initialize Feature Extractor
    lr_w = LRWeights()

    # Sample Training Data
    lr_w.no_pickle_sample(X, y, le)

    # Extract sampled examples, gold labels
    sample_X = lr_w.X
    sample_y = lr_w.y
    sample_original_idxs = lr_w.original_idxs

    print '''
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
    empty_y[range(len(empty_y))] = none_class_idx

    # Create empty array and fill w/ gold body tags
    y_body = empty_y.copy()
    y_body[body_idxs] = body_class_idx

    clf = linear_model.LogisticRegression(C=1, penalty='l2', tol=1e-6, class_weight='auto')

    clf.fit(sample_X, y_body)

    # Get weights and bias of trained LR classifier for Body
    #W_body, b_body = lr_w.get_weights(sample_X, y_body)

    # Initialize lrclf
    #clf = lrclf.LRClassifier()

    # Predict labels
    y_hat_body = clf.predict(sample_X)

    # Calculate error of lrclf on y_body
    body_clf_accuracy = accuracy_score(y_body, y_hat_body)

    print classification_report(y_body, y_hat_body)

    print "\nBody Classification Accuracy: ", body_clf_accuracy, "\n"

    print '''
    PHASE II - Title Classification
    '''
    # Find all examples where y == "Title"
    title_class_idx = le.transform(['Title'])[0]
    title_idxs = np.where(sample_y==title_class_idx)

    # Prepare data for Phase II
    dp2 = DP2()
    new_X, new_y, non_b_idxs_by_doc = dp2.gen_new_feats(X, y, doc_idxs, all_text, body_class_idx, title_class_idx, none_class_idx, hv, all_bows, sample_original_idxs)

    sampled_idxs_by_doc = dp2.sampled_idxs_by_doc

    # Create empty array and fill w/ gold title tags
    y_title = empty_y.copy()
    y_title[title_idxs] = title_class_idx

    # Predict Title (Binary Prediction) w/ lrclf trained on
    # new_X and new_Y. new_x has new features from dp_phaseII
    # and new_Y has all sampled non_body_idxs where y=="Title"
    #W_title, b_title = lr_w.get_weights(new_X, new_y)

    #new_y_hat_title = clf.classify(new_X, W_title, b_title)

    clf = linear_model.LogisticRegression(C=1, penalty='l2', tol=1e-6, class_weight='auto')

    clf.fit(new_X, new_y)

    new_y_hat_title = clf.predict(new_X)

    title_clf_accuracy = accuracy_score(new_y, new_y_hat_title)

    probs = clf.predict_proba(new_X)

    # assert probs.shape == (new_X.shape[0],2)

    # # Choose highest scoring T from new_y_hat_title,
    # # create Y with predicted b's and predicted T's,
    # # and check accuracy against gold
    # y_hat_tb = y_body.copy()

    # ranges = list()
    # curr_idx = 0

    # for idx in range(0, len(sampled_idxs_by_doc)):
    #     ranges.append(curr_idx)
    #     curr_idx += len(sampled_idxs_by_doc[idx])

    # title_max = list()

    # for idx in range(len(ranges)):
    #     if (idx + 1 == len(ranges)):
    #         end = probs.size
    #     else:
    #         end = ranges[idx + 1]

    #     print probs[ranges[idx]:end][:][:][1]
    #     print np.argmax(probs[ranges[idx]:end][:][:][1])

    #     title_max.append(probs[ranges[idx]:end][:][1][1])

    # print title_max

    # doc = sampled_idxs_by_doc[idx]
    # doc_t_idxs = list()
    # doc_t_probs = list()
    # curr_non_b_idx = 0

    #     #print doc

    #     for node_idx in doc:
    #         doc_t_probs.append(probs[node_idx][:])

    #     print np.argmax(doc_t_probs[:][1])

    #     final_t = np.argmax(doc_t_probs)
    #     final_t_idx = doc_t_idxs(final_t) + doc_idxs[idx]
    #     y_hat_tb[final_t_idx] = title_class_idx

    print classification_report(new_y, new_y_hat_title)

    print "\nTitle Classification Accuracy: ", title_clf_accuracy, "\n"

    '''
    --------------------------------------------
          vvvvvvvvvvvv OUT OF DATE vvvvvvvvv
    --------------------------------------------
    '''

    # # Merge y_body and y_title
    # y_tb_gold = y_title.copy()
    # y_tb_gold[body_idxs] = body_class_idx

    # # Combine y_hat_body with gold title labels (y_hat_title_body)
    # y_tb_preds = y_hat_body.copy()
    # y_tb_preds[title_idxs] = title_class_idx


    # # Verify that new_X.shape[0] == y_t_non_b_gold.shape[0]
    # assert new_X.shape[0] == y_t_non_b_gold.shape[0]

    # # Predict Titles
    # W_t_no_b_gold, b_t_no_b_gold = lr_w.get_weights(y_t_non_b_gold)
    # y_hat_t_no_b = clf.classify(new_X, W_t_no_b_gold, b_t_no_b_gold)

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
