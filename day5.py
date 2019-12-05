import sys

inp = input()

code = list(map(int, inp.split(",")))
orig_code = code[:]

def run(code):
    i = 0
    opcode = code[i] % 100
    inc = 0
    while opcode != 99:
        if opcode in [1,2,7,8]:
            inc = 4
        elif opcode in [3,4]:
            inc = 2
        elif opcode in [5,6]:
            inc = 3 # may be ignored by jump

        instr = code[i:i+inc]
        # print(instr)

        # parse param modes
        modes_num = code[i] // 100
        param_modes = [0,0,0]
        for p in range(3):
            param_modes[p] = modes_num % 10
            modes_num //= 10
        # print("op: ", opcode)
        # print("params: ", param_modes)

        if opcode == 1 or opcode == 2:
            pos1 = instr[1] if param_modes[0] == 0 else None
            pos2 = instr[2] if param_modes[1] == 0 else None
            val1 = instr[1] if pos1 == None else code[pos1]
            val2 = instr[2] if pos2 == None else code[pos2]
            pos_out = instr[3]

            if opcode == 1:
                code[pos_out] = val1 + val2
            else:
                code[pos_out] = val1 * val2

            # print(val1, val2, "->", pos_out)

        elif opcode == 3 or opcode == 4:
            pos = instr[1] if param_modes[0] == 0 else None
            val = instr[1] if pos == None else code[pos]

            if opcode == 3:
                val = pos
                code[val] = int(input())
            else:
                print(val)

        elif opcode in [5,6]:
            pos1 = instr[1] if param_modes[0] == 0 else None
            pos2 = instr[2] if param_modes[1] == 0 else None
            val1 = instr[1] if pos1 == None else code[pos1]
            jump_addr = instr[2] if pos2 == None else code[pos2]

            if opcode == 5:
                if val1 != 0:
                    i = jump_addr
                    inc = 0
            elif opcode == 6:
                if val1 == 0:
                    i = jump_addr
                    inc = 0

        elif opcode in [7,8]:
            pos1 = instr[1] if param_modes[0] == 0 else None
            pos2 = instr[2] if param_modes[1] == 0 else None
            pos3 = instr[3] # no immediate mode for writing to
            val1 = instr[1] if pos1 == None else code[pos1]
            val2 = instr[2] if pos2 == None else code[pos2]

            if opcode == 7:
                if val1 < val2:
                    code[pos3] = 1
                else:
                    code[pos3] = 0
            elif opcode == 8:
                if val1 == val2:
                    code[pos3] = 1
                else:
                    code[pos3] = 0

        i += inc
        if i >= len(code):
            break
        opcode = code[i] % 100
    return code

run(code)
