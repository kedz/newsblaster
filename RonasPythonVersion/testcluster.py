import os
import math 
import numpy as np
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
import heapq
from heapq import heappush, heappop
import scipy.sparse
import random
import itertools

def nplusx(n):

    def plus_func(x):
        return n+x
    return plus_func

#def cluster(X, merge_thr, sc_merge_thr):
    #Do clustering here
    #Look at build_tokenizer 

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
        temp = clust1
        clust1 = clust2
        clust2 = temp
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
    clust_dist = np.delete(clust_dist, clust2.clust_id, 0)
    clust_dist = np.delete(clust_dist, clust2.clust_id, 1)
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
        print "###### Similarity: ", "{:.6f}".format(compute_clust_sim(docs_dist, my_clust)), " Superclustid: ", my_clust.clust_id, " *"
        display_clust(docs_dist, list_doc_ids, my_clust)

def display_clust(docs_dist, list_doc_ids, my_clust):
    for subclust in my_clust.subclusts:
        print "$$$$$$ Similarity: ", "{:.6f}".format(compute_clust_sim(docs_dist, subclust)), " Subclustid: ", subclust.clust_id, " *"
        for i in range(0, len(subclust.docs)):  
            print list_doc_ids[subclust.docs[i]], " *"


def main():
    #stop_words 
    stop_words_path = '/proj/nlp/users/Rona/stim2/dataprep/stopwordlist'
    stop_words_file = open(stop_words_path, 'r')
    stop_words_list = stop_words_file.read().splitlines()
    #list of document words
    list_of_docs = []
    list_doc_ids = []
    root_path = '/proj/nlp/users/Rona/stim2/rootdir'
    documents_folder = 'raw2/SmallArticles'
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
    tfidfs_coo = tfidfs.tocoo()
    write = False
    weights_path = os.path.join(root_path, 'weights')
    if not os.path.exists(weights_path):
        os.makedirs(weights_path)
    weight_doc = None
    previous_i = -1
    for i,j,d in itertools.izip(tfidfs_coo.row, tfidfs_coo.col, tfidfs_coo.data):
        if i != previous_i:
            previous_i = i
            if not weight_doc is None:
                weight_doc.close()
            document = list_doc_ids[i]
            weights_file = os.path.join(weights_path, document)
            write = False
            if not os.path.isfile(weights_file):
                write = True 
                weight_doc = file(weights_file, 'w')
            else:
                input_string = "File: " + str(weights_file) + " already exists. Overwrite? "
                overwrite = raw_input(input_string)
                if len(overwrite) > 0 and overwrite[0] == 'y':
                    write = True
                    weight_doc = file(weights_file, 'w')
        if write:
            to_write = str(tfidf.get_feature_names()[j]) + " " + str(d) + "\n" 
            weight_doc.write(to_write)
    if write:
        weight_doc.close()
    #for index in range(0, 26):
    #    print index, tfidf.get_feature_names()[index] 
    cosine_distance = cosine_dis(tfidfs)
    
    print "Cosine distance: \r\n", cosine_distance

    docs_dist = compute_all_doc_dis(cosine_distance)
    
    print "Docs distance: \r\n", docs_dist

    list_of_clusts = []
    for i in range(0, len(list_doc_ids)):
        initialClust = clust([i], i)
        list_of_clusts.append(initialClust)
    list_of_clusts = np.array(list_of_clusts)
    
    clusts_dist = np.zeros([list_of_clusts.shape[0],list_of_clusts.shape[0]])
    clusts_dist = get_clust_dists(docs_dist, clusts_dist, list_of_clusts)

    print "Clust distance: \r\n", clusts_dist
    
    for my_clust in list_of_clusts:
        print my_clust.docs
    result = merge_cluster_set(list_of_clusts, docs_dist, clusts_dist, 0.2)
    list_of_clusts = result[0]
    clusts_dist = result[1]
    print "-----------------END FIRST MERGE------------------"
    #previous_list_of_clusts = read_clusts_from_file(file_name)
    #list_of_clusts = np.append(list_of_clusts, previous_list_of_clusts)
    for superclust in list_of_clusts:
        clusts_dist = np.zeros([len(superclust.docs), len(superclust.docs)])
        next_clust_id = 0
        list_of_subclusts = []
        for doc in superclust.docs:
            subclust = clust([doc], next_clust_id)
            list_of_subclusts.append(subclust)
            next_clust_id += 1
        list_of_subclusts = np.array(list_of_subclusts)
        subclusts = merge_cluster_set(list_of_subclusts, docs_dist, clusts_dist, 0.5)
        superclust.subclusts = subclusts[0]
    print "After Merge"
    display_clusts(docs_dist, list_doc_ids, list_of_clusts)

    #d1 = X[0,:]
    #d2 = X[1,:].T

    #x = np.dot(d1, d2)
    #print x

    #for doc in list_of_docs:
        #print doc + "\n"


    #func = nplusx(5)
    #print func(4)

class clust:
    def __init__(self, param_docs, param_clust_id):
        self.docs = np.array(param_docs)
        self.clust_id =  param_clust_id
        self.subclusts = np.array([])

    def set_distance(self, param_distances):
        self.dist= param_distances

    def set_subclusts(self, param_subclusts):
        self.subclusts = param_subclusts
    
    def set_docs(self, param_docs):
        self.docs = np.array(param_docs)

if __name__ == u'__main__':
    main()
