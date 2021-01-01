import queue
from collections import Counter

"""
Class representing a single verilog module with interior attributes representing:
name, transistor count, inputs, outputs, wires, inner modules, and assign statements
"""
class module: 
    
    """
    Constructor
    """
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

    """
    Shows a formatted version of inner attributes
    """
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

        assign_string = "\n"
        for a in self.assigns:
            assign_string += a + "\n"
        assign_string += "\n"

        module_string = "\n"

        for val, count in dict(Counter(self.modules)).items():
            module_string += str(count) + "x " + val[0] + "\n"
        module_string += "\n"

        string = "\n//////////////////////\nModule name: " + self.name + "\nTransistor count: " + str(self.trans_count)
        string = string + "\nInputs:\n" + input_string + "\nOutputs:\n" + output_string
        string = string + "\nWires:\n" + wire_string + "\nAssigns:\n" + assign_string + "\nModules:\n" + module_string
        
        return string
    """
    Getter: 
    Return string representing name
    """
    def getName(self):
        return self.name
    
    """
    Getter:
    Return list of tuples in the format:
    (module, input_count)
    representing the interior modules of this module
    """
    def getModules(self):
        return self.modules

    """
    Calculates transistor count based on interior characteristics
    """
    def findTransCount(self):
        print("\n//////////////////////\n" + "Analysis of " + self.name)
        print("\nModules: " + str(list(enumerate(self.modules, 1))) + "\n")

        current_count = 0
        error_count = 0
        module_count = 1

        #
        for module in self.modules:
            if module[0] in known_input_independent.keys():
                current_count += known_input_independent.get(module[0])
            #
            elif module[0] in known_input_dependent.keys():
                current_count += known_input_dependent.get(module[0])[0] + known_input_dependent.get(module[0])[1]*module[1]
            #
            elif module[0] in known_modules.keys():
                current_count += known_modules.get(module[0])
            #
            else:
                error_count += 1
            module_count += 1

        self.trans_count = current_count
        known_modules.update({self.name : current_count})

#
known_input_dependent = {
        'and' : (1,1), 
        'or' : (1,1), 
        'nand' : (0,1),
        'nor' : (0,1),
        'xor' : (0,4)
    }

#
known_input_independent = {
        'not' : 1,
        'bufif1' : 6
    }
    
#
known_modules = {}
    
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
Gets the lines with inputs from a module string
"""
def getModInputs(text):
    inputs = []
    for line in text[1:]:
        if (line[0:5] == 'input'):
            inputs.append(line.strip())
    return inputs

"""
Parses inputs
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
            names = input.split('input ')[1].split(',')
        for name in names:
            parsed = (format(name),length)
            inputs.append(parsed)
    return inputs




"""
Gets the lines with outputs from a module string
"""
def getModOutputs(text):
    outputs = []
    for line in text[1:]:
        if (line[0:6] == 'output'):
            outputs.append(line.strip())
    return outputs
"""
Parses outputs
"""
def parseModOutputs(text):
    outputs = []
    for output in text:
        if ('[' and ']' in output):
            range = output.split('[')[1].split(']')[0]
            length = int(range.split(':')[0]) - int(range.split(':')[1]) + 1
            names = output.split(']')[1].split(',' )
        else: 
            length = 1
            names = output.split('output ')[1].split(',')
        for name in names:
            parsed = (format(name),length)
            outputs.append(parsed)
    return outputs


"""
Gets the lines with wires from a module string
"""
def getModWires(text):
    wires = []
    for line in text[1:]:
        if (line[0:4] == 'wire'):
            wires.append(line)
    return wires
"""
Parses wires
"""
def parseModWires(text):
    wires = []
    for wire in text:
        
        if ('[' and ']' in wire):
            range = wire.split('[')[1].split(']')[0]
            length = int(range.split(':')[0]) - int(range.split(':')[1]) + 1
            names = wire.split(']')[1].split(',')
        else: 
            length = 1
            names = wire.split('wire ')[1].split(',')
        for name in names:
            parsed = (format(name),length)
            wires.append(parsed)
    return wires

"""
Gets the lines with assign statements from a module string
"""
def getModAssigns(text): 
    assigns = []
    for line in text[1:]:
        if (line[0:6] == 'assign'):
            assigns.append(line.strip())
    return assigns

"""
Parses assign statements 
"""
def parseModAssigns(text):
    pass


"""
Gets lines with declared inner modules from a module string
"""
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

"""
Parses inner modules
"""
def parseModInnerModules(text):
    modules = []
    for module in text:
        count = module.count(',')
        name = module.split('(')[0].strip()
        if (len(name.split(' ')) == 2):
            name = name.split(' ')[0]
        modules.append((name, count))
    return modules
    

"""
Removes extra ';' and ',' characters
"""
def format(text):
    new = text.replace(';','').replace(',','').strip()
    return new



"""

"""
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
        

"""

"""
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

    #
    for mod in parsed_modules:
        print(mod)

    analyzed_modules = []

    #
    while (not len(parsed_modules) == 0):

        current = parsed_modules.pop()
        current_inner_modules = current.getModules()
        
        known = list(known_input_dependent.keys())
        known += list(known_input_independent.keys())
        known += list(known_modules.keys())
        ready = True
        
        #
        for (name, _) in current_inner_modules:
            
            #
            if name.strip() not in known:
                ready = False
                break
        #
        if ready: 
            current.findTransCount()
            analyzed_modules.append(current)
        #
        else: 
            parsed_modules.add(current)
    #
    for mod in analyzed_modules:
        print(mod)
        
    

"""
Shows a formatted version of attributes
"""
if __name__ == "__main__":
    __main__()
