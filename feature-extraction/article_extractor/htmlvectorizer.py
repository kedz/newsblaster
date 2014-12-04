from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from collections import defaultdict
from charmeleon.py import Charmeleon

class HTMLVectorizer():
	
	# Build Y = [labels]
	Y = list()
	Y_text = list()

	soup = BeautifulSoup(open(path))

	text_nodes = soup.find_all(text=True)

    for text in text_nodes:
        if text.parent is not None:
            node = text.parent
            
            if node.has_attr('annotation'):
                Y.append(node['annotation'])
            else:
                Y.append("None")
           
            Y_text.append(text)

    charm = Charmeleon()

 	nodeMatrix = list()

 	for node in Y_text:
 		features = charm.computefeatures()
 		nodeMatrix.append(features)

 	v = DictVectorizer(sparse=False)
 	X = v.fit_transform(nodeMatrix)