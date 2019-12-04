import sys

inp = sys.stdin.readlines()

# return list of line segments (pairs of points) representing a wire's path
def get_segments(path):
    segs = []
    orig = (0,0)
    curr = (0,0)
    for i in path:
        nxt = None
        direc = i[0]
        dist = int(i[1:])
        if direc == "R":
            nxt = (curr[0] + dist, curr[1])
        elif direc == "L":
            nxt = (curr[0] - dist, curr[1])
        elif direc == "U":
            nxt = curr[0], curr[1] + dist
        elif direc == "D":
            nxt = curr[0], curr[1] - dist
        segs.append((curr, nxt))
        curr = nxt
    return segs

def vec(s):
    return (s[1][0] - s[0][0], s[1][1] - s[0][1])


def dot(s1, s2):
    v1 = vec(s1)
    v2 = vec(s2)
    return v1[0] * v2[0] + v1[1] * v2[1]


def cross(s1, s2):
    perpendicular = dot(s1, s2) == 0
    if perpendicular:
        # vertical seg x must be in between horizontal seg x's
        # AND horizontal seg y must be in between vertical seg y's
        h = s1 if vec(s1)[1] == 0 else s2
        v = s2 if h == s1 else s1
        h = sorted(h)
        v = sorted(v)
        if h[0][0] < v[0][0] < h[1][0] and v[0][1] < h[0][1] < v[1][1]:
            # print(s1, s2)
            return (v[0][0], h[0][1])
    return None

def find_crossings(segs1, segs2):
    crossings = []
    for a in segs1:
        for b in segs2:
            x = cross(a, b)
            if x:
                crossings.append(x)
    return crossings

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def in_segment(p, s):
    s2 = sorted(s)
    return (p[0] == s2[0][0] == s2[1][0] and s2[0][1] <= p[1] <= s2[1][1]) or (p[1] == s2[0][1] == s2[1][1] and s2[0][0] <= p[0] <= s2[1][0])


def steps_to_cross(segments, p):
    # assume p is in both segments
    steps = 0
    for s in segments:
        if not in_segment(p, s):
            steps += manhattan(s[0], s[1])
            # print(s, "...", steps)
        else:
            steps += manhattan(s[0], p)
            # print(s, "...", steps)
            break
    # print("total: ", steps)
    return steps

def get_total_steps(paths, p):
    return sum(map(lambda s: steps_to_cross(s, p), paths))

# Part 1
paths = [p.strip().split(",") for p in inp]
segments = list(map(get_segments, paths))
crossings = find_crossings(segments[0], segments[1])
if (0,0) in crossings:
    crossings.remove((0,0))
print(crossings)
print(min(map(lambda p: manhattan((0,0), p), crossings)))

# Part 2

print(min(map(lambda p: get_total_steps(segments, p), crossings)))
