import sys

from fractions import Fraction
from math import atan2, pi

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

inp = sys.stdin.readlines()

grid = list(map(lambda l: list(l.strip()), inp))

# returns a tuple representing the input direction in reduced form, maintaining sign
def equivalence(dy, dx):
    g = abs(gcd(dy, dx))
    return (dy/g, dx/g)

# returns a tuple representing direction (unreduced)
def direction(a, b):
    dy = b[0] - a[0]
    dx = b[1] - a[1]
    return (dy, dx)

def distance(a, b):
    dy, dx = direction(a, b)
    return dy ** 2 + dx ** 2

# returns dict of asteroids grouped by sight line (reduced direction)
def sight_lines(a, others):
    # sort others into distinct lines of sight
    lines = {}

    for b in others:
        if a == b:
            continue

        dy, dx = direction(a, b)
        f = equivalence(dy, dx)
        if f in lines:
            lines[f].append(b)
        else:
            lines[f] = [b]

    # asteroid can only see one in each line of sight
    # print(a, lines)
    return lines

# tuples (row, col) of asteroids in grid
def asteroids(grid):
    astds = []

    for i, r in enumerate(grid):
        for j, x in enumerate(r):
            if x == "#":
                astds.append((i, j))
    return astds

def best_asteroid(astds):
    
    counts = list(map(lambda a: len(sight_lines(a, astds)), astds))
    max_count = -1
    best = None
    for i, c in enumerate(counts):
        if c > max_count:
            best = astds[i]
            max_count = c
    print("Best asteroid at {}, with {} others detected".format(best, max_count))
    return best, max_count

# return result of atan2(y / x) in range [0,2pi]
def angle(y, x):
    r = atan2(1,0) - atan2(y, x)
    if r < 0:
        r += 2 * pi
    return r

def laser_sweep(a, others):
    # get lines of sight
    lines = sight_lines(a, others)


    # sort lines increasing by atan2 relative to pi/2 (vertical up) (atan2(1,0) - atan2(y, x))
    # atan3 makes angles in 3rd and 4th quadrants a positive value (pi to 2pi)
    sorted_lines = sorted(lines.keys(), key=lambda f: angle(-f[0], f[1]))
    # print(sorted_lines)

    # sort asteroids in each line by distance from asteroid a
    for k, v in lines.items():
        lines[k] = sorted(v, key=lambda b: distance(a, b))

    # loop over lines based on keys from sorted_lines
    # destroy one asteroid in each line at a time (if there are any), and loop back around

    # tuple of number in order of destruction and asteroid location
    astds_destroyed = []

    while any(lines.values()):
        for dir in sorted_lines:
            if lines[dir]:
                astd = lines[dir].pop(0)
                astds_destroyed.append(astd)

    return astds_destroyed


# Part 1
astds = asteroids(grid)
best, max_count = best_asteroid(astds)
print(max_count)

# Part 2
destruction = laser_sweep(best, astds)
y, x = destruction[199]
print(y + 100 * x)
