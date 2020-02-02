from flask import Flask, request
from SentenceParser import EntityEventActorParser

app = Flask(__name__)

@app.route("/sentence", methods=['POST'])
def parseSentence():
    sentence = request.form['sentence']
    parser = EntityEventActorParser(sentence)

    return " Event: " + parser.event + " Entity: " + parser.entity
    
