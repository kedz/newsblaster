# Data Preparation for Chained Classifier, Phase II
# Author: Ramzi Abdoch

# Utiltities
import pickle
import sys
import os

# Sklearn DictVectorizer
from sklearn.feature_extraction import DictVectorizer

# Sklearn Label Encoder (to keep labels consistent)
from sklearn.preprocessing import LabelEncoder

# Numpy
import numpy as np
import numpy.ma as ma

class DP2():

    def __init__(self):
        pass

    # Generate features derived from initial predictions
    def gen_new_feats(X, y, doc_idxs, body_class_idx, hv):

        # Slice up y
        docs = list()

        # Get all docs except last
        for i in range(0, len(doc_idxs) - 1):
            X_doc = X[doc_idxs[i] : doc_idxs[i+1]]
            y_doc = y[doc_idxs[i] : doc_idxs[i+1]]
            new_doc = tuple(X_doc, y_doc)
            docs.append(new_doc)

        # Get last doc
        X_doc = X[doc_idxs[-1]:]
        y_doc = y[doc_idxs[-1]:]
        last_doc = tuple(X_doc, y_doc)
        docs.append(last_doc)

        # Initialize new example list
        new_X = list()
        non_b_idxs_by_doc = list()

        # Iterate through docs and add feat 1-5
        for doc in docs:

            X = doc[0]
            y = doc[1]

            # Find first b tag
            body_idxs = np.where(y == body_class_idx)
            non_body_idxs = np.where(y != body_class_idx)
            first_b_tag_idx = body_idxs[0]

            # Get Feature Dicts for each doc
            textn_feat_dicts = hv.inverse_transform(X)
            num_nodes = len(textn_feat_dicts)

            # Initiate vars for feat #4
            above_b_idx = 0
            below_b_idx = num_nodes
            min_dist_above = np.zeros(num_nodes)
            min_dist_below = np.zeros(num_nodes)

            max_dist = X.shape[0]

            for node_idx in range(0, len(feat_dicts)):

                if y[node_idx] == body_class_idx:
                    above_b_idx = node_idx
                else:
                    feat_dict = textn_feat_dicts[node_idx]

                    # feat1 : dist_from_first_b_tag
                    feat_dict['dist_first_b'] = node_idx - first_b_tag_idx / num_nodes

                    # feat2 : #_of_b_tags_above
                    b_idxs_lt_node = np.where(body_idxs < node_idx)
                    feat_dict['num_bs_above'] = len(b_idxs_lt_node) / num_nodes

                    # feat3 : #_of_b_tags_below
                    b_idxs_gt_node = np.where(body_idxs > node_idx)
                    feat_dict['num_bs_below'] = len(b_idxs_gt_node) / num_nodes

                    if (above_b_idx == 0):
                        min_above[node_idx] = max_dist
                    else:
                        min_above[node_idx] = node_idx - above_b_idx

            for node_idx in range(1, len(feat_dicts)):

                resolved_idx = (node_idx * -1) + num_nodes

                if (y[node_idx * -1] == body_class_idx):
                    below_b_idx = resolved_idx
                else:
                    if(below_b_idx == num_nodes):
                        min_below[resolved_idx] = max_dist
                    else:
                        min_below = below_b_idx - resolved_idx

                # feat4 : dist_to_closest_b
                if argmin(max_above[resolved_idx], max_below[resolved_idx]) == 0:
                    feat_dict['dist_to_closest_b'] = max_above[resolved_idx] / num_nodes
                else:
                    feat_dict['dist_to_closest_b'] = max_below[resolved_idx] / num_nodes

            # feat5 : cosine similarity btw BoW model for Title + all meta tags

            # Extend / Append results
            new_X.extend(feat_dict)
            non_b_idxs_by_doc.append(non_body_idxs)

        return new_x, non_b_idxs_by_doc

def usage():
    print """

    output:
        sorted set of class-conditional weights for each feature in the training set
    """

# Run the data preparation
if __name__ == "__main__":
    pass
