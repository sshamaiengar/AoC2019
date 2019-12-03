import sys

inp = sys.stdin.read()

code = list(map(int, inp.split(",")))
orig_code = code[:]

def run(code):
    i = 0
    opcode = code[i]
    while opcode != 99:
        in1 = code[i+1]
        in2 = code[i+2]
        out = code[i+3]

        if opcode == 1:
            code[out] = code[in1] + code[in2]
        elif opcode == 2:
            code[out] = code[in1] * code[in2]
        
        i += 4
        if i >= len(code):
            break
        opcode = code[i]
    return code

def run_with_noun_and_verb(code, noun, verb):
    code[1] = noun
    code[2] = verb
    return run(code)

# Part 1
print(run_with_noun_and_verb(code, 12, 2)[0])

# Part 2
target = 19690720

for n in range(100):
    for v in range(100):
        code = orig_code[:]
        ans = run_with_noun_and_verb(code, n, v)[0]
        if ans == target:
            print(100 * n + v)
            break


