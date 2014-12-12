import numpy as np


class clust(object):
    def __init__(self, param_docs, param_clust_id):
        self.docs = np.array(param_docs)
        self.clust_id = param_clust_id
        self.subclusts = np.array([])

    def set_distance(self, param_distances):
        self.dist = param_distances

    def set_subclusts(self, param_subclusts):
        self.subclusts = param_subclusts

    def set_doc_tfidfs(self, param_file):
        self.file_name = param_file

    def set_docs(self, param_docs):
        self.docs = np.array(param_docs)
