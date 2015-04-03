from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from collections import defaultdict
from charmeleon import Charmeleon

class HTMLVectorizer():

    def __init__(self):
        # Change to sparse = True?
        self.v = DictVectorizer(sparse=False)

    def html_iter(self, files):
        # Build Y = [labels], X = feature matrix
        Y = list()
        X = list()

        # Calculate character features for each text node
        charm = Charmeleon()

        for f in files:
            soup = BeautifulSoup(open(f))

            # Initialize Document features
            n_id = 0        # Node ID: ith Node traversed in the DOM tree
            textn_id = 0    # TextNode ID: ith TextNode traversed in the DOM
            offset = 0      # Offset: Position relative to the document
            depth = 0       # Depth: depth of the node in the DOM tree

            # Find all text nodes
            text_nodes = soup.find_all(text=True)
            x_temp = list()

            # Iterate through text nodes and find annotation labels or label "None"
            for text in text_nodes:

                textn_id += 1
                offset += len(text)

                if text.parent is not None:
                    node = text.parent

                    if node.has_attr('annotation'):
                        Y.append(node['annotation'])
                    else:
                        Y.append("None")

                    features = charm.compute_features(text)

                    # Add Parent, Gparent, GGparent

                    # Add tag_name to features
                    features['tag_name'] = node.name
                    features['textn_id'] = textn_id
                    features['offset'] = offset

                    x_temp.append(features)

            for example in x_temp:
                example['textn_id'] /= float(textn_id)
                example['offset'] /= float(offset)

            X.extend(x_temp)

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
