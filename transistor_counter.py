"""
Class representing a single verilog module with interior attributes representing:
name, transistor count, inputs, outputs, wires, inner modules, and assign statements
"""
class module: 
    def __init__(self, text):
        mod_text = combine_lines(text)
        first_line = mod_text[0]

        self.trans_count = -1
        self.name = getParseModName(first_line)
        self.inputs = parseModInputs(getModInputs(mod_text)) # PARSE IMPLEMENTED 
        self.outputs = parseModOutputs(getModOutputs(mod_text)) # PARSE IMPLEMENTED
        self.wires =  parseModWires(getModWires(mod_text))
        self.modules = parseModInnerModules(getModInnerModules(mod_text))
        self.assigns = getModAssigns(mod_text) #!!!UNIMPLEMENTED

    # __str__ shows a formatted version of attributes
    def __str__(self):
        input_string = ""
        for i in self.inputs:
            input_string += i[1] + " : width " + str(i[0]) + "\n"

        input_string += "\n"
            
        output_string = ""
        for o in self.outputs:
            output_string += o[1] + " : width " + str(o[0]) + "\n"

        output_string += "\n"
        
        wire_string = ""
        for w in self.wires:
            wire_string += w[1] + " : width " + str(w[0]) + "\n"
        
        wire_string += "\n"

        string = "\n//////////////////////\nModule name: " + self.name + "\nTransistor count: " + str(self.trans_count)
        string = string + "\nInputs:\n" + input_string + "\nOutputs:\n" + output_string
        string = string + "\nWires:\n" + wire_string + "\nAssigns:\n" + str(self.assigns) + "\nModules:\n" + str(self.modules)
        return string
        
    # Getter - currently unused
    def getName(self):
        return self.name

    def getTransCount(self):
        current_count = 0
        for module in self.modules:
            if module[1] in known_input_independent.keys():
                current_count += known_input_independent.get(module[1])
            elif module[1] in known_input_dependent.keys():
                current_count += known_input_dependent.get(module[1])[0] + known_input_dependent.get(module[1])[1]*module[0]
            else:
                print("error")
        self.trans_count = current_count

known_input_dependent = {
        'and' : (1,1), 
        'or' : (1,1), 
        'nand' : (0,1),
        'nor' : (0,1),
        'xor' : (0,4)
    }
known_input_independent = {
        'not' : 1
    }
    
"""
Method that combines and formats the lines of a verilog file, which 
is syntactically separated by semicolons(';'). Right now,
the formatting only removes newline characters
"""
def combine_lines(text):
    combined_lines = []
    current = ''
    setPass = False
    for i in text:
        if (i == "\n"):
            setPass = False
        if (i == "/"):
            setPass = True
        if (setPass):
            continue
        current += i
        if (i == ';'):
            combined_lines.append(current.strip().replace('\n', ' '))
            current = ''
    return combined_lines
"""
Calculates transistor count based on interior characteristics.
"""
def getModTransCount(text):

    transCount = 0
    for line in text[1:-1]:
        transCount = transCount + countTransistorsInLine(line)
    return transCount
    # TODO

"""
Helper method for getModTransCount.
Counts the transistors in one line.

"""
def countTransistorsInLine(line):
    if (line[0:5] == 'input'):
        return 0
    elif (line[0:6] == 'output'):
        return 0
    elif (line[0:4] == 'wire'):
        return 0
    elif (line[0:6] == 'assign'):
        return 0
    else: 
        split_line = line.split('(')
        gate = split_line[0]
        return 1
"""
Gets and parses for the module name given a preformatted list of strings
"""
def getParseModName(first_line):
    split_line = first_line.split('(')
    first_split = split_line[0]
    space_split = first_split.split(' ')
    return space_split[1].strip()


def getModInputs(text):
    inputs = []
    for line in text[1:]:
        if (line[0:5] == 'input'):
            inputs.append(line.strip())
    return inputs
def parseModInputs(text):
    inputs = []
    for input in text:
        if ('[' and ']' in input):
            range = input.split('[')[1].split(']')[0]
            length = int(range.split(':')[0]) - int(range.split(':')[1]) + 1
        else: 
            length = 1
            
        name = input.split(' ')[-1].split(';')[0]
        parsed = (length, name)
        inputs.append(parsed)

    return inputs




def getModOutputs(text):
    outputs = []
    for line in text[1:]:
        if (line[0:6] == 'output'):
            outputs.append(line.strip())
    return outputs
def parseModOutputs(text):
    
    outputs = []
    for output in text:
        if ('[' and ']' in output):
            range = output.split('[')[1].split(']')[0]
            length = int(range.split(':')[0]) - int(range.split(':')[1]) + 1
        else: 
            length = 1
            
        name = output.split(' ')[-1].split(';')[0]
        parsed = (length, name)
        outputs.append(parsed)
            
    return outputs


def getModWires(text):
    wires = []
    for line in text[1:]:
        if (line[0:4] == 'wire'):
            wires.append(line)
    return wires
def parseModWires(text):
    wires = []
    for wire in text:
        if ('[' and ']' in wire):
            range = wire.split('[')[1].split(']')[0]
            length = int(range.split(':')[0]) - int(range.split(':')[1]) + 1
        else: 
            length = 1
        
        name = wire.split(' ')[-1].split(';')[0]
        parsed = (length, name)
        wires.append(parsed)
            
    return wires

def getModAssigns(text): 
    assigns = []
    for line in text[1:]:
        if (line[0:6] == 'assign'):
            assigns.append(line.strip())
    return assigns
def parseModAssigns(text):
    pass

def getModInnerModules(text):
    modules = []
    for line in text[1:]:
        if (line[0:5] == 'input'):
            pass
        elif (line[0:6] == 'output'):
            pass
        elif (line[0:4] == 'wire'):
            pass
        elif (line[0:6] == 'assign'):
            pass
        else: 
            modules.append(line.strip())
    return modules

def parseModInnerModules(text):
    modules = []
    for module in text:
        count = module.count(',')
        name = module.split('(')[0]
        modules.append((count, name))
    return modules
    



def parseInputFile(filename):
    
    file = open(filename, "r")

    line = file.readline().strip()
    modules = set()
        
    # This is looped until the end of the file is reached. 
    while (line is not "") : 

        line = line.strip()

        # Skip lines with comments only 
        if (not line or not line[1]):
            pass
        elif (line[0] == "/" and line[1] == "/"): 
            line = file.readline()
        
        # Identify modules
        if (line[0:6] == "module"):
            current_mod = line + "\n"
            line = file.readline().strip().split('/')[0]
            # Until module ends
            while (line[0:9] != "endmodule"):
                if not line: 
                    pass
                elif (line[0] == "/" and line[1] == "/"):
                    pass
                else:
                    current_mod = current_mod + line + "\n"

                line = file.readline().strip().split('/')[0]
            current_mod = current_mod + "endmodule\n"
            modules.add(current_mod)

        line = file.readline()
    return modules
        

def __main__():
    filename = input("Input the name of the .v file you wish to analyze: ")
    modules = parseInputFile(filename)

   

    for mod in modules:
        current_mod = module(mod)
        current_mod.getTransCount()

        print(current_mod)


if __name__ == "__main__":
    __main__()
