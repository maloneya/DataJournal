import spacy
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


        print("=======Noun Chunks========")
        print("text", "root", "root dep", "root head text")
        for chunk in self.doc.noun_chunks:
            print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

        print("======Recognized Entities=======")
        print("text, label")
        for ent in self.doc.ents:
                print(ent.text, ent.label_)


class EntityEventActorParser(SentenceParser):
    def __init__(self, sentence, debug=False):
        super().__init__(sentence, debug) 
        self.actors = self.getActors()
        self.entity = self.getEntity()
        self.event = self.getEvent()
        
    def getActors(self):
        return self.findAllTokens(self.doc.ents, lambda ent: ent.label_ == 'PERSON')

    def getEntity(self):
        return self.findToken(self.doc, lambda token: token.dep_ == "pobj")

    def getEvent(self):
        """Finds verb and dependent object"""

        root = self.findToken(
                self.doc, 
                lambda token: (token.pos_ == "VERB" or token.pos_ == "AUX") and token.dep_ == "ROOT"
        )

        dependent_object = self.findToken(
                self.doc.noun_chunks,
                lambda chunk: chunk.root.dep_ == "dobj" and chunk.root.head.text == root
        )
        return root + " " + dependent_object

