import spacy
nlp = spacy.load("en_core_web_sm")

# PARSE TODO
# Entity = Noun subject 
def getEntityOrGuess(nlp_doc):
    ents = list(nlp_doc.ents)
    if len(ents) == 0:
        for token in nlp_doc:
            if token.pos_ == "NOUN":
                return token.text
    
    return ents[0].text

def getEvent(doc):
    """Finds verb and dependent object"""

    root = ""
    for token in doc:
        if (token.pos_ == "VERB" or token.pos_ == "AUX") and token.dep_ == "ROOT":
            root = token
        
    dependent_object = ""
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == "dobj" and chunk.root.head.text == root.text:
            dependent_object = chunk.text

    return root.text + " " + dependent_object

def parseSentence(sentence, show_debug_output=False):
    doc = nlp(sentence)
    if show_debug_output:
        showDebug(doc)
    return [getEvent(doc), getEntityOrGuess(doc)]


def showDebug(doc):
    print("DEBUG DUMP")
    print("=======Token Info=========")
    print("text", "pos", "tag", "dep", "children")
    for token in doc:
        print(token.text, token.pos_, token.tag_, token.dep_, [child for child in token.children])


    print("=======Noun Chunks========")
    print("text", "root", "root dep", "root head text")
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

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
    event_entity = parseSentence(sentences[sentence_idx], True)
    print("=====output=====")
    print ("Event, Entity", event_entity)