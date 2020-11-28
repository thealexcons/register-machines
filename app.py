from flask import Flask, render_template, request, jsonify
from rm import execute_program_from_lines_and_config
from coding import decodeIntoProgram, encodeProgramIntoCoding
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-program', methods=['POST'])
def executeProgram():
    try:
        # Parse and some basic pre processing on the input strings
        programText = request.json['programText']
        lines = programText.splitlines()
        initialConfiguration = re.sub(' +', ' ', request.json['initialConfig'].strip())
        initialConfiguration = list(map(int, initialConfiguration.split(" ")))

        # execute the program
        finalConfiguration = execute_program_from_lines_and_config(lines, initialConfiguration)
        return jsonify(config=finalConfiguration)
    except:
        print("error occurred")
        return "Error, incorrect format or missing data"


@app.route('/encode-program', methods=['POST'])
def encodeProgram():
    try:
        programText = request.json['programText']
        programLines = programText.splitlines()
        coding, encodedInstrsList = encodeProgramIntoCoding(programLines)
        return jsonify(coding=coding, encodedInstrsList=encodedInstrsList)
    except:
        print("error occurred")
        return "Error, incorrect program format"


@app.route('/decode-program', methods=['POST'])
def decodeProgram():
    try:
        programCode = request.json['code']
        code = 0
        if '^' in programCode or '*' in programCode:
            programCode = programCode.replace("^", "**")
            code = eval(programCode)
        else:
            code = int(programCode)

        program = decodeIntoProgram(code)
        return jsonify(programText=program)
    except:
        print("error occurred")
        return "Error, incorrect format or invalid number"


app.run(host='0.0.0.0', port=8080)