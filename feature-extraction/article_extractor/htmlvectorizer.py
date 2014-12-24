from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from collections import defaultdict
from charmeleon import Charmeleon

class HTMLVectorizer():

    v = DictVectorizer(sparse=False)

    def html_iter(self, files):
        # Build Y = [labels], X = feature matrix
        Y = list()
        X = list()

        # Calculate character features for each text node
        charm = Charmeleon()

        for f in files:
            soup = BeautifulSoup(open(f))

            # Find all text nodes
            text_nodes = soup.find_all(text=True)

            # Iterate through text nodes and find annotation labels or label "None"
            for text in text_nodes:
                if text.parent is not None:
                    node = text.parent

                    if node.has_attr('annotation'):
                        Y.append(node['annotation'])
                    else:
                        Y.append("None")

                    features = charm.compute_features(text)
                    features['tag_name'] = node.name

                    X.append(features)

        # Return list of character feature vectors + labels
        return [X, Y]

    def fit(self, files):
        result = self.html_iter(files)
        X = self.v.fit(result[0])
        Y = result[1]
        return [X,Y]

    def fit_transform(self, files):
        result = self.html_iter(files)
        X = self.v.fit_transform(result[0])
        Y = result[1]
        return [X, Y]

    def inverse_transform(self, X):
        return self.v.inverse_transform(X)

    def transform(self, files):
        result = html_iter(files)
        X = self.v.transform(result[0])
        Y = result[1]
        return [X, Y]