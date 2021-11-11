class inst:
    def __init__(self, opcode, dest, src1, src2):
        self.opcode = opcode
        self.dest = dest
        self.src1 = src1
        self.src2 = src2

instQueue = []
registerFile = []
rat = [8]

with open('myfile.txt') as fp:
    lines = fp.readlines()
    numInst = int(lines[0])
    print(numInst)
    cycles = lines[1]
    print(cycles)
    for x in range(numInst):
        vars = lines[x+2].split()
        instQueue.append(inst(vars[0],vars[1],vars[2],vars[3]))
        print(lines[x+2])
    for item in lines[numInst+2:]:
        registerFile.append(item)
        print(item)


    