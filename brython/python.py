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
        inputArray.append(i)
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

test_outputs = [
            ['* ** *** **** *****', '* ** *** ****', '* ** *** **** ***** ******'],
            ['10 9 8 7 6 5 4 3 2 1 0', '10 9 8 7 6 5 4 3 2 1 0', '10 9 8 7 6 5 4 3 2 1 0'],
            ['1 2 3 4 5 6 7 8 9 10', '1 2 3 4 5 6 7 8 9 10', '1 2 3 4 5 6 7 8 9 10'],
            ['1 4', '1 4 9', '1 4 9'],
            ['9', '13', '26'],
            ['* ** *** **** *****', '* ** *** ****', '* ** *** **** ***** ******'],
            ['3 6 9', '12 15', '21 24 27 30'],
            ['a a a a a a a a a a Done', 'b b b b b b b b b b Done', 'c c c c c c c c c c Done'],
            ['Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!', 'Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!', 'Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!, Study, study and STUDY AGAIN!'],
            ['     *      * *     * * *    * * * *   * * * * *  * * * * * * ', '     *      * *     * * *    * * * *   * * * * * ', '   *    * *   * * *  * * * * '],
            ['Positive = 4 Negative = 2 Zero = 1 ', 'Positive = 3 Negative = 1 Zero = 3 ', 'Positive = 1 Negative = 4 Zero = 2 '],

            ['1','8','34'],
            ['3 4 5 6 7 8', '10 11 12 13 14 15 16 17 18 19 20', '25 26 27 28 29 30'],
            ['3 4 5 6 7 8', '20 19 18 17 16 15 14 13 12 11 10', '32 31 30 29'],
            ['2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 88 90 92 94 96 98 100','2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 88 90 92 94 96 98 100','2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 88 90 92 94 96 98 100'],
            ['15 13 11 9','19 17 15','31 29 27 25'],
            ['55','107','145'],
            ['15','16','40'],
            ['1 12 123 1234 12345','1 12 123','1 12 123 1234 12345 123456 1234567'],
            ['* ** *** **** *****','* ** ***','* ** *** **** ***** ****** *******'],
            ['120','720','5040'],

            ['225','100','36'],
            ['55','57','223'],
            ['1','3','2'],
            ['153','873','33'],
            ['','',''],
            ['','',''],
            ['2','3','0'],
            ['1505 1540 1575 1610 1645 1680 1715 1750 1785 1820 1855 1890 1925 1960 1995 2030 2065 2100 2135 2170 2205 2240 2275 2310 2345 2380 2415 2450 2485 2520 2555 2590 2625 2660 2695', '1505 1540 1575 1610 1645 1680 1715 1750 1785 1820 1855 1890 1925 1960 1995 2030 2065 2100 2135 2170 2205 2240 2275 2310 2345 2380 2415 2450 2485 2520 2555 2590 2625 2660 2695', '1505 1540 1575 1610 1645 1680 1715 1750 1785 1820 1855 1890 1925 1960 1995 2030 2065 2100 2135 2170 2205 2240 2275 2310 2345 2380 2415 2450 2485 2520 2555 2590 2625 2660 2695'],
            ['0 1 2 4 5', '0 1 2 4 5', '0 1 2 4 5'],
            ['20 22 24 26 28 40', '20 22 24 26 28 40', '20 22 24 26 28 40 '],

            ['Odd numbers = 0 Even numbers = 3', 'Odd numbers = 3 Even numbers = 2', 'Odd numbers = 4 Even numbers = 4'],
            [' ***  *   * *   * ***** *   * *   * *   *', ' ***  *   * *   * ***** *   * *   * *   *', ' ***  *   * *   * ***** *   * *   * *   *'],
            ['Enter only even numbers: 2 2 2 3  You’ve entered an odd number.','Enter only even numbers: 2 8 12 4 38 20  While loop ended successfully.','Enter only even numbers: 81  You’ve entered an odd number.'],
            ['5 * 5 = 25 6 * 6 = 36 7 * 7 = 49 OK','17 * 17 = 289 18 * 18 = 324 19 * 19 = 361 20 * 20 is divisible by 8','4 * 4 is divisible by 8'],
            ['Average: 2.0 Sum: 6.0', 'Average: 2.0 Sum: 6.0', 'Average: 2.0 Sum: 6.0'],
            ['5 x 1 = 5 5 x 2 = 10 5 x 3 = 15 5 x 4 = 20 5 x 5 = 25 5 x 6 = 30 5 x 7 = 35 5 x 8 = 40 5 x 9 = 45 5 x 10 = 50', '3 x 1 = 3 3 x 2 = 6 3 x 3 = 9 3 x 4 = 12 3 x 5 = 15 3 x 6 = 18 3 x 7 = 21 3 x 8 = 24 3 x 9 = 27 3 x 10 = 30','7 x 1 = 7 7 x 2 = 14 7 x 3 = 21 7 x 4 = 28 7 x 5 = 35 7 x 6 = 42 7 x 7 = 49 7 x 8 = 56 7 x 9 = 63 7 x 10 = 70'],
            ['2','3','31'],
            ['20 minutes','30 minutes','15 minutes'],
            ['8','Number 15 is not a Fibonacci number.','9'],
            ['4','35','21'],

            ['*  * *  * * *  * * * *  * * * * *  * * * *  * * *  * *  *  ', '*  * *  * * *  * * * *  * * *  * *  *  ', '*  * *  * * *  * * * *  * * * * *  * * * * * *  * * * * *  * * * *  * * *  * *  *  '],
            ['Yes! 2 to the power of 2 is 4.', 'No!', 'Yes! 4 to the power of 2 is 16.'],
            ['1 2 4 8 16 32', '1 2 4 8 16 32', '1 2 4 8 16 32 64 128'],
            ['34 is not a prime number 2 times 17 is 34', '11 is a prime number', '407 is not a prime number 11 times 37 is 407'],
            ['All Prime numbers between 10 and 50 are: 11 13 17 19 23 29 31 37 41 43 47', 'All Prime numbers between 24 and 35 are: 29 31', 'All Prime numbers between 50 and 67 are: 53 59 61 67'],
            ['12 14 16 18 20 22 24', '10 15 20 25 30 35', '4 5 6 7 8 9 10'],
            ['The Largest Digit is: 7','The Largest Digit is: 8','The Largest Digit is: 9'],
            ['Yes','No','Yes'],
            ['','',''],
            ['','','']
            ]

