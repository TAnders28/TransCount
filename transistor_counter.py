import queue
from typing import NewType

"""
Class representing a single verilog module with interior attributes representing:
name, transistor count, inputs, outputs, wires, inner modules, and assign statements
"""
class module: 
    def __init__(self, text):
        mod_text = combine_lines(text)
        first_line = mod_text[0]

        self.trans_count = -1

        self.name = getParseModName(first_line) # PARSE IMPLEMENTED
        self.inputs = parseModInputs(getModInputs(mod_text)) # PARSE IMPLEMENTED 
        self.outputs = parseModOutputs(getModOutputs(mod_text)) # PARSE IMPLEMENTED
        self.wires =  parseModWires(getModWires(mod_text)) # PARSE IMPLEMENTED
        self.modules = parseModInnerModules(getModInnerModules(mod_text)) # PARSE IMPLEMENTED
        self.assigns = getModAssigns(mod_text) #!! PARSE UNIMPLEMENTED

    # __str__ shows a formatted version of attributes
    def __str__(self):
        input_string = ""
        for i in self.inputs:
            input_string += i[0] + " : width " + str(i[1]) + "\n"

        input_string += "\n"
            
        output_string = ""
        for o in self.outputs:
            output_string += o[0] + " : width " + str(o[1]) + "\n"

        output_string += "\n"
        
        wire_string = ""
        for w in self.wires:
            wire_string += w[0] + " : width " + str(w[1]) + "\n"
        
        wire_string += "\n"

        string = "\n//////////////////////\nModule name: " + self.name + "\nTransistor count: " + str(self.trans_count)
        string = string + "\nInputs:\n" + input_string + "\nOutputs:\n" + output_string
        string = string + "\nWires:\n" + wire_string + "\nAssigns:\n" + str(self.assigns) + "\nModules:\n" + str(self.modules)
        return string
        
    # Getter 
    def getName(self):
        return self.name
    
    # Getter for modules field
    def getModules(self):
        return self.modules

    # Calculates transistor count
    def getTransCount(self):
        print("\n//////////////////////\n" + "Analysis of " + self.name)
        print("\nModules: " + str(list(enumerate(self.modules, 1))) + "\n")

        current_count = 0
        error_count = 0
        module_count = 1

        for module in self.modules:
            if module[0] in known_input_independent.keys():
                current_count += known_input_independent.get(module[0])
            elif module[0] in known_input_dependent.keys():
                current_count += known_input_dependent.get(module[0])[0] + known_input_dependent.get(module[0])[1]*module[1]
            elif module[0] in inner_modules.keys():
                current_count += inner_modules.get(module[0])
            else:
                error_count += 1
                print("Error at module #" + str(module_count))
            module_count += 1

        self.trans_count = current_count
        print("\n" + str(error_count) + " total errors  in " + self.name + "\n")
        print("Total transistors: " + str(current_count))
        inner_modules.update({self.name : current_count})

known_input_dependent = {
        'and' : (1,1), 
        'or' : (1,1), 
        'nand' : (0,1),
        'nor' : (0,1),
        'xor' : (0,4)
    }
known_input_independent = {
        'not' : 1,
        'bufif1' : 6
    }

inner_modules = {}
    
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
Gets and parses for the module name given a preformatted list of strings
"""
def getParseModName(first_line):
    split_line = first_line.split('(')
    first_split = split_line[0]
    space_split = first_split.split(' ')
    return space_split[1].strip()

"""
Gets the lines representing inputs from a module string
"""
def getModInputs(text):
    inputs = []
    for line in text[1:]:
        if (line[0:5] == 'input'):
            inputs.append(line.strip())
    return inputs
"""
Parses lines representing inputs
"""
def parseModInputs(text):
    inputs = []
    for input in text:
        if ('[' and ']' in input):
            range = input.split('[')[1].split(']')[0]
            length = int(range.split(':')[0]) - int(range.split(':')[1]) + 1
            names = input.split(']')[1].split(', ')
        else: 
            length = 1
            names = input.split(' ')[1].split(', ')
        for name in names:
            parsed = (format(name),length)
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
            names = output.split(']')[1]
            names = names.split(',' )
        else: 
            length = 1
            names = output.split(' ')[1].split(', ')
        for name in names:
            parsed = (format(name),length)
            outputs.append(parsed)
    return outputs

def format(text):
    new = text.replace(';','').replace(',','').strip()
    return new




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
            names = wire.split(']')[1]
            names = names.split(',' )
        else: 
            length = 1
            names = wire.split(' ')[1].split(', ')
        for name in names:
            parsed = (format(name),length)
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
        name = module.split('(')[0].strip()
        if (len(name.split(' ')) == 2):
            name = name.split(' ')[0]
        modules.append((name, count))
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


   # Get all of the modules into a set
    parsed_modules = set()
    for mod in modules:
        current_mod = module(mod)
        # TEMPORARILY REMOVED FOR TESTING
        # print(current_mod)
        parsed_modules.add(current_mod)

    for mod in parsed_modules:
        print(mod)

    analyzed_modules = []

    #
    while (not len(parsed_modules) == 0):

        current = parsed_modules.pop()
        current_inner_modules = current.getModules()
        
        known_modules = list(known_input_dependent.keys())
        known_modules += list(known_input_independent.keys())
        known_modules += list(inner_modules.keys())
        ready = True
        
        #
        for (name, _) in current_inner_modules:
            
            #
            if name.strip() not in known_modules:
                ready = False

        #
        if ready: 
            current.getTransCount()
            analyzed_modules.append(current)
        #
        else: 
            parsed_modules.add(current)
    #
    for mod in analyzed_modules:
        print(mod)
        
    


if __name__ == "__main__":
    __main__()
