from collections import defaultdict

class Node:
    def __init__(self, ind, comp):
        self.index = ind
        self.computation = comp

    def __repr__(self):
        return "Node( " + str(self.index) +", " + str(self.computation) + " )"

class Graph:
    def __init__(self):
        self.inc_dct = defaultdict(list)

    def __repr__(self):
        return repr(self.inc_dct.items())
