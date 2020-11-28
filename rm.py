# instruction: ('halt'), ('inc', reg, next_line)
#                        ('dec', reg, success_line, fail_line)

import pickle

def parse_line(line, program):
    line = line.lower()
    if line == "halt":                  # "halt"
        program.append(("halt",))
        return program
   
    if "+" in line:                     # "r3+ -> l2"
        l_str = line.split("->")
        reg = int("".join([c for c in l_str[0] if c.isdigit()]))
        line = int("".join([c for c in l_str[1].strip() if c.isdigit()]))
        program.append(('inc', reg, line))
        return program
   
    # now it must be decrement, of format "r3- -> l2, l4"
    l_str = line.split("->")
    reg = int("".join([c for c in l_str[0] if c.isdigit()]))
   
    dst_line_str = l_str[1].strip().split(",")
    s_line = int("".join([c for c in dst_line_str[0] if c.isdigit()]))
    f_line = int("".join([c for c in dst_line_str[1] if c.isdigit()]))

    program.append(('dec', reg, s_line, f_line))
    return program

def execute_program(program, initConfig):
    config = initConfig.copy()
    index = 0
    while True:
        instr = program[index]
       
        if instr[0] == 'halt':
            return config

        if instr[0] == 'inc':
            config[instr[1]] += 1
            index = instr[2]
            continue
       
        if instr[0] == 'dec':
            if config[instr[1]] == 0:
                index = instr[3]
            else:
                config[instr[1]] -= 1
                index = instr[2]
    return config


def execute_program_from_cmd_line():
    program = []
    config = []
    max_reg = 0

    if (input("Load program from file? [y: enter file name, n: enter new] \n") == 'y'):
        fname = input("File name (w/o extension): ")
        with open(fname + ".pickle", "rb") as fp:
            program = pickle.load(fp)
    else:
        # Parse the program from stdin
        i = 0
        line = input("Enter L" + str(i) + ": ")
        while(line != ""):
            program = parse_line(line, program)
            i += 1
            line = input("Enter L" + str(i) + ": ")

        if (input("Save program to file? [y/n] ") == 'y'):
            fname = input("File name (w/o extension): ")
            with open(fname + ".pickle", "wb") as fp:
                pickle.dump(program, fp)

    # Get the maximum indexed register (nth register)
    for instr in program:
        if instr[0] == 'inc' or instr[0] == 'dec':
            if instr[1] > max_reg:
                max_reg = instr[1]

    # Get the initial configuration
    while len(config) != max_reg + 1:
        config_str = input("Enter the initial configuration for R0 to R" + str(max_reg) + ", space-separated:'r0 ... r" + str(max_reg) + "': ")
        config = config_str.split(" ")

    config = list(map(int, config))

    config = execute_program(program, config)
    print("Final configuration is: ")
    print(config)


# execute_program_from_cmd_line()


########## for the web app ############
def execute_program_from_lines_and_config(lines, initialConfiguration):
    program = []
    for line in lines:
        program = parse_line(line, program)
    
    finalConfig = execute_program(program, initialConfiguration)
    return finalConfig
    