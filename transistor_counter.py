class module: 
    def __init__(self, text):
        mod_text = combine_lines(text)
        self.name = getModName(mod_text)
        self.trans_count= getModTransCount(mod_text)
        self.inputs = getModInputs(mod_text)
        self.outputs = getModOutputs(mod_text)
        self.wires =  getModWires(mod_text)
        self.modules = getModInnerModules(mod_text)
        self.assigns = getModAssigns(mod_text)

    def __str__(self):
        string = "\n//////////////////////\nModule name: " + self.name + "\nTransistor count: " + str(self.trans_count)
        string = string + "\nInputs: " + str(self.inputs) + "\nOutputs: " + str(self.outputs)
        string = string + "\nWires: " + str(self.wires) + "\nAssigns: " + str(self.assigns) + "\nModules: " + str(self.modules)
        return string
    def getName(self):
        return self.name
    def getTransCount(self):
        return self.trans_count
    def setTransCount(self, count):
        self.trans_count = count
        
    
    
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
        current = current + i
        if (i == ';'):
            combined_lines.append(current.strip().replace('\n', ' '))
            current = ''
    return combined_lines

def getModTransCount(text):

    transCount = 0
    for line in text[1:-1]:
        transCount = transCount + countTransistorsInLine(line)
    return transCount
    # TODO
    
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
    
def getModName(text):
    split_text = text
    first_line = split_text[0]
    split_line = first_line.split('(')
    first_split = split_line[0]
    space_split = first_split.split(' ')
    return space_split[1].strip()

def getModInputs(text):
    inputs = []
    for line in text[1:-1]:
        if (line[0:5] == 'input'):
            inputs.append(line.strip())
    return inputs

def getModOutputs(text):
    outputs = []
    for line in text[1:-1]:
        if (line[0:6] == 'output'):
            
            outputs.append(line.strip())
    return outputs

def getModWires(text):
    wires = []
    current = ""
    for line in text[1:-1]:
        if (line[0:4] == 'wire'):
            wires.append(line)
    return wires

def getModAssigns(text): 
    assigns = []
    for line in text[1:-1]:
        if (line[0:6] == 'assign'):
            assigns.append(line.strip())
    return assigns

def getModInnerModules(text):
    modules = []
    for line in text[1:-1]:
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
    
def parseInputFile(filename):
    
    file = open(filename, "r")

    line = file.readline().strip()
    modules = set()
        
    # This is looped until the end of the file is reached. 
    while (line is not "") : 

        line = line.split("/")[0]

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
            line = file.readline().strip()
            # Until module ends
            while (line[0:9] != "endmodule"):
                if not line: 
                    pass
                elif (line[0] == "/" and line[1] == "/"):
                    pass
                else:
                    current_mod = current_mod + line + "\n"

                line = file.readline().strip()
            current_mod = current_mod + "endmodule\n"
            modules.add(current_mod)

        line = file.readline()
        
    


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

    for mod in modules:
        current_mod = module(mod)
        print(current_mod)


if __name__ == "__main__":
    __main__()
