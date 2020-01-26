from nlp_test import SentenceParser
from test_data import input_output

def runTest(test_case):
    sentence, event, entity = [val for val in test_case]
    print("Case: ", sentence)
    actual = SentenceParser(sentence)
    if actual.event != event:
        print("FAIL: event doenst match, got", actual.event, "Expected ", event)
        return
    if actual.entity != entity:
        print("FAIL: entity doenst match, got", actual.entity, "Expected ", entity)
        return
    print("PASSED")

for test_case in input_output:
    runTest(test_case)
