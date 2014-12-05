import sys
import os
import math 
import numpy as np
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction import DictVectorizer
from scipy.spatial.distance import cosine
import heapq
from heapq import heappush, heappop
import scipy.sparse
import random
import itertools
import json

def cosine_dis(sparse_matrix):
    return 1-pairwise_distances(sparse_matrix, metric="cosine")

def compute_all_doc_dis(cosine_dis):
    f = np.vectorize(compute_doc_dis)
    return f(cosine_dis)

def compute_doc_dis(cosine_dis_value):
    h = -3.247626 + 23.595831 * cosine_dis_value
    ex = math.e**h
    return ex / (1.0 + ex)

def compute_clust_sim(docs_dist, param_clust):
    if len(param_clust.docs) == 1:
        return 0
    sum_dist = 0.0
    num_comp = 0
    for i in range(0, len(param_clust.docs)):
        for j in range(i + 1, len(param_clust.docs)):
            sum_dist += docs_dist[param_clust.docs[i], param_clust.docs[j]]
            num_comp += 1
    return sum_dist / num_comp

def compute_new_clust_dis(docs_dist, clust1, clust2):
    num_docs = 0
    tot_docs_dist = 0
    for doc1 in clust1.docs:
        for doc2 in clust2.docs:
           num_docs += 1
           tot_docs_dist += docs_dist[doc1, doc2]
    return tot_docs_dist / num_docs

def compute_clust_dis(clust_dist, docs_dist, clust1, clust2):
    if clust1.clust_id > clust2.clust_id:
        print 'swapped'
        temp = clust1
        clust1 = clust2
        clust2 = temp
    print clust_dist
    print clust1.clust_id
    print clust2.clust_id
    print clust_dist[clust1.clust_id, clust2.clust_id]
    if (clust_dist[clust1.clust_id, clust2.clust_id] == 0):
        clust_dist[clust1.clust_id, clust2.clust_id] =  compute_new_clust_dis(docs_dist, clust1, clust2)
    return clust_dist[clust1.clust_id, clust2.clust_id]

def get_clust_dists(docs_dist, clust_dist, list_of_clusts):
    for i in range(0, len(list_of_clusts)):
        for j in range(i + 1, len(list_of_clusts)):
            clust_dist[list_of_clusts[i].clust_id,list_of_clusts[j].clust_id] = \
            compute_clust_dis(clust_dist, docs_dist, list_of_clusts[i], \
            list_of_clusts[j]) 
    return clust_dist

def merge_cluster_set(clusts_to_merge, docs_dist, clust_dist, threshold):
    merge_pairs = []
    for i in range(0, len(clusts_to_merge)):
        for j in range(i + 1, len(clusts_to_merge)):
            curr_dist = compute_clust_dis(clust_dist, docs_dist, clusts_to_merge[i], clusts_to_merge[j])
            if curr_dist > threshold:
                heappush(merge_pairs, (1-curr_dist, \
                clusts_to_merge[i], clusts_to_merge[j]))
    while merge_pairs:
        pair = heappop(merge_pairs)
        clust1 = pair[1]
        clust2 = pair[2]
        merged_result = merge_clust(clusts_to_merge, clust1, clust2, docs_dist, clust_dist)
        clust1 = merged_result[0]
        clusts_to_merge = merged_result[1]
        clust_dist = merged_result[2]
        merge_pairs = remove_affected_pairs(merge_pairs, clust1, clust2)
        for clust in clusts_to_merge:
            if clust.clust_id != clust1.clust_id:
                curr_dist = compute_clust_dis(clust_dist, docs_dist, clust1, clust) 
                if curr_dist > threshold:
                    if clust1.clust_id > clust.clust_id:
                        heappush(merge_pairs, (1-curr_dist, clust, clust1))
                    else:
                        heappush(merge_pairs, (1-curr_dist, clust1, clust))
    return clusts_to_merge, clust_dist

