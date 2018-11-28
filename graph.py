from collections import defaultdict

class Graph:
    def __init__(self):
        self.inc_dct = defaultdict(list)

    def __repr__(self):
        return repr(self.inc_dct.items())

    def get_nodes(self):
        """Returns set of vertices(keys of the dict)"""
        return list(self.inc_dct.keys())

    def get_children(self, node):
        """Returns children of the given vertice`s"""
        return self.inc_dct[node]

    def dijkstra(self, start):
        visited = {start: 0}
        path = dict()

        nodes = self.get_nodes()

        while nodes:
            min_n = None
            for node in nodes:
                if node in visited:
                    if min_n is None:
                        min_n = node
                    elif visited[node] < visited[min_n]:
                        min_n = node
            if min_n is None:
                break

            nodes.remove(min_n)
            cur_weight = visited[min_n]
            for edge in self.get_children(min_n):
                print(edge, edge[0], edge[1])
                weight = cur_weight + edge[0].computation + edge[1]
                print("weight = ", weight)
                if edge[0] not in visited or weight < visited[edge[0]]:
                    visited[edge[0]] = weight
                    path[edge[0]] = min_n
        return path




class Node:
    def __init__(self, ind, comp):
        self.index = ind
        self.computation = comp

    def __repr__(self):
        return "Node( " + str(self.index) +", " + str(self.computation) + " )"

    def __cmp__(self, other):
        if self.index == other.index and self.computation == other.computation:
            return True
        return False