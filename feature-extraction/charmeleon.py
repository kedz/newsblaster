from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer
import copy

emptyFeatureDict = {
	'len': 0,
	'blackspaces': 0,
	'whitespaces': 0,
	'alpha': 0,
	'digit': 0,
	'upper': 0,
	'lower': 0,
	'punct': 0,
	'newline': 0,
	'backticks': 0,
	'backticks' : 0,	# `	
	'brackets' : 0,		# [		
	'crackets' : 0,		# ]
	'percents' : 0,		# %	24
	'slashes' : 0,		# /
	'blashes' : 0,		# \
	'exclams' : 0,		# !	20
	'periods' : 0,		# .
	'dollars' : 0,		# $	23
	'carrots' : 0,		# ^	25
	'quests' : 0,		# ?
	'colons' : 0,		# :
	'solons' : 0,		# ,
	'parens' : 0,		# (	28
	'qarens' : 0,		# )	29
	'commas' : 0,		# ,	
	'pounds' : 0,		# #	22
	'ampers' : 0,		# &	26
	'pluses' : 0,		# +	33
	'dashes' : 0,		# -	30
	'unders' : 0,		# _	31
	'greats' : 0,		# >
	'lesses' : 0,		# <
	'equals' : 0,		# =	32
	'curlys' : 0,		# {
	'durlys' : 0,		# }
	'tildas' : 0,		# ~
	'quots' : 0,		# '	42
	'duots' : 0,		# "	43
	'stars' : 0,		# *	27
	'bars' : 0,			# |
	'car' : 0,
	'tab' : 0,
	'ats' : 0,			# @		21
	'e' : 0,			# e 	8
	't' : 0,			# t 	9
	'a' : 0,			# a 	10
	'o' : 0,			# o 	11
	'i' : 0,			# i 	12
	'n' : 0,			# n 	13
	's' : 0,			# s 	14
	'h' : 0,			# h		15
	'r' : 0				# r 	16
}

# Build Y = [labels]
Y = list()
# Should I break it up into Y = [labels] and Y_text = [string]?

# Load Annotated HTML (*.annotation)
annotated_html = BeautifulSoup(open("test.annotation"))

# Choose nodes with annotation
def has_annotation(tag):
    return tag.has_attr('annotation')

# Iterate through nodes and save labels in list Y = [labels]
for node in annotated_html.find_all(has_annotation):
	Y.append([node['annotation'], node.getText()])

def increment_feature(dict, key):
	dict[key] = dict.get(key) + 1

# Iterate character-wise through text and compute featureDict
def compute_features(text):
	# Setup dict for counts
	featureDict = copy.deepcopy(emptyFeatureDict)
	
	featureDict['len'] = len(text)
	decodedText = text.encode('ascii','replace')
	
	for c in decodedText:
		if not c.isspace():
			# Non-whitespace
			increment_feature(featureDict, 'blackspaces')
			if c.isalnum():
				# Alpha-numeric
				if c.isdigit(): increment_feature(featureDict, 'digit')
				else:
					# Alpha
					increment_feature(featureDict, 'alpha')
					if c.islower(): increment_feature(featureDict, 'lower')
					if c.isupper(): increment_feature(featureDict, 'upper')

					# Test for characters
					if c.lower() == 'e': increment_feature(featureDict, 'e')
					elif c.lower() == 't': increment_feature(featureDict, 't')
					elif c.lower() == 'a': increment_feature(featureDict, 'a')
					elif c.lower() == 'o': increment_feature(featureDict, 'o')
					elif c.lower() == 'i': increment_feature(featureDict, 'i')
					elif c.lower() == 'n': increment_feature(featureDict, 'n')
					elif c.lower() == 's': increment_feature(featureDict, 's')
					elif c.lower() == 'h': increment_feature(featureDict, 'h')
					elif c.lower() == 'r': increment_feature(featureDict, 'r')
			# Punctuation
			elif c == '!': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'exclams')
			elif c == '@': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'ats')
			elif c == '#': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'pounds')
			elif c == '$': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'dollars')
			elif c == '%': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'percents')
			elif c == '^': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'carrots')
			elif c == '&': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'ampers')
			elif c == '*': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'stars')
			elif c == '(': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'parens')
			elif c == ')': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'qarens')
			elif c == '-': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'dashes')
			elif c == '_': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'unders')
			elif c == '=': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'equals')
			elif c == '+': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'pluses')
			elif c == '{': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'curlys')
			elif c == '}': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'durlyss')
			elif c == '[': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'brackets')
			elif c == ']': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'crackets')
			elif c == '\\': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'blashes')
			elif c == '|': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'bars')
			elif c == ':': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'colons')
			elif c == ';': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'solons')
			elif c == '\'': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'quots')
			elif c == '"': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'duots')
			elif c == ',': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'commas')
			elif c == '.': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'periods')
			elif c == '<': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'lesses')
			elif c == '>': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'greats')
			elif c == '/': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'slashes')
			elif c == '?': 
				increment_feature(featureDict, 'punct') 
				increment_feature(featureDict, 'quests')
			# Whitespace
			else:
				increment_feature(featureDict, 'whitespaces')
				if c == "\n": increment_feature(featureDict, 'whitespaces')
				elif c == '\r': increment_feature(featureDict, 'car')
				elif c == '\t': increment_feature(featureDict, 'tab')

	return featureDict

# Traverse *.annotation's annotated elements and compute feature vectors
def traverse_annotated_nodes(nodes):
	nodeMatrix = list()
	for node in nodes:
		# node = [label, text]
		features = compute_features(node[1])
		nodeMatrix.append(features)
	return nodeMatrix

# Build list of feature vectors to build Matrix X
dictList = traverse_annotated_nodes(Y)

# Use SciKit to store feature vectors for each annotated node
v = DictVectorizer(sparse=False)
X = v.fit_transform(dictList)

# Output X = [feature vectors], Y = [labels]
print X
#print v.inverse_transform(X)
#print v.get_feature_names()