def merge_two_cluster_sets(clusts_to_merge, second_clusts_to_merge, docs_dist, clust_dist, threshold):
    merge_pairs = []
    for i in range(0, len(clusts_to_merge)):
        for j in range(0, len(second_clusts_to_merge)):
            curr_dist = compute_clust_dis(clust_dist, docs_dist, clusts_to_merge[i], second_clusts_to_merge[j])
            if curr_dist > threshold:
                heappush(merge_pairs, (1-curr_dist, \
                clusts_to_merge[i], second_clusts_to_merge[j]))
    clusts_to_merge = np.append(clusts_to_merge, second_clusts_to_merge)
    while merge_pairs:
        pair = heappop(merge_pairs)
        clust1 = pair[1]
        clust2 = pair[2]
        merged_result = merge_clust(clusts_to_merge, clust1, clust2, docs_dist, clust_dist)
        clust1 = merged_result[0]
        clusts_to_merge = merged_result[1]
        clust_dist = merged_result[2]
        merge_pairs = remove_affected_pairs(merge_pairs, clust1, clust2)
        for clust in clusts_to_merge:
            if clust.clust_id != clust1.clust_id:
                print 'here:',clust_dist
                print clust1.clust_id
                print clust.clust_id
                curr_dist = compute_clust_dis(clust_dist, docs_dist, clust1, clust) 
                if curr_dist > threshold:
                    if clust1.clust_id > clust.clust_id:
                        heappush(merge_pairs, (1-curr_dist, clust, clust1))
                    else:
                        heappush(merge_pairs, (1-curr_dist, clust1, clust))
    return clusts_to_merge, clust_dist

def remove_affected_pairs(merge_pairs, clust1, clust2):
    result_heap = []
    while  merge_pairs:
        pair = heappop(merge_pairs)
        if clust1.clust_id != pair[1].clust_id and \
           clust1.clust_id != pair[2].clust_id and \
           clust2.clust_id != pair[1].clust_id and \
           clust2.clust_id != pair[2].clust_id:
            heappush(result_heap, pair)
    return result_heap

def merge_clust(list_of_clusts, clust1, clust2, docs_dist, clust_dist):
    for clust in list_of_clusts:
        if clust.clust_id != clust1.clust_id and clust.clust_id != clust2.clust_id:
            dist_to_clust1 = compute_clust_dis(clust_dist, docs_dist, clust, clust1)
            dist_to_clust2 = compute_clust_dis(clust_dist, docs_dist, clust, clust2)
            if clust.clust_id < clust1.clust_id:
                clust_dist[clust.clust_id, clust1.clust_id] = merged_clust_dis(dist_to_clust1,\
                len(clust1.docs), dist_to_clust2, len(clust2.docs))
            else:
                clust_dist[clust1.clust_id, clust.clust_id] = merged_clust_dis(dist_to_clust1,\
                len(clust1.docs), dist_to_clust2, len(clust2.docs))
    clust1.docs = np.append(clust1.docs, clust2.docs)
    clust1.subclusts = np.append(clust1.subclusts, clust2.subclusts)
    for clust in list_of_clusts:
        if clust.clust_id == clust1.clust_id:
            clust = clust1
            break
    list_of_clusts = delete_clust(list_of_clusts, clust2)
    #clust_dist = np.delete(clust_dist, clust2.clust_id, 0)
    #clust_dist = np.delete(clust_dist, clust2.clust_id, 1)
    return clust1, list_of_clusts, clust_dist

def merged_clust_dis(dist_to_clust1, num_docs_clust1, dist_to_clust2, num_docs_clust2):
    return (dist_to_clust1 * num_docs_clust1 + dist_to_clust2 * num_docs_clust2) / (num_docs_clust1 + num_docs_clust2)

def delete_clust(list_of_clusts, del_clust):
    modified_list = []
    for clust in list_of_clusts:
        if clust.clust_id != del_clust.clust_id:
            modified_list.append(clust)
    return np.array(modified_list)

def display_clusts(docs_dist, list_doc_ids, list_of_clusts):
    for my_clust in list_of_clusts:
        print "###### Similarity: ", "{:.6f}".format(compute_clust_sim(docs_dist, my_clust)), " Superclustid: ", my_clust.clust_id
        display_clust(docs_dist, list_doc_ids, my_clust)

def display_clust(docs_dist, list_doc_ids, my_clust):
    for subclust in my_clust.subclusts:
        print "$$$$$$ Similarity: ", "{:.6f}".format(compute_clust_sim(docs_dist, subclust)), " Subclustid: ", subclust.clust_id
        for i in range(0, len(subclust.docs)):  
            print list_doc_ids[subclust.docs[i]]

