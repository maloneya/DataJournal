from SentenceParser import EntityEventActorParser
from test_data import input_output

if __name__ == "__main__":
    print("select input")
    for i,s in enumerate (input_output): 
        print(i, s[0])

    sentence_idx = int(input())
    parser  = EntityEventActorParser(input_output[sentence_idx][0], True)
    print("=====output=====")
    print ("Actors, Event, Entity", parser.actors, parser.event, parser.entity)
