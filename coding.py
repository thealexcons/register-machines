from rm import parse_line

######### ENCODING ########

# Encodes a list of encoded instruction bodies into a final coding
def encodeList(l):
    if len(l) == 0:
        return 0
    
    return (2 ** l[0]) * (2 * calc(l[1:]) + 1)

def doubleBrackets(x, y):
  return (2 ** x) * (2*y + 1)

def singleBrackets(x, y):
  return (2 ** x) * (2 * y + 1) - 1 

# Encodes a program into the intermediate list and the final coding
def encodeProgramIntoCoding(programLines):
    program = []
    for line in programLines:
        program = parse_line(line, program)

    encodedInstructionList = []
    for instr in program:
        if instr[0] == 'inc':
            encodedInstructionList.append(doubleBrackets(2*instr[1], instr[2]))
        elif instr[0] == 'dec':
            encodedInstructionList.append(doubleBrackets(2*instr[1] + 1, singleBrackets(instr[2], instr[3])))
        else:
            encodedInstructionList.append(0)

    coding = encodeList(encodedInstructionList)
    return coding, encodedInstructionList


######### DECODING ########

# Returns (power, n) where code = 2^power * n
def factoriseTwoEven(code):
    power = 0
    n = code
    while n != 0 and n % 2 == 0:
        n = n / 2
        power += 1
    
    return power, int(n)

# Here, code is odd, so the power will always be 0
# Returns (0, n), where code = 2^0 * (2*n + 1)
def factoriseTwoOdd(code):
    assert(code % 2 != 0, "Not odd")
    return (0, int((code - 1) / 2))

# Given the the encoding of a list, decode it into <<x, y>>
def decodeListInstruction(code):
    if code % 2 == 0:
        power, num = factoriseTwoEven(code)
        return (power, int((num - 1) / 2))
    
    return factoriseTwoOdd(code)

# Decodes a program code into a list of encoded instruction bodies
def decodeIntoList(code):
    encodedInstructions = []
    nextNum = code
    while nextNum != 0:
        power, nextNum = decodeListInstruction(nextNum)
        encodedInstructions.append(power)
    
    return encodedInstructions


# Decode a number into a single bracket representation, num = <j,k>
def decodeIntoSingleBrackets(num):
    for j in range(100):               # Really shit, but works for now
        for k in range(1000):
            if (2 ** j) * (2 * k + 1) - 1 == num:
                return (j, k)

    print("ERROR DECODING INTO SINGLE BRACKETS")
    return (0, 0)


# Decodes the body code into an actual instruction
def decodeInstructionIntoBody(bodyCode):
    if bodyCode == 0:
        return ('halt',)
    
    power, num = decodeListInstruction(bodyCode)
    if power % 2 != 0: # if odd, we have <<2*x + 1, <j, k> >>
        x = int((power - 1) / 2)
        j, k = decodeIntoSingleBrackets(num)
        return ('dec', x, j, k)

    return ('inc', power, num)

# String representation of an instruction
def instructionString(instr):
    if instr[0] == "halt":
        return "HALT"
    
    if instr[0] == "inc":
        return "R" + str(instr[1]) + "+ -> L" + str(instr[2])

    return "R" + str(instr[1]) + "- -> L" + str(instr[2]) + ", L" + str(instr[3])

# Prints the decoded program for the encoded instruction list
# Returns the program list
def decodeListIntoProgram(encodedInstrsList):
    program = []
    for instr in encodedInstrsList:
        instr = decodeInstructionIntoBody(instr)
        program.append(instr)
    return program


# Decodes into a program, without printing (for web app)
def decodeIntoProgram(code):
    encodedInstrs = decodeIntoList(code)
    prog = decodeListIntoProgram(encodedInstrs)

    label = 0
    programText = ""
    for instr in prog:
        programText += "L" + str(label) + ": " + instructionString(instr) + "\n"
        label += 1
    
    return programText

# Decodes into a program and prints it
def decodeAndPrintProgram(code):
    encodedInstrs = decodeIntoList(code)
    prog = decodeListIntoProgram(encodedInstrs)

    label = 0
    for instr in prog:
        print("L" + str(label) + ": " + instructionString(instr))
        label += 1


# code = (2 ** 94) * 16395
# decodeAndPrintProgram(code)
