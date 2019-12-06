import sys

inp = sys.stdin.readlines()

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.dist = 0
        self.parent = parent
        self.children = []

def build_tree(inp):
    links = list(map(lambda s: s.strip().split(")"), inp))
    nodes = {}
    for l in links:
        parent, child = l
        if parent not in nodes:
            nodes[parent] = Node(parent)
        if child not in nodes:
            nodes[child] = Node(child, nodes[parent])
        nodes[child].parent = nodes[parent]
        nodes[parent].children.append(nodes[child])
    return nodes

# bfs to sum path lengths to all nodes
def bfs(root):
    q = [root]
    sum = 0
    while q:
        curr = q.pop()
        for c in curr.children:
            q.insert(0,c)
            c.dist = c.parent.dist + 1
            sum += c.dist
    return sum

# list of ancestors from closest to furthest
def get_ancestors(child):
    ancs = []
    curr = child.parent
    while curr != None:
        ancs.append(curr)
        curr = curr.parent
    return ancs

def lowest_common_ancestor(a, b):
    a_ancs = get_ancestors(a)[::-1]
    b_ancs = get_ancestors(b)[::-1]
    i = 0
    while a_ancs[i] == b_ancs[i]:
        i += 1
    return a_ancs[i-1]

def minimum_orbital_transfer(you, santa):
    lca = lowest_common_ancestor(you, santa)
    return (you.dist - lca.dist - 1) + (santa.dist - lca.dist - 1)


# Part 1
nodes = build_tree(inp)
root = nodes['COM']
print(bfs(root))

# Part 2
you = nodes['YOU']
santa = nodes['SAN']
print(minimum_orbital_transfer(you, santa))
