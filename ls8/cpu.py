"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 244

    # ram_read() should accept the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    #ram_write()` should accept a value to write, and the address to write it to.
    def ram_write(self, value, address):
        self.ram[address] = value



    def load(self, argv):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  130
        #     0b00000000, #           0
        #     0b00001000, #           8
        #     0b01000111, # PRN R0    71
        #     0b00000000, #           0
        #     0b00000001, # HLT       1
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        num = line.split('#')[0].strip()
                        self.ram[address] = int(num, 2)
                        address += 1
                        # print(self.ram)
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not Found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # It needs to read the memory address that’s stored in register PC, and store that result in IR, the Instruction Register. This can just be a local variable in run().
        running = True
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        while running:
            # print('running!')
            # self.trace()
            IR = self.ram[self.pc]
            # running = False
            # return IR
            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == HLT:
                running = False

            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PRN:
                operand_a = self.ram[self.pc + 1]
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == PUSH:
                self.sp = (self.sp % 257) - 1
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2

            elif IR == POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = (self.sp % 257) + 1
                self.pc += 2
        # pass
