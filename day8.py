from collections import Counter

inp = input()

W = 25
H = 6

min_zeros_layer = None
min_zeros = float('inf')
ans = 0
for i in range(0,len(inp),W*H):
    counts = Counter(inp[i:i+W*H])
    if counts['0'] < min_zeros:
        min_zeros = counts['0']
        min_zeros_layer = i//(W*H)
        ans = counts['1'] * counts['2']

def reshape_layer(layer):
    grid = []
    for r in range(H):
        row = layer[r*W:r*W+W]
        grid.append(row)
    return grid

# get top visible pixels from input
def decode(inp):
    layers = []
    for i in range(0, len(inp), W*H):
        layers.append(reshape_layer(inp[i:i + W*H]))
    pixels = [[0 for i in range(W)] for j in range(H)]
    for r in range(H):
        for c in range(W):
            for layer in layers:
                if int(layer[r][c]) < 2:
                    pixels[r][c] = layer[r][c]
                    break
    return pixels

def show(pixels):
    colors = {"0": "░", "1": "█"}
    for r in pixels:
        print("".join(map(lambda p: colors[p], r)))

# Part 1
print(ans)

# Part 2
show(decode(inp))
