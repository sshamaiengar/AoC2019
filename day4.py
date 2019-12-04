inp = input()
lohi = list(map(int, inp.split("-")))
rng = range(lohi[0], lohi[1] + 1)

def adjacent_same(n):
    def adjacent_same_str(s):
        if len(s) == 1:
            return False
        return s[0] == s[1] or adjacent_same_str(s[1:])
    return adjacent_same_str(str(n))

# at least one duplicate pair is not part of larger group of same digits
def adjacent_same_pair(n):
    s = str(n)
    last = -1
    candidate = -1
    group = 1
    for c in s:
        d = int(c)
        if d != last:
            # if end of duplicate pair then good
            if group == 2:
                return True
            candidate = d
            group = 1
        else:
            group += 1
        last = d
    # check last candidate
    if group == 2:
        return True
    return False


def monotonic_digits(n):
    s = str(n)
    last = -1
    for c in s:
        d = int(c)
        if d < last:
            return False
        last = d
    return True

def valid_pwd(n):
    return monotonic_digits(n) and adjacent_same(n)

def valid_pwd2(n):
    return monotonic_digits(n) and adjacent_same_pair(n)

# Part 1
res = list(filter(valid_pwd, rng))
print(len(res))

# Part 2
print(len(list(filter(valid_pwd2, res))))
