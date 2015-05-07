# Data Preparation for Chained Classifier, Phase II
# Author: Ramzi Abdoch

# Utiltities
import pickle
import sys
import os

# Sklearn DictVectorizer
from sklearn.feature_extraction import DictVectorizer

# SciKit Learn (to keep labels consistent)
from sklearn.preprocessing import LabelEncoder

# SciKit Learn utiltities for calculating dist btw text and meta tags
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

# Numpy
import numpy as np
import numpy.ma as ma
import numpy.linalg as LA

class DP2():

    def __init__(self):
        pass

    # Generate features derived from initial predictions
    def gen_new_feats(self, X, y, doc_idxs, text, body_class_idx, title_class_idx, none_class_idx, hv, all_bows, original_idxs):

        # Slice up X, y
        docs = list()

        # Get all docs except last
        for i in range(len(doc_idxs) - 1):
            X_doc = X[doc_idxs[i] : doc_idxs[i+1]]
            y_doc = y[doc_idxs[i] : doc_idxs[i+1]]
            text_doc = text[doc_idxs[i] : doc_idxs[i+1]]
            bow_doc = all_bows[i]

            # Store documents as (X_doc, y_doc, text_doc) tuple
            new_doc = (X_doc, y_doc, text_doc, bow_doc)
            docs.append(new_doc)

        # Get last doc
        X_doc = X[doc_idxs[-1]:]
        y_doc = y[doc_idxs[-1]:]
        text_doc = text[doc_idxs[-1]:]
        bow_doc = all_bows[-1]
        last_doc = (X_doc, y_doc, text_doc, bow_doc)
        bow_cv_doc = all_bows[-1]
        docs.append(last_doc)

        # Initialize new example list
        new_X = list()
        new_y = list()
        non_b_idxs_by_doc = list()
        sampled_idxs_by_doc = list()

        # Iterate through docs and add feat 1-5
        for idx in range(len(docs)):

            X_doc = docs[idx][0]
            y_doc = docs[idx][1]
            text_doc = docs[idx][2]
            meta_bows_doc = docs[idx][3][0]
            cv_doc = docs[idx][3][1]

            # Isolate body_idxs, non_body_idxs
            body_idxs = np.where(y_doc == body_class_idx)
            non_body_idxs = np.where(y_doc != body_class_idx)

            # Find first b tag
            first_b_tag_idx = body_idxs[0][0]

            # Get Feature Dicts for each piece of text
            textn_feat_dicts = hv.inverse_transform(X_doc)

            # Count number of examples in doc
            num_nodes = len(textn_feat_dicts)

            # Initiate vars for feat #4
            above_b_idx = 0
            below_b_idx = num_nodes
            min_above = np.zeros(num_nodes)
            min_below = np.zeros(num_nodes)

            max_dist = X.shape[0]

            sampled_idxs = list()
            doc_feats = list()

            # Iterate through examples
            for node_idx in range(len(textn_feat_dicts)):
                # If body tag,
                if y[node_idx] == body_class_idx:
                    above_b_idx = node_idx
                else:
                    # Check if example is sampled from LR_Weights
                    if (doc_idxs[idx] + node_idx) in original_idxs:
                        feat_dict = textn_feat_dicts[node_idx].copy() # .copy() to preserve size of X

                        # feat1 : dist_from_first_b_tag, normalized
                        feat_dict['dist_first_b'] = (node_idx - first_b_tag_idx) / float(num_nodes)

                        # feat2 : #_of_b_tags_above, normalized
                        b_idxs_lt_node = np.where(body_idxs < node_idx)
                        feat_dict['num_bs_above'] = len(b_idxs_lt_node) / float(num_nodes)

                        # feat3 : #_of_b_tags_below, normalized
                        b_idxs_gt_node = np.where(body_idxs > node_idx)
                        feat_dict['num_bs_below'] = len(b_idxs_gt_node) / float(num_nodes)

                          # feat4 : max cosine similarity btw <meta> BoWs and text[node_idx]
                        if(cv_doc is not None):
                            candidate_text = text_doc[node_idx]
                            candidate_bow = cv_doc.transform(candidate_text)[0]

                            #normalize(candidate_bow, norm="l1", axis=1, copy=False)

                            # Calculate cosine similarity between candidate text and all meta tags
                            similarities = list()

                            similarities = cosine_similarity(candidate_bow, meta_bows_doc)

                            #print max(similarities[0])

                            # Get max
                            feat_dict['max_cos_sim'] = max(similarities[0])
                        else:
                            # If there are no meta tags, set all cosine sims to least value, -1
                            feat_dict['max_cos_sim'] = -1.0

                        # If we haven't seen a body tag yet, set above distance to max dist (effectively infinity)
                        if (above_b_idx == 0):
                            min_above[node_idx] = max_dist
                        else:
                            min_above[node_idx] = node_idx - above_b_idx

                        doc_feats.append(feat_dict)

                        if y_doc[node_idx] == title_class_idx:
                            new_y.append(y_doc[node_idx])
                        else:
                            new_y.append(none_class_idx)

                        sampled_idxs.append(node_idx)

            # Iterate from the bottom up in similar fashion to get min dist below
            for node_idx in range(1, len(textn_feat_dicts)):

                resolved_idx = (node_idx * -1) + num_nodes

                if (y[node_idx * -1] == body_class_idx):
                    below_b_idx = resolved_idx
                else:
                    # Check if example is sampled from LR_Weights
                    if (doc_idxs[idx] + resolved_idx) in original_idxs:
                        if(below_b_idx == num_nodes):
                            min_below[resolved_idx] = max_dist
                        else:
                            min_below[resolved_idx] = below_b_idx - resolved_idx

            # Iterate through doc_feats to add fifth feature
            for node_idx in range(len(sampled_idxs)):
                features = doc_feats[node_idx]
                feat_idx = sampled_idxs[node_idx]

                # feat5 : dist_to_closest_b
                if np.argmin([min_above[feat_idx], min_below[feat_idx]]) == 0:
                    features['dist_to_closest_b'] = min_above[feat_idx] / num_nodes
                else:
                    features['dist_to_closest_b'] = min_below[feat_idx] / num_nodes

            # Extend / Append results
            new_X.extend(doc_feats)
            non_b_idxs_by_doc.append(non_body_idxs)
            sampled_idxs_by_doc.append(sampled_idxs)

        self.sampled_idxs_by_doc = sampled_idxs_by_doc
        new_X = DictVectorizer().fit_transform(new_X)
        new_y = np.array(new_y)
        return new_X, new_y, non_b_idxs_by_doc
