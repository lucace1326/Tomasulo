class inst:
    def __init__(self, opcode, dest, src1, src2):
        self.opcode = int(opcode)
        self.dest = (dest)
        self.src1 = (src1)
        self.src2 = (src2)

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
    i=0
    for item in lines[numInst+2:]:
        i+=1
        registerFiles.append(item)
        rat.append("rf" + str(i))

for cc in range(cycles+1):
    #display
    print("Clock Cycle = " +str(cc))
    print("RAT = " )
    for x in rat:
        print(x)
    #dispatch
    if (add_RS):
        dispatch_inst = add_RS.pop(0)
        execute(dispatch_inst)
    #issue
    if (instQueue):
        currentInstruction = instQueue.pop(0)
        if(currentInstruction.opcode == 0):
            if(len(add_RS) < 3):
                if(rat[int(currentInstruction.src1)] != "rf"+currentInstruction.src1):
                    currentInstruction.src1 = rat[int(currentInstruction.src1)]
                if(rat[int(currentInstruction.src2)] != "rf"+currentInstruction.src2):
                    currentInstruction.src2 = rat[int(currentInstruction.src2)]
                add_RS.append(currentInstruction)
                rat[int(currentInstruction.dest)-1] = "RS"+str(len(add_RS))
            else:
                instQueue.insert(0,currentInstruction)


        elif(currentInstruction.opcode == 1):
            if(len(add_RS)  < 3):
                add_RS.append(currentInstruction)
                rat.insert(currentInstruction.dest, len(add_RS))
            else:
                instQueue.insert(0,currentInstruction)


        elif(currentInstruction.opcode == 2):
            if(len(mul_RS)  < 2):
                mul_RS.append(currentInstruction)
                rat.insert(currentInstruction.dest, len(mul_RS))
            else:
                instQueue.insert(0,currentInstruction)


        elif(currentInstruction.opcode == 3):
            if(len(mul_RS)   < 2):
                mul_RS.append(currentInstruction)
                rat.insert(currentInstruction.dest, len(mul_RS))
            else:
                instQueue.insert(0,currentInstruction)

