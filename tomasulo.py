class inst:
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
dispatch_inst = None
with open('myfile.txt') as fp:
    lines = fp.readlines()
    numInst = int(lines[0])
    # print(numInst)
    cycles = int(lines[1])
    # print(cycles)
    for x in range(numInst):
        vars = lines[x+2].split()
        instQueue.append(inst(vars[0], vars[1], vars[2], vars[3]))
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
    if(dispatch_inst != None and cc == dispatch_inst.doneTime):
        rat[int(dispatch_inst.dest)] = "rf"+dispatch_inst.dest
        registerFiles[int(dispatch_inst.dest)] = dispatch_inst.execute()
        if(dispatch_inst.opcode == 0 or dispatch_inst.opcode == 1):
            add_RS.pop(0)
        else:
            mul_RS.pop(0)
        for x in add_RS:
            x.setVals()
        for x in mul_RS:
            x.setVals()
        dispatch_inst = None

# dispatch
    if mul_RS and dispatch_inst == None:
        if(mul_RS[0].val1 != None) and (mul_RS[0].val2 != None):
            dispatch_inst = mul_RS[0]
            if(dispatch_inst.opcode == 2):
                dispatch_inst.doneTime = cc+10
            elif(dispatch_inst.opcode == 3):
                dispatch_inst.doneTime = cc+40
    elif add_RS and dispatch_inst == None:
        if(add_RS[0].val1 != None) and (add_RS[0].val2 != None):
            dispatch_inst = add_RS[0]
            dispatch_inst.doneTime = cc+2

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
