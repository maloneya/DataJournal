import spacy
nlp = spacy.load("en_core_web_sm")


class SentenceParser:
    def __init__(self, sentence, debug=False):
        self.doc = nlp(sentence)
        self.parsed_tokens = {}
        self.actors = self.getActors()
        self.entity = self.getEntity()
        self.event = self.getEvent()
        
        if (debug):
            self.showDebug()

    def getActors(self):
        pass

    def getEntity(self):
        pobj = ""
        for token in self.doc:
            if token.dep_ == "pobj":
                pobj = token.text

        return pobj

    def getEvent(self):
        """Finds verb and dependent object"""

        root = ""
        for token in self.doc:
            if (token.pos_ == "VERB" or token.pos_ == "AUX") and token.dep_ == "ROOT":
                root = token

        dependent_object = ""
        for chunk in self.doc.noun_chunks:
            if chunk.root.dep_ == "dobj" and chunk.root.head.text == root.text:
                dependent_object = chunk.text

        return root.text + " " + dependent_object

    def showDebug(self):
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


    

if __name__ == "__main__":
    # eventually we should track actor too 
    sentences = [
    "I read The Pale King",
    "last week I took a trip to California",
    "Yesterday I had coffee with Rachel at Herkimer",
    "Autonomous cars shift insurance liability toward manufacturers"
    ]

    print("select input")
    for i,s in enumerate (sentences): 
        print(i, s)

    sentence_idx = int(input())
    parser  = SentenceParser(sentences[sentence_idx], True)
    print("=====output=====")
    print ("Actors, Event, Entity", parser.actors, parser.event, parser.entity)
