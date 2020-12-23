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


def getModName(full_text):
    return ""
    # TODO

    
def getTransCount(full_text):
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

        current_mod = ""
        if (line[0:6] == "module"):
            while (line[0:9] != "endmodule"):
                current_mod = current_mod + line.strip() + "\n"
                line = file.readline()
        modules.add(current_mod)

        line = file.readline()
        
    

    for mod in modules:
        name = getModName(mod)
        transCount = getTransCount(mod)

        print(mod)
        print("///////////////////////////////////////////////////\n")
        
    




if __name__ == "__main__":
    __main__()
