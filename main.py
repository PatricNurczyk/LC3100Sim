# Const Variables
MAX_MEM_SIZE = 65536
NUM_REG = 8


def print_state(pc, mem, reg):
    print("\n@@@\nstate:")
    print(f"\tpc {pc}")
    print("\tmemory:")
    for i, j in enumerate(mem):
        if j is not None:
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


def add_inst(num: str, Register: list, Pc: int):
    # Getting Registers A and B
    RegA = Register[int(f"0b{num[10:13]}", 2)]
    RegB = Register[int(f"0b{num[13:16]}", 2)]

    # Getting the Destination Register
    if num[29:] == "000":
        print(f"Error in Memory Location {Pc}, Cannot write to Register 0")
        return True, Pc

    # Running the Add into Destination Register
    Register[int(f"0b{num[29:]}", 2)] = RegA + RegB
    return False, Pc + 1


def nand_inst(num: str, Register: list, Pc: int):
    Output = []
    RegA = int_to_bin(Register[int(f"0b{num[10:13]}", 2)])
    RegB = int_to_bin(Register[int(f"0b{num[13:16]}", 2)])
    for index, obj in enumerate(RegA):
        if not (obj == RegB[index]):
            Output.append("1")
        else:
            Output.append("0")
    if num[29:] == "000":
        print(f"Error in Memory Location {Pc}, Cannot write to Register 0")
        return True, Pc
    Output = "".join(Output)
    Register[int(f"0b{num[29:]}", 2)] = int(f"0b{Output}", 2)
    return False, Pc + 1


def lw_inst(num: str, Register: list, Memory: list, Pc: int):
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])
    if (Address + Offset) >= len(Memory):
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        return True, Pc
    Address += Offset
    Register[int(f"0b{num[13:16]}", 2)] = Memory[Address]
    return False, Pc + 1


def sw_inst(num: str, Register: list, Memory: list, Pc: int):
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])
    if (Address + Offset) >= MAX_MEM_SIZE:
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        return True, Pc
    Address += Offset
    Memory[Address] = Register[int(f"0b{num[13:16]}", 2)]
    return False, Pc + 1


def beq_inst(num: str, Register: list, Memory: list, Pc: int):
    return False, Pc + 1


def op_code(num: str, Register: list, Memory: list, Pc: int):
    opcode = num[7:10]
    if opcode == "110":
        # Halt
        return True, Pc
    if opcode == "000":
        return add_inst(num, Register, Pc)
    if opcode == "001":
        return nand_inst(num, Register, Pc)
    if opcode == "010":
        return lw_inst(num, Register, Memory, Pc)
    if opcode == "011":
        return sw_inst(num, Register, Memory, Pc)
    if opcode == "100":
        return beq_inst(num, Register, Memory, Pc)
    if opcode == "111":
        # Noop
        return False, Pc + 1
    else:
        print(f"Error in Memory Location {Pc}, Unknown Opcode")
        return True, Pc


def main():
    # Declaring Variables
    Pc = 0
    Memory = []
    Register = []
    Halt = False

    # Loading 0 into Registers
    for i in range(NUM_REG):
        Register.append(0)
    print("Welcome to the LC3100 Simulator")
    print("This Simulator will take existing machine code and output the results to a text file 'Output'")
    print("Enter the File Name containing Machine Code")
    # Read the Text File
    f = open(input("FileName: ") + ".txt", "rt")
    line = f.readline()
    for index in range(MAX_MEM_SIZE):
        if line != '':
            Memory.append(int(line))
        else:
            Memory.append(None)
        line = f.readline()
    for i, j in enumerate(Memory):
        if j is not None:
            print(f"Memory[ {i} ] = {j}")
    while not Halt and Pc < len(Memory):
        # First We print the state
        print_state(Pc, Memory, Register)
        # We convert the integer to a binary string
        curr = int_to_bin(Memory[Pc])
        # Then we call the function by the Opcode
        Result = op_code(curr, Register, Memory, Pc)
        Halt = Result[0]
        Pc = Result[1]


if __name__ == "__main__":
    main()