def data_prep():
    #stop_words 
    stop_words_path = '/proj/nlp/users/Rona/stim2/dataprep/stopwordlist'
    stop_words_file = open(stop_words_path, 'r')
    stop_words_list = stop_words_file.read().splitlines()
    #list of document words
    list_of_docs = []
    list_doc_ids = []
    root_path = '/proj/nlp/users/Rona/stim2/rootdir'
    documents_folder = 'raw2/SmallArticles1'
    documents_path = os.path.join(root_path, documents_folder)
    documents_in_folder = os.listdir(documents_path)
    doc_id = 0
    for document in documents_in_folder:
        print document
        with codecs.open(os.path.join(documents_path, document), 'r', 'utf-8', errors='replace') as f:
            document_text = u''.join(f.readlines())
            list_of_docs.append(document_text)
            list_doc_ids.append(document)
    tfidf = TfidfVectorizer(stop_words=stop_words_list, norm=None, smooth_idf=False)
    tfidfs = tfidf.fit_transform(list_of_docs)
    print "Tfidf: \r\n", tfidfs 
    
    #write tfidfs to file
    list_of_dicts = []
    transformed_matrix = tfidf.inverse_transform(tfidfs);
    feature_names = tfidf.get_feature_names();    
    for i in range(0, len(transformed_matrix)):
        article = transformed_matrix[i]
        article_dict = {}
        for word in article:
            word_index = feature_names.index(word)
            article_dict[word] = tfidfs[i, word_index]
        list_of_dicts.append(article_dict)
    full_list = [list_of_dicts, list_doc_ids]
    save_file = os.path.join(root_path, 'save_matrix_b')
    with open(save_file, 'w') as outfile:
        json.dump(full_list, outfile)
    #End of Data Prep

def load_tfidfs(list_file):
    list_of_dicts = []
    list_doc_ids = []
    with open(list_file, 'r') as infile:
        full_list = json.load(infile)
        list_of_dicts = full_list[0]
        list_doc_ids = full_list[1]
    return list_of_dicts, list_doc_ids

