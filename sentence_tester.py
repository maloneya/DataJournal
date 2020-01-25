from nlp_test import parseSentence

input_output = [
  ["last week I took a trip to California", "took a trip", "California"],
  ["Yesterday I had coffee with Rachel at Herkimer", "had coffee", "Herkimer"],
  ["Autonomous cars shift insurance liability toward manufacturers", "shift insurance liability", "manufacturers"]
]

def runTest(test_case):
    sentence, event, entity = [val for val in test_case]
    print("Case: ", sentence)
    print("Expected", event, entity)
    actual_event_entity = parseSentence(sentence)
    if actual_event_entity[0] != event:
        print("FAIL: event doenst match, got", actual_event_entity[0])
        return
    if actual_event_entity[1] != entity:
        print("FAIL: entity doenst match, got", actual_event_entity[1])
        return
    print("PASSED")

for test_case in input_output:
    runTest(test_case)
