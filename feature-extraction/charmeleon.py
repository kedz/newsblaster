from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer
import copy
from collections import defaultdict

#emptyFeatureDict = {
#    'len': 0,
#    'blackspaces': 0,
#    'whitespaces': 0,
#    'alpha': 0,
#    'digit': 0,
#    'upper': 0,
#    'lower': 0,
#    'punct': 0,
#    'newline': 0,
#    'backticks': 0,
#    'backticks' : 0,    # `    
#    'brackets' : 0,        # [        
#    'crackets' : 0,        # ]
#    'percents' : 0,        # %    24
#    'slashes' : 0,        # /
#    'blashes' : 0,        # \
#    'exclams' : 0,        # !    20
#    'periods' : 0,        # .
#    'dollars' : 0,        # $    23
#    'carrots' : 0,        # ^    25
#    'quests' : 0,        # ?
#    'colons' : 0,        # :
#    'solons' : 0,        # ,
#    'parens' : 0,        # (    28
#    'qarens' : 0,        # )    29
#    'commas' : 0,        # ,    
#    'pounds' : 0,        # #    22
#    'ampers' : 0,        # &    26
#    'pluses' : 0,        # +    33
#    'dashes' : 0,        # -    30
#    'unders' : 0,        # _    31
#    'greats' : 0,        # >
#    'lesses' : 0,        # <
#    'equals' : 0,        # =    32
#    'curlys' : 0,        # {
#    'durlys' : 0,        # }
#    'tildas' : 0,        # ~
#    'quots' : 0,        # '    42
#    'duots' : 0,        # "    43
#    'stars' : 0,        # *    27
#    'bars' : 0,            # |
#    'car' : 0,
#    'tab' : 0,
#    'ats' : 0,            # @        21
#    'e' : 0,            # e     8
#    't' : 0,            # t     9
#    'a' : 0,            # a     10
#    'o' : 0,            # o     11
#    'i' : 0,            # i     12
#    'n' : 0,            # n     13
#    's' : 0,            # s     14
#    'h' : 0,            # h        15
#    'r' : 0                # r     16
#}

# Build Y = [labels]
Y = list()
# Should I break it up into Y = [labels] and Y_text = [string]?

# Load Annotated HTML (*.annotation)
annotated_html = BeautifulSoup(open("test.annotation"))

text_nodes = annotated_html.find_all(text=True)

for node in text_nodes:
    name = getattr(node, "name", None)
    if name is not None:
        print name
    elif not node.isspace(): # leaf node, don't print spaces
        print node

# Choose nodes with annotation
def has_annotation(tag):
    return tag.has_attr('annotation')

# Iterate through nodes and save labels in list Y = [labels]
for node in annotated_html.find_all(has_annotation):
    Y.append([node['annotation'], node.getText()])

def increment_feature(dict, key):
    dict[key] = dict.get(key, 0) + 1

# Iterate character-wise through text and compute featureDict
def compute_features(text):
    # Setup dict for counts
    # featureDict = copy.deepcopy(emptyFeatureDict)
    
    featureDict = defaultdict(int)
    featureDict['len'] = len(text)
    decodedText = text.encode('ascii','replace')
    
    for c in decodedText:
        if not c.isspace():
            # Non-whitespace
            featureDict['blackspaces'] += 1
            #increment_feature(featureDict, 'blackspaces')
            if c.isalnum():
                # Alpha-numeric
                if c.isdigit(): featureDict['digit'] += 1
                else:
                    # Alpha
                    featureDict['alpha'] += 1
                    if c.islower(): featureDict['lower'] += 1
                    if c.isupper(): featureDict['upper'] += 1

                    # Test for characters
                    featureDict[c.lower()] += 1

            # Punctuation
            elif c == '!': 
                featureDict['punct'] += 1
                featureDict['exclams'] += 1
            elif c == '@': 
                featureDict['punct'] += 1
                featureDict['ats'] += 1
            elif c == '#': 
                featureDict['punct'] += 1
                featureDict['pounds'] += 1
            elif c == '$': 
                featureDict['punct'] += 1
                featureDict['dollars'] += 1
            elif c == '%': 
                featureDict['punct'] += 1
                featureDict['percents'] += 1
            elif c == '^': 
                featureDict['punct'] += 1
                featureDict['carrots'] += 1
            elif c == '&': 
                featureDict['punct'] += 1
                featureDict['ampers'] += 1
            elif c == '*': 
                featureDict['punct'] += 1 
                featureDict['stars'] += 1
            elif c == '(': 
                featureDict['punct'] += 1 
                featureDict['parens'] += 1
            elif c == ')': 
                featureDict['punct'] += 1 
                featureDict['qarens'] += 1
            elif c == '-': 
                featureDict['punct'] += 1 
                featureDict['dashes'] += 1
            elif c == '_': 
                featureDict['punct'] += 1 
                featureDict['unders'] += 1
            elif c == '=': 
                featureDict['punct'] += 1 
                featureDict['equals'] += 1
            elif c == '+': 
                featureDict['punct'] += 1 
                featureDict['pluses'] += 1
            elif c == '{': 
                featureDict['punct'] += 1 
                featureDict['curlys'] += 1
            elif c == '}': 
                featureDict['punct'] += 1 
                featureDict['durlys'] += 1
            elif c == '[': 
                featureDict['punct'] += 1 
                featureDict['brackets'] += 1
            elif c == ']': 
                featureDict['punct'] += 1 
                featureDict['crackets'] += 1
            elif c == '\\': 
                featureDict['punct'] += 1 
                featureDict['blashes'] += 1
            elif c == '|': 
                featureDict['punct'] += 1 
                featureDict['bars'] += 1
            elif c == ':': 
                featureDict['punct'] += 1 
                featureDict['colons'] += 1
            elif c == ';': 
                featureDict['punct'] += 1 
                featureDict['solons'] += 1
            elif c == '\'': 
                featureDict['punct'] += 1
                featureDict['quots'] += 1
            elif c == '"': 
                featureDict['punct'] += 1 
                featureDict['duots'] += 1
            elif c == ',': 
                featureDict['punct'] += 1 
                featureDict['commas'] += 1
            elif c == '.': 
                featureDict['punct'] += 1 
                featureDict['periods'] += 1
            elif c == '<': 
                featureDict['punct'] += 1 
                featureDict['lesses'] += 1
            elif c == '>': 
                featureDict['punct'] += 1 
                featureDict['greats'] += 1
            elif c == '/': 
                featureDict['punct'] += 1 
                featureDict['slashes'] += 1
            elif c == '?': 
                featureDict['punct'] += 1 
                featureDict['quests'] += 1
            # Whitespace
            else:
                featureDict['whitespaces'] += 1
                if c == "\n": featureDict['newline'] += 1
                elif c == '\r': featureDict['car'] += 1
                elif c == '\t': featureDict['tab'] += 1

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
print v.inverse_transform(X)
#print v.get_feature_names()
