from collections import defaultdict

class Charmeleon():

    # Iterate character-wise through text and compute featureDict
    def compute_features(self, text):
        # Setup dict for counts
        featureDict = defaultdict(int)
        featureDict['len'] = len(text)
        decodedText = text.encode('ascii','replace')

        l = 1 / len(decodedText)

        for c in decodedText:
            if not c.isspace():
                # Non-whitespace
                featureDict['blackspaces'] += l

                if c.isalnum():
                    # Alpha-numeric
                    if c.isdigit(): featureDict['digit'] += l
                    else:
                        # Alpha
                        featureDict['alpha'] += l
                        if c.islower(): featureDict['lower'] += l
                        if c.isupper(): featureDict['upper'] += l

                        # Test for characters
                        featureDict[c.lower()] += l

                # Punctuation
                elif c == '!':
                    featureDict['punct'] += l
                    featureDict['exclams'] += l
                elif c == '@':
                    featureDict['punct'] += l
                    featureDict['ats'] += l
                elif c == '#':
                    featureDict['punct'] += l
                    featureDict['pounds'] += l
                elif c == '$':
                    featureDict['punct'] += l
                    featureDict['dollars'] += l
                elif c == '%':
                    featureDict['punct'] += l
                    featureDict['percents'] += l
                elif c == '^':
                    featureDict['punct'] += l
                    featureDict['carrots'] += l
                elif c == '&':
                    featureDict['punct'] += l
                    featureDict['ampers'] += l
                elif c == '*':
                    featureDict['punct'] += l
                    featureDict['stars'] += l
                elif c == '(':
                    featureDict['punct'] += l
                    featureDict['parens'] += l
                elif c == ')':
                    featureDict['punct'] += l
                    featureDict['qarens'] += l
                elif c == '-':
                    featureDict['punct'] += l
                    featureDict['dashes'] += l
                elif c == '_':
                    featureDict['punct'] += l
                    featureDict['unders'] += l
                elif c == '=':
                    featureDict['punct'] += l
                    featureDict['equals'] += l
                elif c == '+':
                    featureDict['punct'] += l
                    featureDict['pluses'] += l
                elif c == '{':
                    featureDict['punct'] += l
                    featureDict['curlys'] += l
                elif c == '}':
                    featureDict['punct'] += l
                    featureDict['durlys'] += l
                elif c == '[':
                    featureDict['punct'] += l
                    featureDict['brackets'] += l
                elif c == ']':
                    featureDict['punct'] += l
                    featureDict['crackets'] += l
                elif c == '\\':
                    featureDict['punct'] += l
                    featureDict['blashes'] += l
                elif c == '|':
                    featureDict['punct'] += l
                    featureDict['bars'] += l
                elif c == ':':
                    featureDict['punct'] += l
                    featureDict['colons'] += l
                elif c == ';':
                    featureDict['punct'] += l
                    featureDict['solons'] += l
                elif c == '\'':
                    featureDict['punct'] += l
                    featureDict['quots'] += l
                elif c == '"':
                    featureDict['punct'] += l
                    featureDict['duots'] += l
                elif c == ',':
                    featureDict['punct'] += l
                    featureDict['commas'] += l
                elif c == '.':
                    featureDict['punct'] += l
                    featureDict['periods'] += l
                elif c == '<':
                    featureDict['punct'] += l
                    featureDict['lesses'] += l
                elif c == '>':
                    featureDict['punct'] += l
                    featureDict['greats'] += l
                elif c == '/':
                    featureDict['punct'] += l
                    featureDict['slashes'] += l
                elif c == '?':
                    featureDict['punct'] += l
                    featureDict['quests'] += l
                # Whitespace
                else:
                    featureDict['whitespaces'] += l
                    if c == "\n": featureDict['newline'] += l
                    elif c == '\r': featureDict['car'] += l
                    elif c == '\t': featureDict['tab'] += l

        return featureDict