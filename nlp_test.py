import spacy
nlp = spacy.load("en_core_web_sm")


print("Enter Sentence: ")
sentence = str(input())

def getEntityOrGuess(nlp_doc):
    ents = list(nlp_doc.ents)
    if len(ents) == 0:
        for token in nlp_doc:
            if token.pos_ == "NOUN":
                return token.text
    
    return ents[0].text

def getVerb(nlp_doc):
    for token in nlp_doc:
        if token.pos_ == "VERB":
            return token.text


doc = nlp(sentence)
print("Entity: ")
print(getEntityOrGuess(doc))
print("Verb: ")
print(getVerb(doc))

print("==================")
print("DEBUG DUMP")
for token in doc:
     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)