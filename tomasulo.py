class inst:
    def __init__(self, opcode, dest, src1, src2):
        self.opcode = int(opcode)
        self.dest = int(dest)
        self.src1 = int(src1)
        self.src2 = int(src2)


instQueue = []
registerFiles = []
rat = []
add_RS = []
mul_RS = []
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
    for item in lines[numInst+2:]:
        registerFiles.append(item)
        # print(item)

for cc in range(cycles):
    #dispatch
    if (add_RS):
        print(add_RS.pop(0).opcode)
    #issue
    if (instQueue):
        currentInstruction = instQueue.pop(0)
        print("current instruction: " + str(currentInstruction.opcode))
        if(currentInstruction.opcode == 0):
            if(len(add_RS) < 3):
                add_RS.append(currentInstruction)
                rat.insert(currentInstruction.dest, )
            else:
                instQueue.insert(0,currentInstruction)


        elif(currentInstruction.opcode == 1):
            if(len(add_RS)  < 3):
                add_RS.append(currentInstruction)
            else:
                instQueue.insert(0,currentInstruction)


        elif(currentInstruction.opcode == 2):
            if(len(mul_RS)  < 2):
                mul_RS.append(currentInstruction)
            else:
                instQueue.insert(0,currentInstruction)


        elif(currentInstruction.opcode == 3):
            if(len(mul_RS)   < 2):
                mul_RS.append(currentInstruction)
            else:
                instQueue.insert(0,currentInstruction)

