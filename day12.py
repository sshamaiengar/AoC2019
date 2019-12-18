import sys
from itertools import combinations
import re
from math import gcd
from functools import reduce

inp = sys.stdin.readlines()

class Vector:
    def __init__(self, x, y, z):
        self.val = [x, y, z]

    def __str__(self):
        return str(tuple(self.val))

    def __getitem__(self, i):
        return self.val[i]

    def __setitem__(self, i, v):
        self.val[i] = v

class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def __str__(self):
        return "Moon at position {}, velocity {}".format(self.position, tuple(self.velocity))

    def kinetic_energy(self):
        return sum(map(abs, self.velocity))

    def potential_energy(self):
        return sum(map(abs, self.position))

    def total_energy(self):
        return self.kinetic_energy() * self.potential_energy()

    def vals(self):
        return (tuple(self.position), tuple(self.velocity))

def apply_gravity(moons):
    for a, b in combinations(moons, 2):
        for i, d in enumerate(a.position.val):

            if a.position[i] < b.position[i]:
                a.velocity[i] += 1
                b.velocity[i] -= 1
            elif a.position[i] > b.position[i]:
                a.velocity[i] -= 1
                b.velocity[i] += 1
    return moons

def apply_velocity(moons):
    for m in moons:
        for i, d in enumerate(m.velocity):
            m.position[i] += d
    return moons

def time_step(moons):
    apply_gravity(moons)
    apply_velocity(moons)
    return moons

def total_energy(moons):
    return sum(map(lambda m: m.total_energy(), moons))

def moons(inp_lines):
    moons = []
    for line in inp_lines:
        res = re.search('x=([\-0-9]+), y=([\-0-9]+), z=([\-0-9]+)', line)
        x = int(res.group(1))
        y = int(res.group(2))
        z = int(res.group(3))
        moon = Moon(Vector(x, y, z))
        moons.append(moon)
    return moons

def lcm(*nums):
    return reduce(lambda a, b: a * b // gcd(a, b), nums)

def get_moon_axis_states(moons):
    velocities = [m.velocity for m in moons]
    positions = [m.position for m in moons]
    states = [tuple([(velocities[j][i], positions[j][i]) for j in range(len(moons))]) for i in range(3)]
    return tuple(states)

# Part 1
moons = moons(inp)

# find period for each axis independently
axis_states = [{get_moon_axis_states(moons)[i]: 0} for i in range(3)]
periods = [float('inf')] * 3
i = 0
while any(map(lambda x: type(x) == type(1.0), periods)) or i < 1000:
    moons = time_step(moons)

    if i == 999:
        print("Total energy: {}".format(total_energy(moons)))

    # check if each axis state has been seen before
    # if so, update that period
    ax_state = get_moon_axis_states(moons)
    for j in range(3):
        if ax_state[j] in axis_states[j]:
            periods[j] = min(periods[j], i + 1 - axis_states[j][ax_state[j]])
        else:
            axis_states[j][ax_state[j]] = i

    i += 1

# Part 2
# find period for each axis
# get lcm of all periods as overall period
# print(periods)
print(lcm(*periods))
