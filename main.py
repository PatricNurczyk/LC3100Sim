# Variables
MAX_MEM_SIZE = 65536
NUM_REG = 8
Pc = 0
Memory = []
Register = []
Halt = False


def print_state(pc, mem, reg):
    print("\n@@@\nstate:")
    print(f"\tpc {pc}")
    print("\tmemory:")
    for i, j in enumerate(mem):
        print(f"\t\tmem[ {i} ] {j}")
    print("\tregisters:")
    for i, j in enumerate(reg):
        print(f"\t\treg[ {i} ] {j}")
    print("end state\n")


def int_to_bin(input):
    input = bin(input)[2:]
    binum = "0"
    for j in range(31 - len(input)):
        binum = binum + "0"
    input = binum + input
    return input


def two_comp(bitstring: str):
    # If the number is already Positive
    if bitstring[0] == '0':
        return int(f"0b{bitstring}", 2)
    # If the number is negative
    bit_list = list(bitstring)
    for ind, j in enumerate(bit_list):
        if j == '1':
            bit_list[ind] = '0'
        else:
            bit_list[ind] = '1'
    bitstring = "".join(bit_list)
    return -1 * (int(f"0b{bitstring}", 2) + 1)





def add_inst(num):
    # Getting Registers A and B
    RegA = Register[int(f"0b{num[10:13]}", 2)]
    RegB = Register[int(f"0b{num[13:16]}", 2)]

    # Getting the Destination Register
    if num[29:] == "000":
        print(f"Error in Memory Location {Pc}, Cannot write to Register 0")
        return True

    # Running the Add into Destination Register
    Register[int(f"0b{num[29:]}", 2)] = RegA + RegB
    return False


def nand_inst(num):
    return True


def lw_inst(num):
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])


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
    elif opcode == "010":
        return lw_inst(num)

print(str(two_comp("1111111111111111")))

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
