from browser import bind, window, document, html, highlight, markdown
import os
import sys
import traceback
from browser.local_storage import storage

# questionId = -1
# if document.query['question']:
question_id = document.query['question']

# Transform markdown to html and insert in the document


def run(ev):
    document["output_0"].clear()
    code = document["editor"].text
    code = imports + test_input_output  + utils + stdout_to_textarea + code
    code = replaceInput(code)
    code = code.strip()
    code = os.linesep.join(
        [s for s in code.splitlines() if s and len(s) > 1])
    loc = {}
    try:
        exec(code, {"test_id": 0, "question_id": question_id}, loc)
        document["error"].clear()
    except Exception as e:
        document["output_0"].clear()
        document["error"].clear()
        document["error"] <= "Exception: " + str(e)
        # exception_handler(e)


imports = """
import sys
from browser import document
from io import StringIO
from browser.local_storage import storage
"""
utils = """

# print('get_test_inputs', get_test_inputs())
question_id = int(question_id)
class MyOutput:
    def __init__(self):
        self.console = document["output_0"]
    def write(self, text):
        self.console.text += text


def readInput(test_id):
    inputText = document["input_" + str(test_id)].value.strip()
    inputArray = []
    for i in inputText.split():
        inputArray.append(int(i))
    return inputArray

def readTestInput(test_id):
    # print('in readTestInput', test_id)
    test_inputs = get_test_inputs()
    return test_inputs[question_id][test_id]

inputArray = readInput(0)
inputArray0 = readTestInput(0)
inputArray1 = readTestInput(1)
inputArray2 = readTestInput(2)

# print('inputArray1', inputArray0)
# print('inputArray2', inputArray1)
# print('inputArray3', inputArray2)
outputArray = []
"""
stdout_to_variable = """
old_stdout = sys.stdout
new_stdout = StringIO()
sys.stdout = new_stdout
"""
stdout_to_textarea = """
sys.stdout = MyOutput()
"""


def get_result_code():
    return """

result = new_stdout.getvalue().strip()
equal = False
output = test_outputs[question_id][test_id]

output = output.strip()

sys.stdout = MyOutput()

result = result.replace('\\n', ' ')

if result.__eq__(output):
    equal = True

storage["result_{}_{}"] = str(equal)

"""


def test(test_id):

    code = document["editor"].text
    result_code = get_result_code()
    result_code = result_code.format(question_id, test_id)

    code = imports + stdout_to_variable + \
        test_input_output + utils + code + result_code
    code = replaceInputById(code, test_id)
    code = code.strip()
    code = os.linesep.join(
        [s for s in code.splitlines() if s and len(s) > 1])
    loc = {}

    try:
        exec(code, {"test_id": test_id, "question_id": question_id}, loc)
    except Exception as e:
        document["error"].clear()
        document["error"] <= "Exception: " + str(e)
        # exception_handler(e)


def exception_handler(e):

    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (
            trace[0], trace[1], trace[2], trace[3]))

    print("Exception type : %s " % ex_type.__name__)
    print("Exception message : %s" % ex_value)
    print("Stack trace : %s" % stack_trace)


def replaceInput(code):
    return code.replace("input()", "inputArray.pop(0)")


def replaceInputById(code, test_id):
    inputArray = get_input_array(test_id)
    return code.replace("input()", inputArray)


def get_input_array(test_id):
    inputArray = "inputArray.pop(0)"
    if test_id == 0:
        inputArray = "inputArray0.pop(0)"
    elif test_id == 1:
        inputArray = "inputArray1.pop(0)"
    elif test_id == 2:
        inputArray = "inputArray2.pop(0)"
    return inputArray


@bind(document["run-code"], "click")
def runCode(ev):
    run(ev)


@bind(document["submit-code"], "click")
def runTest(ev):
    clean_local_storage()
    test(0)
    test(1)
    test(2)
    show_user_test_result()


def clean_local_storage():
    try:
        del storage["result_" + question_id + '_0']
    except Exception as e:
        exc = str(e)
        # print(str(e))


def show_user_test_result():
    document["test-result"].clear()
    result_0 = storage["result_" + question_id + '_0']
    result_1 = storage["result_" + question_id + '_1']
    result_2 = storage["result_" + question_id + '_2']

    if result_0 == 'True' and result_1 == 'True' and result_2 == 'True':
        document["test-result"] <= html.SPAN(
            "<span class='test-success'>test passed succesfully</span>")
    else:
        document["test-result"] <= html.SPAN(
            "<span class='test-fail'>test failed</span>")


test_input_output = """

test_outputs = [['5 6', '4 4', '9 20']]

def get_test_inputs():
    test_inputs = [[[2,3],[2,2], [4,5]], [[6,3],[4,5], [5,5]]]
    return test_inputs


"""
