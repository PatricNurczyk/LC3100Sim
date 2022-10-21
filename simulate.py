# Const Variables
MAX_MEM_SIZE = 65536
NUM_REG = 8


def print_state(pc: int, mem: list, reg: list, output):
    print("\n@@@\nstate:")
    output.write("\n@@@\nstate:\n")
    print(f"\tpc {pc}")
    output.write(f"\tpc {pc}\n")
    print("\tmemory:")
    output.write("\tmemory:\n")
    for i, j in enumerate(mem):
        if j is not None:
            print(f"\t\tmem[ {i} ] {j}")
            output.write(f"\t\tmem[ {i} ] {j}\n")
    print("\tregisters:")
    output.write("\tregisters:\n")
    for i, j in enumerate(reg):
        print(f"\t\treg[ {i} ] {j}")
        output.write(f"\t\treg[ {i} ] {j}\n")
    print("end state\n")
    output.write("end state\n")


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


def add_inst(num: str, Register: list, Pc: int, output):
    # Getting Registers A and B
    RegA = Register[int(f"0b{num[10:13]}", 2)]
    RegB = Register[int(f"0b{num[13:16]}", 2)]

    # Getting the Destination Register
    if num[29:] == "000":
        print(f"Error in Memory Location {Pc}, Cannot write to Register 0")
        output.write(f"Error in Memory Location {Pc}, Cannot write to Register 0\n")
        return True, Pc + 1

    # Running the Add into Destination Register
    Register[int(f"0b{num[29:]}", 2)] = RegA + RegB
    return False, Pc + 1


def nand_inst(num: str, Register: list, Pc: int, output):
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
        output.write(f"Error in Memory Location {Pc}, Cannot write to Register 0\n")
        return True, Pc + 1
    Output = "".join(Output)
    Register[int(f"0b{num[29:]}", 2)] = int(f"0b{Output}", 2)
    return False, Pc + 1


def lw_inst(num: str, Register: list, Memory: list, Pc: int, output):
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])
    if (Address + Offset) >= len(Memory):
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        output.write(f"Error in Memory Location {Pc}, Outside Memory Bounds\n")
        return True, Pc + 1
    Address += Offset
    Register[int(f"0b{num[13:16]}", 2)] = Memory[Address]
    return False, Pc + 1


def sw_inst(num: str, Register: list, Memory: list, Pc: int, output):
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])
    if (Address + Offset) >= MAX_MEM_SIZE:
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        output.write(f"Error in Memory Location {Pc}, Outside Memory Bounds\n")
        return True, Pc + 1
    Address += Offset
    Memory[Address] = Register[int(f"0b{num[13:16]}", 2)]
    return False, Pc + 1


def beq_inst(num: str, Register: list, Pc: int, output):
    Offset = two_comp(num[16:])
    if (Pc + Offset) >= MAX_MEM_SIZE:
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        output.write(f"Error in Memory Location {Pc}, Outside Memory Bounds\n")
        return True, Pc + 1
    RegA = Register[int(f"0b{num[10:13]}", 2)]
    RegB = Register[int(f"0b{num[13:16]}", 2)]
    if RegA == RegB:
        return False, Pc + 1 + Offset
    return False, Pc + 1


def op_code(num: str, Register: list, Memory: list, Pc: int, output):
    opcode = num[7:10]
    if opcode == "110":
        # Halt
        return True, Pc + 1
    if opcode == "000":
        return add_inst(num, Register, Pc, output)
    if opcode == "001":
        return nand_inst(num, Register, Pc, output)
    if opcode == "010":
        return lw_inst(num, Register, Memory, Pc, output)
    if opcode == "011":
        return sw_inst(num, Register, Memory, Pc, output)
    if opcode == "100":
        return beq_inst(num, Register, Pc, output)
    if opcode == "111":
        # Noop
        return False, Pc + 1
    else:
        print(f"Error in Memory Location {Pc}, Unknown Opcode")
        output.write(f"Error in Memory Location {Pc}, Unknown Opcode\n")
        return True, Pc + 1


def main():
    # Declaring Variables
    Pc = 0
    Memory = []
    Register = []
    Halt = False
    InstCounter = 0
    # Loading 0 into Registers
    for i in range(NUM_REG):
        Register.append(0)
    print("Welcome to the LC3100 Simulator")
    print("This Simulator will take existing machine code and output the results to a text file 'Output'")
    print("Enter the File Name containing Machine Code")
    # Read the Text File
    f = open(input("FileName: ") + ".txt", "rt")
    output = open("output.txt", "w")
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
            output.write(f"Memory[ {i} ] = {j}\n")
    while not Halt and Pc < len(Memory):
        # First We print the state
        print_state(Pc, Memory, Register, output)
        # We convert the integer to a binary string
        curr = int_to_bin(Memory[Pc])
        # Then we call the function by the Opcode
        Result = op_code(curr, Register, Memory, Pc, output)
        Halt = Result[0]
        Pc = Result[1]
        InstCounter += 1
    print("machine halted")
    output.write("machine halted\n")
    print(f"total of {InstCounter} instructions executed")
    output.write(f"total of {InstCounter} instructions executed\n")
    print("final state of machine:")
    output.write("final state of machine:\n")
    print_state(Pc, Memory, Register, output)
    input("Press Enter to Close the Simulator")


if __name__ == "__main__":
    main()
