import itertools

inp = input()

code = list(map(int, inp.split(",")))
orig_code = code[:]

def run(code, inputs=[], pausing=False, start_ip=0):
    i = start_ip
    opcode = code[i] % 100
    inc = 0
    input_i = 0
    outputs = []
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
                # accept input from parameters
                if inputs and input_i < len(inputs):
                        code[val] = int(inputs[input_i])
                        input_i += 1
                else:
                    code[val] = int(input())
            else:
                # redirect outputs to return list
                # print("out: ", val)
                outputs.append(val)
                if pausing:
                    if code[i+inc] == 99:
                        return code, outputs, -1
                    return code, outputs, i+inc

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
    return code, outputs, -1

def run_chain(code, phase_levels):
    _, out, _ = run(code[:], [phase_levels[0],0])
    _, out, _ = run(code[:], [phase_levels[1],out[0]])
    _, out, _ = run(code[:], [phase_levels[2], out[0]])
    _, out, _ = run(code[:], [phase_levels[3],out[0]])
    _, out, _ = run(code[:], [phase_levels[4],out[0]])
    return out[0]

def find_max_output(code, run_func, phase_range=range(5)):
    perms = list(itertools.permutations(phase_range))
    return max(map(lambda p: run_func(code[:], p), perms))

def run_chain_continuous(code, phase_levels):
    codes = [code[:] for i in range(len(phase_levels))]
    ips = [0] * len(phase_levels)
    out = None
    last_E_out = None
    cycle = 0
    halt = False
    while not halt:
        for i in range(len(codes)):
            inpi = [phase_levels[i], 0 if i == 0 else out[0]] if cycle == 0 else [out[0]]
            codes[i], out, ips[i] = run(codes[i], inpi, pausing=True, start_ip=ips[i])
            if ips[i] == -1:
                halt = True

        if out:
            last_E_out = out
            # print(last_E_out)
        cycle += 1
    return last_E_out[0]


# Part 1
print(find_max_output(code, run_chain))

# Part 2
print(find_max_output(code, run_chain_continuous, phase_range=range(5,10)))
