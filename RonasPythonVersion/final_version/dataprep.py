import os
import math
import numpy as np
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
import json


class dataprep(object):
    def __init__(self, param_root_path, param_save_path):
        self.root_path = param_root_path
        self.save_path = param_save_path

    def data_prep(self):
        # stop_words
        stop_words_path = 'stopwordlist'
        stop_words_file = open(stop_words_path, 'r')
        stop_words_list = stop_words_file.read().splitlines()

        # list of document words
        list_of_docs = []
        list_doc_ids = []
        root_path = self.root_path
        documents_in_folder = os.listdir(root_path)
        documents_in_folder = sorted(documents_in_folder)
        doc_id = 0
        for document in documents_in_folder:
            with codecs.open(os.path.join(documents_path, document),
                             'r', 'utf-8', errors='replace') as f:
                document_text = u''.join(f.readlines())
                list_of_docs.append(document_text)
                list_doc_ids.append(document)

        # Create tfidfs
        tfidf = TfidfVectorizer(stop_words=stop_words_list,
                                norm=None, smooth_idf=False)
        tfidfs = tfidf.fit_transform(list_of_docs)

        # write tfidfs to file
        list_of_dicts = []
        transformed_matrix = tfidf.inverse_transform(tfidfs)
        feature_names = tfidf.get_feature_names()
        for i in range(0, len(transformed_matrix)):
            article = transformed_matrix[i]
            article_dict = {}
            for word in article:
                word_index = feature_names.index(word)
                article_dict[word] = tfidfs[i, word_index]
            list_of_dicts.append(article_dict)
        full_list = [list_of_dicts, list_doc_ids]
        with open(self.save_path, 'w') as outfile:
            json.dump(full_list, outfile)
