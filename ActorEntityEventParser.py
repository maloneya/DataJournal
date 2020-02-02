import spacy
from test_data import input_output
nlp = spacy.load("en_core_web_sm")


class SentenceParser:
    def __init__(self, sentence, debug=False):
        self.doc = nlp(sentence)
        self.parsed_tokens = {}
        if (debug):
            self._showDebug()

    def findAllTokens(self, container, match_rule):
        tokens = []
        for token in self.unparsedTokens(container):
            if match_rule(token):
                self._setParsed(token.text)
                tokens.append(token)

        return tokens


    def findToken(self, container, match_rule):
        for token in self.unparsedTokens(container):
            if match_rule(token):
                self._setParsed(token.text)
                return token.text

        return ""

    def unparsedTokens(self, iterable):
        for token in iterable: 
            if self._isParsed(token.text):
                continue 

            yield token 

    def _isParsed(self, token_text):
        return self.parsed_tokens.get(token_text, False) 

    def _setParsed(self, token_text):
        self.parsed_tokens[token_text] = True
            

    def _showDebug(self):
        print("DEBUG DUMP")
        print("=======Token Info=========")
        print("text", "pos", "tag", "dep", "children")
        for token in self.doc:
            print(token.text, token.pos_, token.tag_, token.dep_, [child for child in token.children])
