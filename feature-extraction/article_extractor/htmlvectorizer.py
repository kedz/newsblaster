from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from collections import defaultdict
from BoWser import BoWser
#from charmeleon import Charmeleon

class HTMLVectorizer():

    def __init__(self):
        # Change to sparse = True?
        self.v = DictVectorizer(sparse=False)

    def html_iter(self, files):
        # Build Y = [labels], X = feature matrix
        Y = list()
        X = list()
        all_text = list()
        text_by_doc = list()
        metas_by_doc = list()
        curr_id = 0
        doc_idxs = list()

        # Calculate character features for each text node
        # charm = Charmeleon()

        for f in files:
            # Open doc for reading, save doc (line-delimited?), and put doc into BS
            doc = open(f)
            doc_idxs.append(curr_id)

            soup = BeautifulSoup(doc)

            # Initialize Document features
            n_id = 0        # Node ID: ith Node traversed in the DOM tree
            textn_id = 0    # TextNode ID: ith TextNode traversed in the DOM
            offset = 0      # Offset: Position relative to the document
            depth = 0       # Depth: depth of the node in the DOM tree

            # Extract document <meta> tags for use in BoWser
            metas = soup.find_all("meta")

            doc_metas = list()

            if metas is not None:
                for tag in metas:
                    meta_string = tag.get("content")

                    if meta_string is None:
                        meta_string = ""

                    # Append to doc_metas to keep track of which
                    # metas appear in which document
                    doc_metas.append(meta_string)

            # Append doc_mettas to all_metas
            metas_by_doc.append(doc_metas)

            # Find all text nodes
            # What if instead, I used soup.strings?
            text_nodes = soup.find_all(text=True)

            x_temp = list()
            doc_text = list()

            # Iterate through text nodes and find annotation labels or label "None"
            for text in text_nodes:
                textn_id += 1
                curr_id += 1
                offset += len(text)
                doc_text.append(text)
                all_text.append(text)

                # Find golden label
                if text.parent is not None:
                    node = text.parent

                    if node.has_attr('annotation'):
                        Y.append(node['annotation'])
                    elif node.has_attr(''):
                        Y.append("None")
                    else:
                        Y.append("None")

                    #features = charm.compute_features(text)
                    features = defaultdict(int)

                    # Add Parent, Gparent, GGparent
                    if node.parent != None :
                        features['parent'] = node.parent.name
                        #print "Has parent", node.parent
                        if node.parent.parent != None:
                            features['gparent'] = node.parent.parent.name
                            if node.parent.parent.parent != None:
                                features['ggparent'] = node.parent.parent.parent.name

                    # Add tag_name to features
                    features['tag_name'] = node.name

                    # Add textn_id, offset to features
                    features['textn_id'] = textn_id
                    features['offset'] = offset

                    # Add example to x_temp (all examples in this doc)
                    x_temp.append(features)

                    # Add text to all_text
                    all_text.extend(text_nodes)

            # Normalize real-valued features
            for example in x_temp:
                example['textn_id'] /= float(textn_id)
                example['offset'] /= float(offset)

            # Add example to X
            X.extend(x_temp)

            # Add text_nodes to text_by_doc
            text_by_doc.append(doc_text)

        # Get BoWs for each doc
        bowser = BoWser(metas_by_doc, text_by_doc)
        all_bows = bowser.get_counts()

        print'''
        \n HTMLVectorizer Finished. \n
        '''

        # Return list of character feature vectors + labels + doc_idxs (beginning
        # index of a document in X) + doc_bow (bow_metas, countvectorizer, text)
        return [X, Y, doc_idxs, all_text, all_bows]

    def fit(self, files):
        result = self.html_iter(files)
        X = self.v.fit(result[0])
        Y = result[1]
        doc_idxs = result[2]
        all_text = result[3]
        all_bows = result[4]
        return [X,Y, doc_idxs, all_text, all_bows]

    def fit_transform(self, files):
        result = self.html_iter(files)
        X = self.v.fit_transform(result[0])
        Y = result[1]
        doc_idxs = result[2]
        all_text = result[3]
        all_bows = result[4]
        return [X,Y, doc_idxs, all_text, all_bows]

    def inverse_transform(self, X):
        return self.v.inverse_transform(X)

    def transform(self, files):
        result = html_iter(files)
        X = self.v.transform(result[0])
        Y = result[1]
        doc_idxs = result[2]
        all_text = result[3]
        all_bows = result[4]
        return [X,Y, doc_idxs, all_text, all_bows]
