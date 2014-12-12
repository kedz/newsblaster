from clust import clust
import numpy as np
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
import json


class clustering(object):
    def __init__(self, p_load_context, p_save_context, p_segsize,
                 p_list_file, p_major_threshold,
                 p_minor_threshold):
        self.load_context = p_load_context
        self.save_context = p_save_context
        self.segsize = p_segsize
        self.list_file = p_list_file
        self.major_threshold = p_major_threshold
        self.minor_threshold = p_minor_threshold
        self.exists_load_context = False
        self.exists_save_context = False
        if not self.load_context == "":
            self.exists_load_context = True
        if not self.save_context == "":
            self.exists_save_context = True

    def cosine_dis(self, sparse_matrix, list_of_dicts):
        # Calculate cosine distance
        return 1-pairwise_distances(sparse_matrix, metric="cosine")

    def compute_all_doc_dis(self, cosine_dis):
        # Get cosine distance of every document pair
        f = np.vectorize(self.compute_doc_dis)
        return f(cosine_dis)

    def compute_doc_dis(self, cosine_dis_value):
        # Get document distance
        h = -3.247626 + 23.595831 * cosine_dis_value
        ex = math.e**h
        return ex / (1.0 + ex)

    def compute_clust_sim(self, docs_dist, param_clust):
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

    def compute_new_clust_dis(self, docs_dist, clust1, clust2):
        # Average of document pair distances
        # Where each pair must have one doc from clust1 and one from clust2
        num_docs = 0
        tot_docs_dist = 0
        for doc1 in clust1.docs:
            for doc2 in clust2.docs:
                num_docs += 1
                tot_docs_dist += docs_dist[doc1, doc2]
        return tot_docs_dist / num_docs

    def compute_clust_dis(self, clust_dist, docs_dist, clust1, clust2):
        # Make clust1 the smaller of the two clust ids
        if clust1.clust_id > clust2.clust_id:
            temp = clust1
            clust1 = clust2
            clust2 = temp
        # Retrieve clust dist if already calculated, otherwise recalculate
        if (clust_dist[clust1.clust_id, clust2.clust_id] == 0):
            clust_dist[clust1.clust_id, clust2.clust_id] =  \
                self.compute_new_clust_dis(docs_dist, clust1, clust2)
        return clust_dist[clust1.clust_id, clust2.clust_id]

    def get_clust_dists(self, docs_dist, clust_dist, list_of_clusts):
        # Populate the table of clust distances given a list of clusts
        for i in range(0, len(list_of_clusts)):
            for j in range(i + 1, len(list_of_clusts)):
                clust_dist[list_of_clusts[i].clust_id,
                           list_of_clusts[j].clust_id] = \
                    self.compute_clust_dis(clust_dist, docs_dist,
                                           list_of_clusts[i],
                                           list_of_clusts[j])
        return clust_dist

    def merge_cluster_set(self, clusts_to_merge, docs_dist,
                          clust_dist, threshold):
        # Find all clust pairs that exceed the threshold req to merge
        # and add them to a heap (sorted by clust similarity)
        merge_pairs = []
        for i in range(0, len(clusts_to_merge)):
            for j in range(i + 1, len(clusts_to_merge)):
                curr_dist = self.compute_clust_dis(clust_dist, docs_dist,
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
            merged_result = self.merge_clust(clusts_to_merge, clust1, clust2,
                                             docs_dist, clust_dist)
            clust1 = merged_result[0]
            clusts_to_merge = merged_result[1]
            clust_dist = merged_result[2]
            # Remove pairs on heap that no longer exist because of the merge
            merge_pairs = self.remove_affected_pairs(merge_pairs,
                                                     clust1, clust2)
            # Calculate clust distances to this new heap
            for clust in clusts_to_merge:
                if clust.clust_id != clust1.clust_id:
                    curr_dist = self.compute_clust_dis(clust_dist, docs_dist,
                                                       clust1, clust)
                    # If the new clust dist meets the threshold, add to heap
                    if curr_dist > threshold:
                        if clust1.clust_id > clust.clust_id:
                            heappush(merge_pairs, (1-curr_dist, clust, clust1))
                        else:
                            heappush(merge_pairs, (1-curr_dist, clust1, clust))
        return clusts_to_merge, clust_dist

    def merge_two_cluster_sets(self, clusts_to_merge, second_clusts_to_merge,
                               docs_dist, clust_dist, threshold):
        # Create pairs such that the first clust is in clusts_to_merge
        # and the second is in second_clusts_to_merge, see if the pairs meet
        # the required threshold, if so add them to a heap
        merge_pairs = []
        for i in range(0, len(clusts_to_merge)):
            for j in range(0, len(second_clusts_to_merge)):
                curr_dist = self.compute_clust_dis(clust_dist, docs_dist,
                                                   clusts_to_merge[i],
                                                   second_clusts_to_merge[j])
                if curr_dist > threshold:
                    heappush(merge_pairs, (1-curr_dist,
                                           clusts_to_merge[i],
                                           second_clusts_to_merge[j]))
        clusts_to_merge = np.append(clusts_to_merge, second_clusts_to_merge)
        # Merge the pairs while there are still pairs on the heap
        while merge_pairs:
            pair = heappop(merge_pairs)
            clust1 = pair[1]
            clust2 = pair[2]
            merged_result = self.merge_clust(clusts_to_merge, clust1, clust2,
                                             docs_dist, clust_dist)
            clust1 = merged_result[0]
            clusts_to_merge = merged_result[1]
            clust_dist = merged_result[2]
            # Remove pairs from heap that no longer exist because of this merge
            merge_pairs = self.remove_affected_pairs(merge_pairs,
                                                     clust1, clust2)
            # Calculate new clust distances to this clust
            for clust in clusts_to_merge:
                if clust.clust_id != clust1.clust_id:
                    curr_dist = self.compute_clust_dis(clust_dist, docs_dist,
                                                       clust1, clust)
                    # If the new pair meets the threshold, add to heap
                    if curr_dist > threshold:
                        if clust1.clust_id > clust.clust_id:
                            heappush(merge_pairs, (1-curr_dist, clust, clust1))
                        else:
                            heappush(merge_pairs, (1-curr_dist, clust1, clust))
        return clusts_to_merge, clust_dist

    def delete_clust(self, list_of_clusts, del_clust):
        # Deletes a clust from the given list based on clust_id
        modified_list = []
        for clust in list_of_clusts:
            if clust.clust_id != del_clust.clust_id:
                modified_list.append(clust)
        return np.array(modified_list)

    def remove_affected_pairs(self, merge_pairs, clust1, clust2):
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

    def merge_clust(self, list_of_clusts, clust1, clust2,
                    docs_dist, clust_dist):
        # Compute clust distances to this new pair
        for clust in list_of_clusts:
            if clust.clust_id != clust1.clust_id and \
               clust.clust_id != clust2.clust_id:
                dist_to_clust1 = self.compute_clust_dis(clust_dist, docs_dist,
                                                        clust, clust1)
                dist_to_clust2 = self.compute_clust_dis(clust_dist, docs_dist,
                                                        clust, clust2)
                if clust.clust_id < clust1.clust_id:
                    clust_dist[clust.clust_id, clust1.clust_id] = \
                        self.merged_clust_dis(dist_to_clust1, len(clust1.docs),
                                              dist_to_clust2, len(clust2.docs))
                else:
                    clust_dist[clust1.clust_id, clust.clust_id] = \
                        self.merged_clust_dis(dist_to_clust1,
                                              len(clust1.docs), dist_to_clust2,
                                              len(clust2.docs))
        # Combine the documents and subclusters of the two clusts
        clust1.docs = np.append(clust1.docs, clust2.docs)
        clust1.subclusts = np.append(clust1.subclusts, clust2.subclusts)
        # Update the new clust in list of clusts
        for clust in list_of_clusts:
            if clust.clust_id == clust1.clust_id:
                clust = clust1
                break
        # Remove the second clust
        list_of_clusts = self.delete_clust(list_of_clusts, clust2)
        return clust1, list_of_clusts, clust_dist

    def merged_clust_dis(self, dist_to_clust1, num_docs_clust1, dist_to_clust2,
                         num_docs_clust2):
        # Calculate merge distance
        return (dist_to_clust1 * num_docs_clust1 + dist_to_clust2 *
                num_docs_clust2) / (num_docs_clust1 + num_docs_clust2)

    def display_clusts(self, docs_dist, list_doc_ids, list_of_clusts):
        for my_clust in list_of_clusts:
            print "###### Similarity: ", \
                "{:.6f}".format(self.compute_clust_sim(
                                docs_dist, my_clust)), \
                " Superclustid: ", my_clust.clust_id
            self.display_clust(docs_dist, list_doc_ids, my_clust)

    def display_clust(self, docs_dist, list_doc_ids, my_clust):
        for subclust in my_clust.subclusts:
            print "$$$$$$ Similarity: ", \
                "{:.6f}".format(self.compute_clust_sim(
                                docs_dist, subclust)), \
                " Subclustid: ", subclust.clust_id
            for i in range(0, len(subclust.docs)):
                print list_doc_ids[subclust.docs[i]]

    def load_tfidfs(self, list_file):
        list_of_dicts = []
        list_doc_ids = []
        with open(list_file, 'r') as infile:
            full_list = json.load(infile)
            list_of_dicts = full_list[0]
            list_doc_ids = full_list[1]
        return list_of_dicts, list_doc_ids

    def load_clust(self, infile_name, offset):
        with open(infile_name, 'r') as infile:
            list_clust = json.load(infile)
            result = []
            for clust in list_clust[1]:
                result.append(self.create_clust_from_list(clust, offset))
            return result, len(list_clust[1]), list_clust[0]

    def create_clust_from_list(self, list_clust, id_mod):
        docs = list_clust[0]
        docs = [int(doc) + id_mod for doc in docs]
        clust_id = int(list_clust[1])
        subclusts = []
        for subclust in list_clust[2]:
            sub_result = self.create_clust_from_list(subclust, id_mod)
            subclusts.append(sub_result)
        result_clust = clust(docs, clust_id)
        result_clust.set_subclusts(subclusts)
        return result_clust

    def save_clust(self, clusts, file_name, outfile_name):
        list_clust = []
        for clust in clusts:
            list_clust.append(self.create_list_from_clust(clust))
        to_file = [file_name, list_clust]
        with open(outfile_name, 'w') as outfile:
            json.dump(to_file, outfile)

    def create_list_from_clust(self, clust):
        clust_list = []
        docs = clust.docs.tolist()
        clust_id = clust.clust_id
        subclusts = []
        for subclust in clust.subclusts:
            subclusts.append(self.create_list_from_clust(subclust))
        return [docs, clust_id, subclusts]

    def cluster(self):
        # Get new documents
        list_of_dicts, list_doc_ids = self.load_tfidfs(self.list_file)

        # Get old cluster
        all_doc_ids = list_doc_ids
        existing_clust = []
        num_clust = 0
        if self.exists_load_context:
            existing_clust, num_clust, file_name = \
                self.load_clust(self.load_context, len(list_doc_ids))
            existing_list_of_dicts, existing_list_doc_ids = \
                self.load_tfidfs(file_name)
            list_of_dicts = list_of_dicts + existing_list_of_dicts
            all_doc_ids = all_doc_ids + existing_list_doc_ids

        # Get only first 101 words (copying old Newsblaster)
        for i in range(0, len(list_of_dicts)):
            dic = list_of_dicts[i]
            sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))
            j = 0
            new_dic = {}
            while j < 101 and j < len(sorted_dic):
                new_dic[sorted_dic[len(sorted_dic) - j - 1][0]] = \
                    sorted_dic[len(sorted_dic) - j - 1][1]
                j += 1
            list_of_dicts[i] = new_dic

        # Process tfidfs to documents distance
        dict_vect = DictVectorizer()
        tfidfs = dict_vect.fit_transform(list_of_dicts)
        cosine_distance = self.cosine_dis(tfidfs, list_of_dicts)
        docs_dist = self.compute_all_doc_dis(cosine_distance)

        # Make new documents into separate clusters
        list_of_clusts = []
        for i in range(0, len(list_doc_ids)):
            initialClust = clust([i], i + num_clust)
            list_of_clusts.append(initialClust)
        list_of_clusts = np.array(list_of_clusts)

        # Fill in cluster distances
        clusts_dist = np.zeros([list_of_clusts.shape[0] + len(existing_clust),
                               list_of_clusts.shape[0] + len(existing_clust)])
        clusts_dist = self.get_clust_dists(docs_dist, clusts_dist,
                                           list_of_clusts.tolist()
                                           + existing_clust)

        # Divide into segments if number of new documents
        # is greater than the specified segsize
        for i in range(0, int(math.ceil(len(list_of_clusts)
                                        * 1.0 / self.segsize))):
            current_list = []
            for j in range(0, self.segsize):
                if i * 1.0 * self.segsize + j < len(list_of_clusts):
                    current_list.append(list_of_clusts[i * 1.0 *
                                        self.segsize + j])
                else:
                    break
            # Cluster into superclusters
            result = self.merge_cluster_set(current_list, docs_dist,
                                            clusts_dist, self.major_threshold)
            current_list = result[0]
            clusts_dist = result[1]
            result = self.merge_two_cluster_sets(current_list, existing_clust,
                                                 docs_dist, clusts_dist,
                                                 self.major_threshold)
            existing_clust = result[0]
            clusts_dist = result[1]
        # Cluster superclusters into subclusters
        for superclust in existing_clust:
            clusts_dist = np.zeros([len(superclust.docs),
                                    len(superclust.docs)])
            list_of_subclusts = []
            next_clust_id = 0
            for doc in superclust.docs:
                subclust = clust([doc], next_clust_id)
                list_of_subclusts.append(subclust)
                next_clust_id += 1
            list_of_subclusts = np.array(list_of_subclusts)
            subclusts = self.merge_cluster_set(list_of_subclusts, docs_dist,
                                               clusts_dist,
                                               self.minor_threshold)
            superclust.subclusts = subclusts[0]

        # Show result
        self.display_clusts(docs_dist, all_doc_ids,
                            existing_clust)

        # Save result to file
        if self.exists_save_context:
            with open(self.list_file, 'r') as output_file:
                to_file = [list_of_dicts, all_doc_ids]
                json.dumps(to_file, output_file)
            self.save_clust(existing_clust, self.list_file, self.save_context)
