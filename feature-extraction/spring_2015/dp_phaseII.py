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
from sklearn.preprocessing import normalize

# Numpy
import numpy as np
import numpy.ma as ma
import numpy.linalg as LA

class DP2():

    def __init__(self):
        pass

    # Generate features derived from initial predictions
    def gen_new_feats(X, y, original_docs, body_class_idx, title_class_idx, hv, new_text):

        # Slice up X, y
        docs = list()

        # Get all docs except last
        for i in range(0, len(doc_idxs) - 1):
            X_doc = X[doc_idxs[i] : doc_idxs[i+1]]
            y_doc = y[doc_idxs[i] : doc_idxs[i+1]]
            bow_doc = bowser.all_bows[i]

            # Store documents as (X_doc, y_doc, text_doc) tuple
            new_doc = tuple(X_doc, y_doc, text_doc, bow_doc)
            docs.append(new_doc)

        # Get last doc
        X_doc = X[doc_idxs[-1]:]
        y_doc = y[doc_idxs[-1]:]
        text_doc = text[doc_idxs[-1]:]
        last_doc = tuple(X_doc, y_doc, text_doc)
        bow_cv_doc = bowser.all_bows[-1]
        docs.append(last_doc)

        # Initialize new example list
        new_X = list()
        non_b_idxs_by_doc = list()

        # Iterate through docs and add feat 1-5
        for doc in docs:

            X = doc[0]
            y = doc[1]
            text = doc[2]
            meta_bows = doc[3][0]
            cv = doc[3][1]

            # Isolate body_idxs, non_body_idxs
            body_idxs = np.where(y == body_class_idx)
            non_body_idxs = np.where(y != body_class_idx)

            # Find first b tag
            first_b_tag_idx = body_idxs[0]

            # Get Feature Dicts for each piece of text
            textn_feat_dicts = hv.inverse_transform(X)

            # Count number of examples in doc
            num_nodes = len(textn_feat_dicts)

            # Initiate vars for feat #4
            above_b_idx = 0
            below_b_idx = num_nodes
            min_dist_above = np.zeros(num_nodes)
            min_dist_below = np.zeros(num_nodes)

            max_dist = X.shape[0]

            # Iterate through examples
            for node_idx in range(0, len(textn_feat_dicts)):

                # If body tag,
                if y[node_idx] == body_class_idx:
                    above_b_idx = node_idx
                else:
                    feat_dict = textn_feat_dicts[node_idx].copy() # .copy() to preserve size of X

                    # feat1 : dist_from_first_b_tag, normalized
                    feat_dict['dist_first_b'] = (node_idx - first_b_tag_idx) / float(num_nodes)

                    # feat2 : #_of_b_tags_above, normalized
                    b_idxs_lt_node = np.where(body_idxs < node_idx)
                    feat_dict['num_bs_above'] = len(b_idxs_lt_node) / float(num_nodes)

                    # feat3 : #_of_b_tags_below
                    b_idxs_gt_node = np.where(body_idxs > node_idx)
                    feat_dict['num_bs_below'] = len(b_idxs_gt_node) / float(num_nodes)

                    # feat4 : max cosine similarity btw <meta> BoWs and text[node_idx]
                    candidate_text = text[node_idx]
                    candidate_count = cv.transform(candidate_text)

                    normalize(candidate_count, norm="l1", copy=False)

                    # Calculate cosine similarity between candidate text and all meta tags
                    similarities = list()

                    for bow in meta_bows:
                        sim = np.dot(candidate_count, bow) / (LA.norm(candidate_count) * LA.norm(bow))
                        similarities.append(sim)

                    # Get max
                    feat_dict['max_cos_sim'] = max(similarities)

                    # If we haven't seen a body tag yet, set above distance to max dist (effectively infinity)
                    if (above_b_idx == 0):
                        min_above[node_idx] = max_dist
                    else:
                        min_above[node_idx] = node_idx - above_b_idx

            # Iterate from the bottom up in similar fashion to get min dist below
            for node_idx in range(1, len(feat_dicts)):

                resolved_idx = (node_idx * -1) + num_nodes

                if (y[node_idx * -1] == body_class_idx):
                    below_b_idx = resolved_idx
                else:
                    if(below_b_idx == num_nodes):
                        min_below[resolved_idx] = max_dist
                    else:
                        min_below = below_b_idx - resolved_idx

                # feat5 : dist_to_closest_b
                if argmin(min_above[resolved_idx], min_below[resolved_idx]) == 0:
                    feat_dict['dist_to_closest_b'] = min_above[resolved_idx] / num_nodes
                else:
                    feat_dict['dist_to_closest_b'] = min_below[resolved_idx] / num_nodes

            # Extend / Append results
            new_X.extend(feat_dict)
            non_b_idxs_by_doc.append(non_body_idxs)

        return new_X, non_b_idxs_by_doc
