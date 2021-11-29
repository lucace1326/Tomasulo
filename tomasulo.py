class instr:
    def __init__(self, opcode, dest, src1, src2):
        self.opcode = int(opcode)
        self.dest = (dest)
        self.src1 = (src1)
        self.src2 = (src2)
        self.doneTime = 0
        self.val1 = None
        self.val2 = None

    def setVals(self):
        if("rf" in rat[int(self.src1)] and self.val1 == None):
            self.val1 = registerFiles[int(self.src1)]
        if("rf" in rat[int(self.src2)] and self.val2 == None):
            self.val2 = registerFiles[int(self.src2)]

    def execute(self):
        if(self.opcode == 0):
            return self.val1 + self.val2
        if(self.opcode == 1):
            return self.val1 - self.val2
        if(self.opcode == 2):
            return self.val1 * self.val2
        if(self.opcode == 3):
            return self.val1 / self.val2

    def print(self):
        if(self.opcode == 0):
            return "RF" + self.dest + " = RF" + self.src1 + " + RF" + self.src2
        if(self.opcode == 1):
            return "RF" + self.dest + " = RF" + self.src1 + " - RF" + self.src2
        if(self.opcode == 2):
            return "RF" + self.dest + " = RF" + self.src1 + " * RF" + self.src2
        if(self.opcode == 3):
            return "RF" + self.dest + " = RF" + self.src1 + " / RF" + self.src2


instQueue = []
registerFiles = []
rat = []
add_RS = []
mul_RS = []
dispatch_inst_ADD = None
dispatch_inst_MUL = None
with open('myfile.txt') as fp:
    lines = fp.readlines()
    numInst = int(lines[0])
    # print(numInst)
    cycles = int(lines[1])
    # print(cycles)
    for x in range(numInst):
        vars = lines[x+2].split()
        instQueue.append(instr(vars[0], vars[1], vars[2], vars[3]))
        # print(lines[x+2])
    i = 0
    for item in lines[numInst+2:]:
        registerFiles.append(int(item))
        rat.append("rf" + str(i))
        i += 1

for cc in range(cycles+1):
    # display
    print("Clock Cycle = " + str(cc))
    print("RAT = ", end='')
    for x in rat:
        print(x, end=' ')
    print()
    print("RF  = ", end='')
    for x in registerFiles:
        print(str(x).rjust(3), end=' ')
    print()
    print("Instruction Queue = ")
    for x in instQueue:
        print(x.print())
    print("Reservation Stations = ")
    for x in add_RS:
        print(x.print())
    for x in mul_RS:
        print(x.print())
        
# broadcast
    if((dispatch_inst_MUL != None) and cc == dispatch_inst_MUL.doneTime):
        print("----------->>BROADCAST: " + dispatch_inst_MUL.print())
        rat[int(dispatch_inst_MUL.dest)] = "rf"+dispatch_inst_MUL.dest
        registerFiles[int(dispatch_inst_MUL.dest)] = dispatch_inst_MUL.execute()
        mul_RS.remove(dispatch_inst_MUL)
        for x in add_RS:
            x.setVals()
        for x in mul_RS:
            x.setVals()
        dispatch_inst_MUL = None
    elif((dispatch_inst_ADD != None) and cc == dispatch_inst_ADD.doneTime):
        print("----------->>BROADCAST: " + dispatch_inst_ADD.print())
        rat[int(dispatch_inst_ADD.dest)] = "rf"+dispatch_inst_ADD.dest
        registerFiles[int(dispatch_inst_ADD.dest)] = dispatch_inst_ADD.execute()
        add_RS.remove(dispatch_inst_ADD)
        for x in add_RS:
            x.setVals()
        for x in mul_RS:
            x.setVals()
        dispatch_inst_ADD = None        

# dispatch
    for instr in mul_RS:
        if( (dispatch_inst_MUL == None) and (instr.val1 != None) and (instr.val2 != None)):
            print("----------->>DISPATCH: " + instr.print())
            dispatch_inst_MUL = instr
            if(dispatch_inst_MUL.opcode == 2):
                dispatch_inst_MUL.doneTime = cc+10
            elif(dispatch_inst_MUL.opcode == 3):
                dispatch_inst_MUL.doneTime = cc+40
            break
    for instr in add_RS:
        if( (dispatch_inst_ADD == None) and (instr.val1 != None) and (instr.val2 != None)):
            print("----------->>DISPATCH: " + instr.print())
            dispatch_inst_ADD = instr
            dispatch_inst_ADD.doneTime = cc+2
            break

# issue
    if (instQueue):
        currentInstruction = instQueue.pop(0)
        if(currentInstruction.opcode == 0 or currentInstruction.opcode == 1):
            if(len(add_RS) < 3):
                add_RS.append(currentInstruction)
                currentInstruction.setVals()
                rat[int(currentInstruction.dest)] = "RS"+str(len(add_RS))
            else:
                instQueue.insert(0, currentInstruction)

        elif(currentInstruction.opcode == 2):
            if(len(mul_RS) < 2):
                mul_RS.append(currentInstruction)
                currentInstruction.setVals()
                rat[int(currentInstruction.dest)] = "RS"+str(len(mul_RS)+3)
            else:
                instQueue.insert(0, currentInstruction)

        elif(currentInstruction.opcode == 3):
            if(len(mul_RS) < 2):
                mul_RS.append(currentInstruction)
                currentInstruction.setVals()
                rat[int(currentInstruction.dest)] = "RS"+str(len(mul_RS)+3)
            else:
                instQueue.insert(0, currentInstruction)
    print()
