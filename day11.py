import sys
from enum import IntEnum

inp = input()

code = list(map(int, inp.split(",")))
orig_code = code[:]

REL_BASE = 0

class ParamMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

def get_value(param, mode, code):
    pos = None
    if mode == ParamMode.POSITION:
        pos = param
    elif mode == ParamMode.RELATIVE:
        pos = param + REL_BASE
    val = param if pos == None else code[pos]
    # print("val {} = param {}, pos {}, with mode {} and REL_BASE {}".format(val, param, pos, mode, REL_BASE))
    return val

def run(code):
    global REL_BASE

    # add additional memory beyond code
    code += [0] * (len(code) * 10)

    i = 0
    opcode = code[i] % 100
    inc = 0

    input_val = None

    while opcode != 99:
        if opcode in [1,2,7,8]:
            inc = 4
        elif opcode in [3,4,9]:
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
            val1 = get_value(instr[1], param_modes[0], code)
            val2 = get_value(instr[2], param_modes[1], code)
            pos_out = instr[3] + (REL_BASE if param_modes[2] == ParamMode.RELATIVE else 0)

            if opcode == 1:
                code[pos_out] = val1 + val2
            else:
                code[pos_out] = val1 * val2

            # print(val1, val2, "->", pos_out)

        elif opcode == 3 or opcode == 4:
            # writing to the parameter address given (plus REL_BASE)
            # not to the address of the vlaue of the param
            val = get_value(instr[1], param_modes[0], code)

            if opcode == 3:
                val = instr[1] + (REL_BASE if param_modes[0] == ParamMode.RELATIVE else 0)
                # print('IN YIELD')
                input_val = yield
                # print("in: ", input_val)
                code[val] = int(input_val)
            else:
                # print('OUT YIELD', val)
                yield val
                # print("out: ", val)

        elif opcode in [5,6]:
            val1 = get_value(instr[1], param_modes[0], code)
            jump_addr = get_value(instr[2], param_modes[1], code)

            if opcode == 5:
                if val1 != 0:
                    i = jump_addr
                    inc = 0
            elif opcode == 6:
                if val1 == 0:
                    i = jump_addr
                    inc = 0

        elif opcode in [7,8]:
            pos3 = instr[3] + (REL_BASE if param_modes[2] == ParamMode.RELATIVE else 0)
            val1 = get_value(instr[1], param_modes[0], code)
            val2 = get_value(instr[2], param_modes[1], code)

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

        elif opcode == 9:
            val = get_value(instr[1], param_modes[0], code)
            REL_BASE += val

        i += inc
        if i >= len(code):
            break
        opcode = code[i] % 100

# based on inputs and outputs of paint program,
# track which panels have been painted
def track_painting(start_color=0):

    painted_tiles = {}
    curr = (0,0)
    curr_color = None
    direc = 0
    moves = [(0,1), (1,0), (0,-1), (-1,0)] # (x, y)

    r = run(code) # generator
    # next(r)
    while True:
        try:
            # curr_color = painted_tiles.get(curr, 0)
            # print("send: ", curr_color)
            color_out = r.send(curr_color) # send and yield next value
        except StopIteration:
            break

        if color_out == None:
            curr_color = painted_tiles.get(curr, start_color)
            continue
        elif color_out in [0,1]:
            # color_out = next(r)
            painted_tiles[curr] = color_out
            # print("color_out: ", color_out)

        dir_out = next(r)
        # print("dir out: ", dir_out)

        if dir_out == 0:
            direc = (direc - 1) % 4
        elif dir_out == 1:
            direc = (direc + 1) % 4
        dx, dy = moves[direc]
        x, y = curr
        curr = x + dx, y + dy
        # print("curr: ", curr)
    # count tiles painted over
    return painted_tiles

def show_painting(painted_tiles):
    tiles = sorted(painted_tiles.keys())
    # print(tiles)
    max_x = tiles[-1][0]
    min_x = tiles[0][0]
    
    sorted_y_tiles = sorted(tiles, key=lambda t: t[1])
    max_y = tiles[-1][1]
    min_y = tiles[0][1]
    
    for i in range(max_y + 1, min_y - 2, -1): # not sure why need to adjust the range
        for j in range(min_x, max_x + 1):
            tile = (j, i)
            color = painted_tiles.get(tile, 0)
            if color == 1:
                print("█", end='')
            else:
                print('░', end='')
        print()

# Part 1
painted = track_painting(0)
print(len(painted))

# Part 2
painted = track_painting(1)
show_painting(painted)
