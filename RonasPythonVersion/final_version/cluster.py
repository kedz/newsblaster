from clust import clust
import numpy as np
from collections import namedtuple
import operator
import sys
import os
import math
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction import DictVectorizer
from scipy.spatial.distance import cosine
import heapq
from heapq import heappush, heappop
import scipy.sparse
import random
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer


class Cluster(object):
    def __init__(self, p_input_type, p_seg_size, p_maj_threshold,
                 p_min_threshold, p_labels=[], p_documents=[]):
        self.input_type = p_input_type
        self.seg_size = p_seg_size
        self.major_threshold = p_maj_threshold
        self.minor_threshold = p_min_threshold
        self.labels = p_labels
        self.documents = p_documents

    def fit(self, p_documents):
        original_len = len(self.documents)
        tfidfs = self.documents + p_documents
        if self.input_type == "file_path":
            tfidfs = self._data_prep(tfidfs)
        cosine_distance = self._cosine_dis(tfidfs)
        docs_dist = self._compute_all_doc_dis(cosine_distance)
            
        Clust = namedtuple('Clust', ['docs', 'clust_id', 'subclusts'])
        existing_clust = [] 
        if self.labels:
            existing_clust = self._create_clust_from_labels()
        
        list_of_clusts = []
        for i in range(0, len(p_documents)):
            initialClust = Clust([original_len + i], i + len(existing_clust), [])
            list_of_clusts.append(initialClust)
        
        # Fill in cluster distances
        clusts_dist = np.zeros([len(list_of_clusts) + len(existing_clust),
                               len(list_of_clusts) + len(existing_clust)])
        clusts_dist = self._get_clust_dists(docs_dist, clusts_dist,
                                           existing_clust + list_of_clusts)

        # Divide into segments if number of new documents
        # is greater than the specified segsize
        for i in range(0, int(math.ceil(len(list_of_clusts)
                                        * 1.0 / self.seg_size))):
            current_list = []
            for j in range(0, self.seg_size):
                if i * self.seg_size + j < len(list_of_clusts):
                    current_list.append(list_of_clusts[i *
                                        self.seg_size + j])
                else:
                    break
            # Cluster into superclusters
            result = self._merge_cluster_set(current_list, docs_dist,
                                            clusts_dist, self.major_threshold)
            current_list = result[0]
            clusts_dist = result[1]
            result = self._merge_two_cluster_sets(current_list, existing_clust,
                                                 docs_dist, clusts_dist,
                                                 self.major_threshold)
            existing_clust = result[0]
            clusts_dist = result[1]
        # Cluster superclusters into subclusters
        for i in range(0, len(existing_clust)):
            superclust = existing_clust[i]
            clusts_dist = np.zeros([len(superclust.docs),
                                    len(superclust.docs)])
            list_of_subclusts = []
            next_clust_id = 0
            for doc in superclust.docs:
                subclust = Clust([doc], next_clust_id, [])
                list_of_subclusts.append(subclust)
                next_clust_id += 1
            list_of_subclusts = list_of_subclusts
            subclusts = self._merge_cluster_set(list_of_subclusts, docs_dist,
                                               clusts_dist,
                                               self.minor_threshold)
            existing_clust[i] = Clust(superclust.docs, superclust.clust_id, subclusts[0])
        
        self.documents = self.documents + p_documents
        # Show result
        self._display_clusts(docs_dist, existing_clust)

        # Show labels
        self._create_labels(existing_clust)
        print self.documents
        print self.labels
        return self.labels
                        
    def predict(self, p_documents):
        results = np.zeros((len(p_documents),2))
        print results
        results[:, :] = -1
        print results
        for i in range(0, len(p_documents)):
            to_find_doc = p_documents[i]
            doc_index = self.documents.index(to_find_doc)
            if doc_index >= 0:            
                results[i,:] = self.labels[doc_index,:]
        return results

    def _data_prep(self, p_documents):
        # stop_words
        stop_words_path = 'stopwordlist'
        stop_words_file = open(stop_words_path, 'r')
        stop_words_list = stop_words_file.read().splitlines()

        # list of document words
        list_of_docs = []
        for document in p_documents:
            with codecs.open(document, 'r', 'utf-8', errors='replace') as f:
                document_text = u''.join(f.readlines())
                list_of_docs.append(document_text)
        # Create tfidfs
        tfidf = TfidfVectorizer(stop_words=stop_words_list,
                                norm=None, smooth_idf=False)
        tfidfs = tfidf.fit_transform(list_of_docs)
        return tfidfs

    def _create_clust(self):
        Clust = namedtuple('Clust', ['docs', 'clust_id', 'subclusts'])
        existing_clusts = []
        num_doc = 0
        for row in self.labels:
            superclust_id = row[0]
            subclust_id = row[1]
            added = False
            for i in range(0, len(existing_clusts)):
                superclust = existing_clusts[i]
                if superclust.id == superclust_id:
                    for j in range(0, len(superclust.subclusts)):
                        subclust = superclust.subclusts[j]
                        if subclust.id == subclust_id:
                            superclust.subclusts[j]  = Clust(subclust.docs + \
                                                             [num_doc],
                                                             subclust.clust_id,
                                                              subclust.subclusts)
                            existing_clusts[i] = superclust
                            added = True
                    if not added:
                        new_clust = Clust([numdoc],
                                          subclust_id, [])
                        existing_clust[i] = Clust(superclust.docs + [num_doc],
                                            superclust.clust_id,
                                            superclust.subclusts + [new_clust])
                        added = True
            if not added:
                new_subclust = Clust([numdoc], subclust_id, [])
                new_superclust = Clust([numdoc], superclust_id,
                                       [new_subclust])
                existing_clusts = existing_clusts + [new_superclust]
            num_doc = num_doc + 1
        return existing_clusts

    def _create_labels(self, existing_clust):
        new_labels = np.zeros((len(self.documents), 2))
        for i in range(0, len(existing_clust)):
            superclust = existing_clust[i]
            for super_doc in superclust.docs:
                new_labels[super_doc, 0] = superclust.clust_id
            for j in range(0, len(superclust.subclusts)):
                subclust = superclust.subclusts[j]
                for sub_doc in subclust.docs:
                    new_labels[sub_doc, 1] = subclust.clust_id
        self.labels = new_labels
            
    def _cosine_dis(self, sparse_matrix):
        # Calculate cosine distance
        return 1-pairwise_distances(sparse_matrix, metric="cosine")

    def _compute_all_doc_dis(self, cosine_dis):
        # Get cosine distance of every document pair
        f = np.vectorize(self._compute_doc_dis)
        return f(cosine_dis)

    def _compute_doc_dis(self, cosine_dis_value):
        # Get document distance
        h = -3.247626 + 23.595831 * cosine_dis_value
        ex = math.e**h
        return ex / (1.0 + ex)

    def _compute_clust_sim(self, docs_dist, param_clust):
        # Average document pair distances in cluster
        if len(param_clust.docs) == 1:
            return 0
        sum_dist = 0.0
        num_comp = 0
        for i in range(0, len(param_clust.docs)):
            for j in range(i + 1, len(param_clust.docs)):
                sum_dist += docs_dist[param_clust.docs[i], param_clust.docs[j]]
                num_comp += 1
        return sum_dist / num_comp

    def _compute_new_clust_dis(self, docs_dist, clust1, clust2):
        # Average of document pair distances
        # Where each pair must have one doc from clust1 and one from clust2
        num_docs = 0
        tot_docs_dist = 0
        for doc1 in clust1.docs:
            for doc2 in clust2.docs:
                num_docs += 1
                tot_docs_dist += docs_dist[doc1, doc2]
        return tot_docs_dist / num_docs

    def _compute_clust_dis(self, clust_dist, docs_dist, clust1, clust2):
        # Make clust1 the smaller of the two clust ids
        if clust1.clust_id > clust2.clust_id:
            temp = clust1
            clust1 = clust2
            clust2 = temp
        # Retrieve clust dist if already calculated, otherwise recalculate
        if (clust_dist[clust1.clust_id, clust2.clust_id] == 0):
            clust_dist[clust1.clust_id, clust2.clust_id] =  \
                self._compute_new_clust_dis(docs_dist, clust1, clust2)
        return clust_dist[clust1.clust_id, clust2.clust_id]

    def _get_clust_dists(self, docs_dist, clust_dist, list_of_clusts):
        # Populate the table of clust distances given a list of clusts
        for i in range(0, len(list_of_clusts)):
            for j in range(i + 1, len(list_of_clusts)):
                clust_dist[list_of_clusts[i].clust_id,
                           list_of_clusts[j].clust_id] = \
                    self._compute_clust_dis(clust_dist, docs_dist,
                                           list_of_clusts[i],
                                           list_of_clusts[j])
        return clust_dist

    def _merge_cluster_set(self, clusts_to_merge, docs_dist,
                          clust_dist, threshold):
        # Find all clust pairs that exceed the threshold req to merge
        # and add them to a heap (sorted by clust similarity)
        merge_pairs = []
        for i in range(0, len(clusts_to_merge)):
            for j in range(i + 1, len(clusts_to_merge)):
                curr_dist = self._compute_clust_dis(clust_dist, docs_dist,
                                                   clusts_to_merge[i],
                                                   clusts_to_merge[j])
                if curr_dist > threshold:
                    heappush(merge_pairs, (1-curr_dist,
                                           clusts_to_merge[i],
                                           clusts_to_merge[j]))
        # Merge the clust pairs that are now on the heap
        while merge_pairs:
            pair = heappop(merge_pairs)
            clust1 = pair[1]
            clust2 = pair[2]
            merged_result = self._merge_clust(clusts_to_merge, clust1, clust2,
                                             docs_dist, clust_dist)
            clust1 = merged_result[0]
            clusts_to_merge = merged_result[1]
            clust_dist = merged_result[2]
            # Remove pairs on heap that no longer exist because of the merge
            merge_pairs = self._remove_affected_pairs(merge_pairs,
                                                     clust1, clust2)
            # Calculate clust distances to this new heap
            for clust in clusts_to_merge:
                if clust.clust_id != clust1.clust_id:
                    curr_dist = self._compute_clust_dis(clust_dist, docs_dist,
                                                       clust1, clust)
                    # If the new clust dist meets the threshold, add to heap
                    if curr_dist > threshold:
                        if clust1.clust_id > clust.clust_id:
                            heappush(merge_pairs, (1-curr_dist, clust, clust1))
                        else:
                            heappush(merge_pairs, (1-curr_dist, clust1, clust))
        return clusts_to_merge, clust_dist

    def _merge_two_cluster_sets(self, clusts_to_merge, second_clusts_to_merge,
                               docs_dist, clust_dist, threshold):
        # Create pairs such that the first clust is in clusts_to_merge
        # and the second is in second_clusts_to_merge, see if the pairs meet
        # the required threshold, if so add them to a heap
        merge_pairs = []
        for i in range(0, len(clusts_to_merge)):
            for j in range(0, len(second_clusts_to_merge)):
                curr_dist = self._compute_clust_dis(clust_dist, docs_dist,
                                                   clusts_to_merge[i],
                                                   second_clusts_to_merge[j])
                if curr_dist > threshold:
                    heappush(merge_pairs, (1-curr_dist,
                                           clusts_to_merge[i],
                                           second_clusts_to_merge[j]))
        clusts_to_merge = clusts_to_merge + second_clusts_to_merge
        # Merge the pairs while there are still pairs on the heap
        while merge_pairs:
            pair = heappop(merge_pairs)
            clust1 = pair[1]
            clust2 = pair[2]
            merged_result = self._merge_clust(clusts_to_merge, clust1, clust2,
                                             docs_dist, clust_dist)
            clust1 = merged_result[0]
            clusts_to_merge = merged_result[1]
            clust_dist = merged_result[2]
            # Remove pairs from heap that no longer exist because of this merge
            merge_pairs = self._remove_affected_pairs(merge_pairs,
                                                     clust1, clust2)
            # Calculate new clust distances to this clust
            for clust in clusts_to_merge:
                if clust.clust_id != clust1.clust_id:
                    curr_dist = self._compute_clust_dis(clust_dist, docs_dist,
                                                       clust1, clust)
                    # If the new pair meets the threshold, add to heap
                    if curr_dist > threshold:
                        if clust1.clust_id > clust.clust_id:
                            heappush(merge_pairs, (1-curr_dist, clust, clust1))
                        else:
                            heappush(merge_pairs, (1-curr_dist, clust1, clust))
        return clusts_to_merge, clust_dist

    def _delete_clust(self, list_of_clusts, del_clust):
        # Deletes a clust from the given list based on clust_id
        modified_list = []
        for clust in list_of_clusts:
            if clust.clust_id != del_clust.clust_id:
                modified_list.append(clust)
        return modified_list

    def _remove_affected_pairs(self, merge_pairs, clust1, clust2):
        # Makes sure the pairs in merge pairs do no contain clust1 or clust2
        # If it does, remove the pair containing either clust1 or clust2
        result_heap = []
        while merge_pairs:
            pair = heappop(merge_pairs)
            if clust1.clust_id != pair[1].clust_id and \
               clust1.clust_id != pair[2].clust_id and \
               clust2.clust_id != pair[1].clust_id and \
               clust2.clust_id != pair[2].clust_id:
                heappush(result_heap, pair)
        return result_heap

    def _merge_clust(self, list_of_clusts, clust1, clust2,
                    docs_dist, clust_dist):
        # Compute clust distances to this new pair
        for clust in list_of_clusts:
            if clust.clust_id != clust1.clust_id and \
               clust.clust_id != clust2.clust_id:
                dist_to_clust1 = self._compute_clust_dis(clust_dist, docs_dist,
                                                        clust, clust1)
                dist_to_clust2 = self._compute_clust_dis(clust_dist, docs_dist,
                                                        clust, clust2)
                if clust.clust_id < clust1.clust_id:
                    clust_dist[clust.clust_id, clust1.clust_id] = \
                        self._merged_clust_dis(dist_to_clust1, len(clust1.docs),
                                              dist_to_clust2, len(clust2.docs))
                else:
                    clust_dist[clust1.clust_id, clust.clust_id] = \
                        self._merged_clust_dis(dist_to_clust1,
                                              len(clust1.docs), dist_to_clust2,
                                              len(clust2.docs))
        # Combine the documents and subclusters of the two clusts
        Clust = namedtuple('Clust', ['docs', 'clust_id', 'subclusts'])
        clust1 = Clust(clust1.docs + clust2.docs, clust1.clust_id, clust1.subclusts + clust2.subclusts)
        # Update the new clust in list of clusts
        for i in range(0, len(list_of_clusts)):
            current_clust = list_of_clusts[i]
            if current_clust.clust_id == clust1.clust_id:
                list_of_clusts[i] = clust1
                break
        # Remove the second clust
        list_of_clusts = self._delete_clust(list_of_clusts, clust2)
        return clust1, list_of_clusts, clust_dist

    def _merged_clust_dis(self, dist_to_clust1, num_docs_clust1, dist_to_clust2,
                         num_docs_clust2):
        # Calculate merge distance
        return (dist_to_clust1 * num_docs_clust1 + dist_to_clust2 *
                num_docs_clust2) / (num_docs_clust1 + num_docs_clust2)

    def _display_clusts(self, docs_dist, list_of_clusts):
        for my_clust in list_of_clusts:
            print "###### Similarity: ", \
                "{:.6f}".format(self._compute_clust_sim(
                                docs_dist, my_clust)), \
                " Superclustid: ", my_clust.clust_id
            self._display_clust(docs_dist, my_clust)

    def _display_clust(self, docs_dist, my_clust):
        for subclust in my_clust.subclusts:
            print "$$$$$$ Similarity: ", \
                "{:.6f}".format(self._compute_clust_sim(
                                docs_dist, subclust)), \
                " Subclustid: ", subclust.clust_id
            for i in range(0, len(subclust.docs)):
                print self.documents[subclust.docs[i]]
    

    
