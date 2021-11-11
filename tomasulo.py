class inst:
    def __init__(self, opcode, dest, src1, src2):
        self.opcode = opcode
        self.dest = dest
        self.src1 = src1
        self.src2 = src2


file1 = open("myfile.txt","r+")

print( "Output of Read function is ")
print( file1.read())
instQueue = []
registerFile = [8]
rat = [8]



    