def get_test_inputs():
    test_inputs = [
            [[5],[4],[6]],
            [[],[],[]],
            [[],[],[]],
            [[5],[10],[15]],
            [[10,20],[10,30],[10,100]],
            [[5],[4],[6]],
            [[1,10],[10,15],[20,30]],
            [['a'],['b'],['c']],
            [[],[],[]],
            [[6],[5],[4]],
            [[-2,9,13,7,1,0,-6],[5,23,-6,0,0,1,0],[-3,-5,-2,6,0,-7,0]],

            [[3],[7],[10]],
            [[3,8],[10,20],[25,30]],
            [[3,8],[20,10],[32,29]],
            [[],[],[]],
            [[15,8],[20,14],[32,25]],
            [[1,2,3,4,5,6,7,8,9,10],[35,24,5,2,5,2,9,12,3,10],[10,11,12,13,14,15,16,17,18,19]],
            [[5,5,4,3,2,1],[3,4,5,7],[8,5,5,5,5,5,5,5,5]],
            [[5],[3],[7]],
            [[5],[3],[7]],
            [[5],[6],[7]],

            [[5],[4],[3]],
            [[1,2,3,4,5,6,7,8,9,10],[5,3,4,5,6,7,8,9,0,10],[5,2,4,8,1,67,34,23,15,64]],
            [[4,1,0,1,1],[8,1,0,0,0,0,0,1,1],[5,1,1,0,0,1]],
            [[5],[6],[4]],
            [[],[],[]],
            [[],[],[]],
            [[5,2,0,6,0,10],[6,0,0,0,10,20,30],[8,4,37,6,48,1,3,6,29]],
            [[],[],[]],
            [[],[],[]],
            [[],[],[]],

            [[5,2,0,6,0,10],[6,3,7,0,13,20,30],[8,4,37,6,48,1,3,6,29]],
            [[],[],[]],
            [[2,2,2,3,2,2],[2,8,12,4,38,20],[81,2,10,4,8,2]],
            [[5,7],[17,25],[4,14]],
            [[1,2,3,0],[1,2,3,0],[1,2,3,0]],
            [[5],[3],[7]],
            [[6],[9],[31]],
            [[3,5,8,7],[4,5,10,5,10],[2,7,8]],
            [[21],[15],[34]],
            [[100,23,200],[1000,7,10000],[123,12,1234]],

            [[5],[4],[6]],
            [[4],[7],[16]],
            [[60],[32],[150]],
            [[34],[11],[407]],
            [[10,50],[24,35],[50,67]],
            [[12,25,2],[10,35,5],[4,10,1]],
            [[3671],[764580],[458791]],
            [[128],[107],[12]],
            [[],[],[]],
            [[],[],[]]

            ]
    return test_inputs
"""
