from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from collections import defaultdict
from charmeleon import Charmeleon

class HTMLVectorizer():
    
    v = DictVectorizer(sparse=False)

    def html_iter(self, files):
        # Build Y = [labels]
        Y = list()
        Y_text = list()

        soups = list()

        for f in files:
            soups.append(BeautifulSoup(open(f)))

        for soup in soups:
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
                   
                    Y_text.append(text)

        # Calculate character features for each text node
        charm = Charmeleon()

        nodeMatrix = list()

        for node in Y_text:
            features = charm.compute_features(node)
            nodeMatrix.append(features)

        # Return list of character feature vectors + labels
        return [nodeMatrix, Y]

    def fit(self, files):
        result = html_iter(files)
        return self.v.fit(result[0])

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