import sys

inp = sys.stdin.readlines()

total_fuel = 0

# total including fuel cost of fuel
total_fuel2 = 0

def fuel(mass):
    return mass // 3 - 2

for i in inp:
    mass = int(i.strip())
    fl = fuel(mass)
    total_fuel += fl
    added_fl = fuel(fl)

    # add fuel costs of fuel until they are <= 0
    while added_fl > 0:
        total_fuel += added_fl
        added_fl = fuel(added_fl)

print(total_fuel)
