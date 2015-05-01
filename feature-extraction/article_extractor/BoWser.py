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

    def __init__(self, all_metas):
        self.all_metas = all_metas

    # Get BoW counts for each <meta> tag, grouped by document
    def get_counts(self):
        all_bows = list()

        # Iterate through each doc
        for doc in self.all_metas:

            # Create BoW for each document

            # Check if there are any meta tags
            if not doc:
                # If not, add none_tuple to preserve order of docs
                none_tuple = (None, None)
                all_bows.append(none_tuple)
            else:
                cv = CountVectorizer(dtype=float)

                doc_bow = cv.fit_transform(doc)

                # Normalize counts (tf)
                normalize(doc_bow, norm="l1", axis=1, copy=False)

                # Save tuple (BoWs for each <meta> in doc, CountVectorizer)
                # Saving CV to transform candidate titles during Phase II of
                # Chained CLFs
                bow_and_cv = (doc_bow, cv)
                all_bows.append(bow_and_cv)

        self.all_bows = all_bows

    # Calculate Cosine Diff between two BoWs
    def cos_dist():
        pass

if __name__ == "__main__":
    soups = list()

    # Get a soup for each article
    for f in os.listdir(sys.argv[1]):
        path = os.path.join(sys.argv[1], f)
        doc = open(path)

        soup = BeautifulSoup(doc)
        soups.append(soup)

    # Get all meta tags, grouped by document
    all_metas = list()

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

    jr = BoWser(all_metas)
    jr.get_counts()