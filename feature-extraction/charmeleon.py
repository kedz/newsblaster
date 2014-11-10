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

# Output X = [feature vectors], Y = [labels]
X = {}
Y = list()

# Load Annotated HTML (*.annotation)
annotated_html = BeautifulSoup(open("test.annotation"))

# Choose nodes with annotation
def has_annotation(tag):
    return tag.has_attr('annotation')

# Iterate through nodes and save labels in list Y = [labels]
for node in annotated_html.find_all(has_annotation):
	Y.append(node['annotation'])

print(Y)

# Setup dict for counts
new_dict = copy.deepcopy(emptyFeatureDict)
print(new_dict)

#def add_feature_to_dictionary(feature, value):


def compute_char_features(node):
	
	
# Iterate through links, calculate map for each node

# Use SciKit to store feature vectors for each annotated node

# Output X = [feature vectors], Y = [labels]