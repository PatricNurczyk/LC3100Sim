# Const Variables
MAX_MEM_SIZE = 65536
NUM_REG = 8

# Prints out the current state of the Machine
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


# This will Convert a Integer Number to a 32-Bit Binary String
def int_to_bin(input):

    # we get the binary string then keep everything except the 0b
    input = bin(input)[2:]

    # Extends the string by adding 0s until it is 32-Bits 
    while len(input) != 32:
        input = "0" + input
    return input


# This will take a Binary String and convert it into a 2s-Compliment Integer
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

# Preforms the Add Instruction, (DestReg = RegA + RegB)
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

# Preforms the Nand Instruction, (DestReg = RegA NAND RegB)
def nand_inst(num: str, Register: list, Pc: int, output):
    # Creates a output list
    Output = []

    # Loads RegA and RegB
    RegA = int_to_bin(Register[int(f"0b{num[10:13]}", 2)])
    RegB = int_to_bin(Register[int(f"0b{num[13:16]}", 2)])

    # If RegA and RegB are both 1 then NAND of 1 and 1 is 0
    for index, obj in enumerate(RegA):
        if obj == "1" and RegB[index] == "1":
            Output.append("0")
        else:
            Output.append("1")
    if num[29:] == "000":
        print(f"Error in Memory Location {Pc}, Cannot write to Register 0")
        output.write(f"Error in Memory Location {Pc}, Cannot write to Register 0\n")
        return True, Pc + 1

    # Creates a binary string from the list
    Output = "".join(Output)

    # Returns the 2s-Compliment Value of the Binary Number
    Register[int(f"0b{num[29:]}", 2)] = two_comp(Output)
    return False, Pc + 1

# Preforms the lw Instruction, (DestReg = Mem[Address + Offset])
def lw_inst(num: str, Register: list, Memory: list, Pc: int, output):

    # Loads the Address and gets the offset
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])
    if (Address + Offset) >= len(Memory):
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        output.write(f"Error in Memory Location {Pc}, Outside Memory Bounds\n")
        return True, Pc + 1

    # Adds the Address and the Offset
    Address += Offset

    # Loads the word into the Destination Register
    Register[int(f"0b{num[13:16]}", 2)] = Memory[Address]
    return False, Pc + 1

# Preforms the sw function, (Mem[Address + Offset] = RegB)
def sw_inst(num: str, Register: list, Memory: list, Pc: int, output):
    # Loads the Address and the offset
    Address = Register[int(f"0b{num[10:13]}", 2)]
    Offset = two_comp(num[16:])
    if (Address + Offset) >= MAX_MEM_SIZE:
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        output.write(f"Error in Memory Location {Pc}, Outside Memory Bounds\n")
        return True, Pc + 1

    # Adds the offset to the Address
    Address += Offset

    #Stores the contents of RegB into the address in Memory
    Memory[Address] = Register[int(f"0b{num[13:16]}", 2)]
    return False, Pc + 1

# Preforms the beq instruction, (If RegA == RegB then Pc = Pc + 1 + Offset)
def beq_inst(num: str, Register: list, Pc: int, output):
    # Loads the Offset
    Offset = two_comp(num[16:])
    if (Pc + 1 + Offset) >= MAX_MEM_SIZE:
        print(f"Error in Memory Location {Pc}, Outside Memory Bounds")
        output.write(f"Error in Memory Location {Pc}, Outside Memory Bounds\n")
        return True, Pc + 1

    # Loads the Registers
    RegA = Register[int(f"0b{num[10:13]}", 2)]
    RegB = Register[int(f"0b{num[13:16]}", 2)]

    # Checks for Equality and will branch if True
    if RegA == RegB:
        return False, Pc + 1 + Offset
    return False, Pc + 1

# This Function will scan for the the opcode, then run the corresponding function
# Returns whether or not to halt the program as well as the Program Counter
def op_code(num: str, Register: list, Memory: list, Pc: int, output):
    opcode = num[7:10]
    # Halt
    if opcode == "110":
        return True, Pc + 1
    # Add
    if opcode == "000":
        return add_inst(num, Register, Pc, output)
    # Nand
    if opcode == "001":
        return nand_inst(num, Register, Pc, output)
    # Load Word
    if opcode == "010":
        return lw_inst(num, Register, Memory, Pc, output) 
    # Store Word
    if opcode == "011":
        return sw_inst(num, Register, Memory, Pc, output)
    # Branch
    if opcode == "100":
        return beq_inst(num, Register, Pc, output)
    # Noop
    if opcode == "111":
        return False, Pc + 1
    #Unknown Function
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
    print("Enter the File Name containing Machine Code (Ex: 'Test1.txt') ")
    # Read the Text File

    while True:
        try:
            f = open(input("FileName: "), "rt")
            break
        except:
            print("File not found...Please enter a different file name")
    output = open("output.txt", "w")
    line = f.readline()

    #Loading Memory
    for index in range(MAX_MEM_SIZE):
        if line != '':
            Memory.append(int(line))
        else:
            Memory.append(None)
        line = f.readline()

    #Prints out Memory
    for i, j in enumerate(Memory):
        if j is not None:
            print(f"Memory[ {i} ] = {j}")
            output.write(f"Memory[ {i} ] = {j}\n")
    while not Halt and Pc < len(Memory):
        if Memory[Pc] is None:
            print(f"No Data in Mem {Pc}")
            break
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