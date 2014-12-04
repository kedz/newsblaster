from collections import defaultdict

class Charmeleon():

    # Iterate character-wise through text and compute featureDict
    def compute_features(self, text):
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