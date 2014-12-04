from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from collections import defaultdict
from charmeleon import Charmeleon

class HTMLVectorizer():
    
    v = DictVectorizer(sparse=False)

    def html_iter(self, filename):
        # Build Y = [labels]
        Y = list()
        Y_text = list()

        soup = BeautifulSoup(open(filename))

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

    def fit(filename):
        result = html_iter(filename)
        X = self.v.fit(result[0])
        Y = result[1]
        return [X, Y]

    def fit_transform(self, filename):
        result = self.html_iter(filename)
        X = self.v.fit_transform(result[0])
        Y = result[1]
        return [X, Y]

    def inverse_transform(X):
        return self.v.inverse_transform(X)

    def transform(filename):
        result = html_iter(filename)
        X = self.v.transform(result[0])
        Y = result[1]
        return [X, Y]