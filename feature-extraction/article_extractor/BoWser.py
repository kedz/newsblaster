# Bag of Words (BoW) Model for Chained Classifier
#
# Use BoW model to calculate cosine distances
# between predicted titles and all meta tags.
#
# Ramzi Abdoch

# Utilities
import sys
import os

# Beautiful Soup
from bs4 import BeautifulSoup

# Sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

# Numpy
import numpy as np

class BoWser():

    def __init__(self, all_metas, all_text):
        self.all_metas = all_metas
        self.all_text = all_text

    # Get BoW counts for each <meta> tag, grouped by document
    def get_counts(self):
        all_metas = self.all_metas
        all_text = self.all_text

        all_bows = list()

        # Num docs
        num_docs = len(all_metas)

        # Iterate through all docs
        for i in np.arange(0, num_docs):

            # Create BoW for each document

            # Check if there are any meta tags
            if all_metas[i] == []:
                # If not, add none_tuple to preserve order of docs
                none_tuple = (None, None, None)
                all_bows.append(none_tuple)
            else:
                cv = CountVectorizer(dtype=float)

                # Combine meta + text to get full doc
                full_doc = list(all_metas[i])
                full_doc.extend(all_text[i])

                # Train CountVectorizer on full_doc (so when we call .transform(text)
                # later, we can calculate cosine similarities and the vocabularies will be correct.)
                cv.fit(full_doc)

                # Get bows for meta tags (for cosine sim calculations)
                doc_meta_bows = cv.transform(all_metas[i])

                # Normalize counts (tf)
                normalize(doc_meta_bows, norm="l1", axis=1, copy=False)

                # Save tuple (BoWs for each <meta> in doc, CountVectorizer, text nodes for document)
                # Saving CV to transform candidate titles during Phase II of Chained CLFs
                bow = (doc_meta_bows, cv)
                all_bows.append(bow)

        return all_bows

if __name__ == "__main__":
    soups = list()

    # Get a soup for each article
    for f in os.listdir(sys.argv[1]):
        path = os.path.join(sys.argv[1], f)
        doc = open(path)

        soup = BeautifulSoup(doc)
        soups.append(soup)

    # Get all <meta> tags and text, grouped by document
    all_metas = list()
    all_text = list()

    for soup in soups:
        # Extract document <meta> tags for use in BoWser
        doc_metas = list()
        metas = soup.find_all("meta")

        if metas is not None:
            for tag in metas:
                meta_string = tag.get("content")

                if meta_string is None:
                    meta_string = ""

                # Append to doc_metas to keep track of which
                # metas appear in which document
                doc_metas.append(meta_string)

        # Append doc_mettas to all_metas
        all_metas.append(doc_metas)

        text_nodes = soup.find_all(text=True)
        all_text.append(text_nodes)

    jr = BoWser(all_metas, all_text)
    jr.get_counts()