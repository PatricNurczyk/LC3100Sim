# Variables
MAX_MEM_SIZE = 65536
NUM_REG = 8
Pc = 0
Memory = []
Register = []
Halt = False


def print_state(pc, mem, reg):
    print("\n@@@\nstate:")
    print("\tpc " + str(pc))
    print("\tmemory:")
    for i in mem:
        print("\t\tmem[ " + str(mem.index(i)) + " ] " + str(i))
    print("\tregisters:")
    for i in range(NUM_REG):
        print("\t\treg[ " + str(i) + " ] " + str(reg[i]))
    print("end state\n")


def int_to_bin(input):
    input = bin(input)[2:]
    binum = "0"
    for j in range(31 - len(input)):
        binum = binum + "0"
    input = binum + input
    return input


def add_inst(num):
    # Getting Registers A and B
    RegA = Register[int(f"0b{num[10:13]}", 2)]
    RegB = Register[int(f"0b{num[13:16]}", 2)]

    # Getting the Destination Register
    if num[29:] == "000":
        print(f"Error in Memory Location {Pc}, Cannot write to Register 0")
        return True

    # Running the Add into Destination Register
    Register[int(f"0b{num[29:]}, 2")] = RegA + RegB
    return False


def nand_inst(num):
    return True


def op_code(num):
    opcode = num[7:10]
    print(opcode)
    # Halt
    if opcode == "110":
        return True
    elif opcode == "000":
        return add_inst(num)
    elif opcode == "001":
        return nand_inst(num)


for i in range(NUM_REG):
    Register.append(0)
print(Register)
print("Welcome to the LC3100 Simulator")
print("This Simulator will take existing machine code and output the results to a text file 'Output'")
print("Enter the File Name containing Machine Code")
f = open(input("FileName: ") + ".txt", "rt")
line = f.readline()
while line != '':
    Memory.append(int(line))
    line = f.readline()
for i in Memory:
    print("Memory[" + str(Memory.index(i)) + "] = " + str(i))
while not Halt and Pc < len(Memory):
    # First We print the state
    print_state(Pc, Memory, Register)
    # We convert the integer to a binary string
    curr = int_to_bin(Memory[Pc])
    Halt = op_code(curr)
    Pc += 1
