class module: 
    def __init__(self, mod_text):
        self.name = getModName(mod_text)
        self.trans_count= getTransCount(mod_text)
        self.inputs = getInputs(mod_text)
        self.outputs = getOutputs(mod_text)
        self.wires =  getWires(mod_text)
        self.modules = getModules(mod_text)
        self.assigns = getAssigns(mod_text)

    def __str__(self):
        string = "\n//////////////////////\nModule name: " + self.name + "\nTransistor count: " + str(self.trans_count)
        string = string + "\nInputs: " + str(self.inputs) + "\nOutputs: " + str(self.outputs)
        string = string + "\nWires: " + str(self.wires) + "\nModules: " + str(self.modules)
        return string
    def getName(self):
        return self.name
    def getTransCount(self):
        return self.trans_count
    def setTransCount(self, count):
        self.trans_count = count
        
    
def getModName(text):
    split_text = text.splitlines()
    first_line = split_text[0]
    split_line = first_line.split('(')
    first_split = split_line[0]
    space_split = first_split.split(' ')
    return space_split[1].strip()

    
def getTransCount(text):

    transCount = 0
    for line in text.splitlines()[1:-1]:
        transCount = transCount + countTransistorsInLine(line)
    return transCount
    # TODO

def getInputs(text):
    inputs = []
    for line in text.splitlines()[1:-1]:
        if (line[0:5] == 'input'):
            inputs.append(line.strip())
    return inputs
    

def getOutputs(text):
    outputs = []
    for line in text.splitlines()[1:-1]:
        if (line[0:6] == 'output'):
            outputs.append(line.strip())
    return outputs

def getWires(text):
    wires = []
    for line in text.splitlines()[1:-1]:
        if (line[0:4] == 'wire'):
            wires.append(line.strip())
    return wires

def getAssigns(text): 
    assigns = []
    for line in text.splitlines()[1:-1]:
        if (line[0:6] == 'assign'):
            assigns.append(line.strip())
    return assigns



def getModules(text):
    modules = []
    for line in text.splitlines()[1:-1]:
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
