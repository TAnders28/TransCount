class module: 
    def __init__(self, name, trans_count):
        self.name = name
        self.trans_count = trans_count
        self.prop_delay = prop_delay
    def getName(self):
        return self.name
    def getTransCount(self):
        return self.trans_count
    def setTransCount(self, count):
        self.trans_count = count


def getModName(mod_text):
    split_text = mod_text.splitlines()
    first_line = split_text[0]
    split_line = first_line.split('(')
    first_split = split_line[0]
    space_split = first_split.split(' ')
    return space_split[1]

    
def getTransCount(mod_text):
    return 0

    # TODO



def __main__():
    filename = input("Input the name of the .v file you wish to analyze: ")
    file = open(filename, "r")
    known = {
        'and' : 2, 
        'or' : 2, 
        'nand' : 1,
        'nor' : 1, 
        'not' : 1
    }

    line = file.readline()
    line = line.strip()
    modules = set()
        
    # This is looped until the end of the file is reached. 
    while (line is not "") : 

        # Remove blank spaces
        while (line[0] == " "):
            line = line[1:]
        # Skip lines with comments only 
        while (line[0] == "/" and line[1] == "/"): 
            line = file.readline()
        
        # Identify modules
        if (line[0:6] == "module"):
            current_mod = line
            line = file.readline().strip()
            # Until module ends
            while (line[0:9] != "endmodule"):
                if not line: 
                    pass
                elif (line[0] == "/" and line[1] == "/"):
                    pass
                else:
                    current_mod = current_mod + line + "\n"

                line = file.readline()
                line = line.strip()
            # current_mod = current_mod.replace(" ", "")
            current_mod = current_mod + "endmodule\n"
            modules.add(current_mod)

        line = file.readline()
        
    

    for mod in modules:
        name = getModName(mod)
        transCount = getTransCount(mod)

        print(name)
        print("\n///////////////////////////////////////////////////\n")
        
    




if __name__ == "__main__":
    __main__()
