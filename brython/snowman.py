from re import I
from browser import bind, window, document, html, highlight, markdown
import os
import sys
import traceback
from browser.local_storage import storage

# questionId = -1
# if document.query['question']:
#     question_id = document.query['question']

# Transform markdown to html and insert in the document


def run(ev):
    document["input-letter"].clear()
    document["output"].clear()
    code = document["textarea-editor"].value

    add_indent_and_wrap = False
    if "input(" in code:
        add_indent_and_wrap = True

    code = replaceInput(code)
    # print(code)
    if add_indent_and_wrap:
        code = addTabsToUserCode(code)
        code = wrap_async(code)

    # print(code)
    code = imports + utils + stdout_to_textarea + code
    code = code.strip()
    loc = {}
    try:
        exec(code, loc)
        document["error"].clear()
    except Exception as e:
        document["output"].clear()
        document["error"].clear()
        document["error"] <= "Exception: " + str(e)
        # exception_handler(e)


imports = """
import sys
from browser import document, window, bind
from io import StringIO
from browser.local_storage import storage
"""
utils = """
class MyOutput:
    def __init__(self):
        self.console = document["output"]
    def write(self, text):
        self.console.text += text

def readInput():
    inputText = document["input"].value.strip()
    inputArray = []
    for i in inputText.split():
        inputArray.append(i)
    return inputArray

inputArray = readInput()
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
"""


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


def wrap_async(code):
    prefix = ['from browser import aio, html', 'async def main():']
    code = '\n'.join(prefix) + code
    code = code + '\naio.run(main())'
    return code


def replaceInput(code):

    updated_code = []
    counter = 0
    for row in code.splitlines():

        lower = False
        upper = False
        row = replace_read(row)
        label, varName = input_row_parts(row)
        if "input(" in row:
            if "lower()" in row:
                lower = True
            elif "upper()" in row:
                upper = True

            indent = indent_find(row)
            counter = counter + 1
            row = "\n" + html_input(label, indent, counter)
            row = row.replace("letter_guessed_qqqq", varName)

            if lower:
                row = row.replace("ev.target.value", "ev.target.value.lower()")
            if upper:
                row = row.replace("ev.target.value", "ev.target.value.upper()")

        updated_code.append("\n" + row)
    code = "".join(updated_code)
    return code


def replace_read(row):

    eq = "="
    if "read()" in row:
        eqId = row.find(eq)
        varName = row[0: eqId]
        row = varName + " = (document['input'].value).splitlines() "
        # row = row.replace("file.readlines()",
        #                     "(document['input'].value).splitlines()")
        # row = row.replace("file.read().splitlines()",
        #                     "(document['input'].value).splitlines()")
    elif "readlines()" in row:
        eqId = row.find(eq)
        varName = row[0: eqId]
        row = varName + " = (document['input'].value).splitlines() "
    return row


def html_input(input_label, indent, counter):
    counter = str(counter)
    if not input_label:
        input_label = "''"
    rows = [
        "html_input_qqqq = html.INPUT(**{'id':'input-letter-" + counter + "', 'onfocusout':'scrollDown(" +
        counter + ")'})",

        "document['input-letter'] <= html.DIV("+input_label+", **{'id':'div-letter-" + counter + "'})",
        "document['input-letter'] <= html_input_qqqq",
        #        "document['input-letter'] <= html.BUTTON('Enter')",
        "document['input-letter'] <= html.BUTTON('Enter', **{'onclick': 'scrollDown(" +
        counter + ")','id':'input-button-" + counter + "'})",
        "ev = await aio.event(html_input_qqqq, 'blur')",
        "letter_guessed_qqqq = ev.target.value",
        "try:",
        "    letter_guessed_qqqq = int(letter_guessed_qqqq)",
        "except:",
        "    letter_guessed_qqqq = letter_guessed_qqqq",
        # "document['input-letter'].clear()"
    ]
    new_rows = []
    for row in rows:
        new_rows.append(indent + row)
    return "\n".join(new_rows)


def input_row_parts(row):
    dquote = '\"'
    squote = '\''
    eq = '='
    if "input()" in row:
        eqId = row.find(eq)
        return '', row[0: eqId].strip()
    elif "input(" in row:
        startId = row.find(dquote)
        endId = row.rfind(dquote)
        eqId = row.find(eq)
        if startId == -1 and endId == -1:
            startId = row.find(squote)
            endId = row.rfind(squote)
            if startId == -1 and endId == -1:
                return 0, 0, "", row[0: eqId].strip()
        return row[startId: endId + 1], row[0: eqId].strip()
    return '', ''


def addTabsToUserCode(code):
    formattedCode = []
    for row in code.splitlines():
        row = "    " + row
        formattedCode.append(row)
    code = "\n".join(formattedCode)
    return code


def replaceInputById(code, test_id):
    inputArray = get_input_array(test_id)
    return code.replace("input()", inputArray)


def get_input_array(test_id):
    return "inputArray.pop(0)"


def indent_find(row):
    leading_spaces = len(row) - len(row.lstrip())
    return row[0:leading_spaces]


@bind(document["run-code"], "click")
def runCode(ev):
    run(ev)