def main():

    data_prep()
    
    #Start of Clustering
    exists_load_context = False
    load_context = ""
    exists_save_context = False
    save_context = ""
    segsize = 10000
    outfile = ""
    root_path = ""
    list_file = ""
    major_threshold = -1
    minor_threshold = -1

    for i in range(1, len(sys.argv), 2):
        tag = sys.argv[i]
        param = sys.argv[i + 1]
        if tag == '-l':
            exists_load_context = True
            load_context = param
        elif tag == '-s':
            exists_save_context = True
            save_context = param
        elif tag == '-i':
            seg_size = int(param)
        elif tag == '-r':
            root_path = param
        elif tag == '-f':
            list_file = param
        elif tag == '-T':
            major_threshold = float(param)
        elif tag == '-t':
            minor_threshold = float(param)
        elif tag == '-o':
            outfile = param
        else:
            print 'Unknown Tag: ',tag
    error = False
    if outfile == "":
        error = True
        print "Missing mandatory param: outfile"
    if root_path == "":
        error = True
        print "Missing mandatory param: root_dir"
    if list_file == "":
        error = True
        print "Missing mandatory param: list_file"
    if major_threshold > 1 or major_threshold < 0:
        error = True
        print "Invalid major threshold given - [0, 1]"
    if minor_threshold > 1 or minor_threshold < 0:
        error = True
        print "Invalid minor threshold given - [0, 1]"
    if error:
        sys.exit()
        
    list_of_dicts, list_doc_ids = load_tfidfs(list_file)
    all_doc_ids = list_doc_ids
    existing_clust = []
    num_clust = 0
    if exists_load_context:
        existing_clust, num_clust, file_name = load_clust(load_context,len(list_doc_ids))
        existing_list_of_dicts, existing_list_doc_ids = load_tfidfs(file_name)
        list_of_dicts = list_of_dicts + existing_list_of_dicts
        all_doc_ids = all_doc_ids + existing_list_doc_ids
    dict_vect = DictVectorizer()
    print list_of_dicts
    tfidfs = dict_vect.fit_transform(list_of_dicts)
    cosine_distance = cosine_dis(tfidfs)
    
    print "Cosine distance: \r\n", cosine_distance
    docs_dist = compute_all_doc_dis(cosine_distance)
    print "Docs distance: \r\n", docs_dist
    print 'After docs ids:', all_doc_ids
    display_clusts(docs_dist, all_doc_ids, existing_clust)

    list_of_clusts = []
    for i in range(0, len(list_doc_ids)):
        initialClust = clust([i], i + num_clust)
        list_of_clusts.append(initialClust)
    list_of_clusts = np.array(list_of_clusts)
    
    clusts_dist = np.zeros([list_of_clusts.shape[0] + len(existing_clust),list_of_clusts.shape[0] + len(existing_clust)])
    print type(list_of_clusts)
    print type(existing_clust)
    clusts_dist = get_clust_dists(docs_dist, clusts_dist, list_of_clusts.tolist()  + existing_clust) 

    print "Clust distance: \r\n", clusts_dist
    for i in range(0, int(math.ceil(len(list_of_clusts) * 1.0 /segsize))):
        current_list = []
        for j in range(0, segsize):    
            if i * 1.0 *segsize + j < len(list_of_clusts):
                current_list.append(list_of_clusts[i * 1.0 * segsize + j])
            else:
                break
        result = merge_cluster_set(current_list, docs_dist, clusts_dist, major_threshold)
        current_list = result[0]
        print 'current: '
        display_clusts(docs_dist, all_doc_ids, current_list)
        print current_list[0].docs
        clusts_dist = result[1]
        result = merge_two_cluster_sets(current_list, existing_clust, docs_dist, clusts_dist, major_threshold)
        existing_clust = result[0]
        clusts_dist = result[1]
    print 'existing: '
    display_clusts(docs_dist, all_doc_ids, existing_clust)
    print existing_clust[0].docs
    print "-----------------END FIRST MERGE------------------"

    for superclust in existing_clust:
        clusts_dist = np.zeros([len(superclust.docs), len(superclust.docs)])
        list_of_subclusts = []
        next_clust_id = 0
        for doc in superclust.docs:
            subclust = clust([doc], next_clust_id)
            list_of_subclusts.append(subclust)
            next_clust_id += 1
        list_of_subclusts = np.array(list_of_subclusts)
        subclusts = merge_cluster_set(list_of_subclusts, docs_dist, clusts_dist, minor_threshold)
        superclust.subclusts = subclusts[0]
    print "After Merge"
    display_clusts(docs_dist, all_doc_ids, existing_clust)

    if exists_save_context:
        with open(list_file, 'r') as outfile:
            to_file = [list_of_dicts, all_doc_ids]
            json.dumps(to_file, outfile)
        save_clust(existing_clust, list_file, save_context)

def load_clust(infile_name, offset):
    with open(infile_name, 'r') as infile:
        list_clust = json.load(infile)
        result = []
        for clust in list_clust[1]:
            result.append(create_clust_from_list(clust, offset))
        return result, len(list_clust[1]), list_clust[0]
        
def create_clust_from_list(list_clust, id_mod):
    docs = list_clust[0]
    docs = [int(doc) + id_mod for doc in docs]
    clust_id = int(list_clust[1])
    subclusts = []
    for subclust in list_clust[2]:
        sub_result = create_clust_from_list(subclust, id_mod)
        subclusts.append(sub_result)
    result_clust = clust(docs, clust_id)
    result_clust.set_subclusts(subclusts)
    return result_clust
        
def save_clust(clusts, file_name, outfile_name):
    list_clust = []
    for clust in clusts:
        list_clust.append(create_list_from_clust(clust))
    to_file = [file_name, list_clust]
    print to_file
    with open(outfile_name, 'w') as outfile:
        json.dump(to_file, outfile)

def create_list_from_clust(clust):
    clust_list = []
    docs = clust.docs.tolist()
    clust_id = clust.clust_id
    subclusts = []
    for subclust in clust.subclusts:
        subclusts.append(create_list_from_clust(subclust))
    return [docs, clust_id, subclusts]

class clust:
    def __init__(self, param_docs, param_clust_id):
        self.docs = np.array(param_docs)
        self.clust_id =  param_clust_id
        self.subclusts = np.array([])

    def set_distance(self, param_distances):
        self.dist = param_distances

    def set_subclusts(self, param_subclusts):
        self.subclusts = param_subclusts

    def set_doc_tfidfs(self, param_file):
        self.file_name = param_file
        
    def set_docs(self, param_docs):
        self.docs = np.array(param_docs)

if __name__ == u'__main__':
    main()
