from datetime import datetime
import os
import sys
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sumpy

# Import local modules
module_path = os.path.dirname(os.path.realpath(__file__))
datastore_module = os.path.join(module_path, os.path.join(
    '..' + os.sep + 'datastore'))
sys.path.append(datastore_module)
from mongo import MongoStore


def summarize_clusters_lexrank():

    ms = MongoStore()

    clusters = ms.get_pending_clusters()
    for cluster in clusters:
        retrieve_ids = [aid for aid, sim in cluster["articles"] if sim > .55]
        articles = ms.get_articles_from_ids(retrieve_ids)
        art_texts = [a["text_content"].replace(u"\u201D", u"\"").replace(
            u"\u201C", u"\"") for a in articles]

        summary = sumpy.lexrank(art_texts)
        sents = []

        for x, row in summary._df.head(5).iterrows():
            s = {"article_id": articles[row["doc id"]]["_id"],
                 "sentence_id": row["sent id"],
                 "text": row["sent text"]}
            sents.append(s)

        summary_map = {"sentences": sents, "cluster_id": cluster["_id"],
                       "summary_type": "lexrank",
                       "date": datetime.now()}

        if ms.insert_summary(summary_map):
            ms.set_summarized_flag(cluster)


if __name__ == '__main__':
    summarize_clusters_lexrank()
