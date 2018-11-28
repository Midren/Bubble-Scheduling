class Graph:
    def __init__(self):
        pass

    def get_nodes(self):
        """Returns set of vertices(keys of the dict)"""
        pass

    def children(self, node):
        """Returns children of the given vertice`s"""


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
            for transfer in self.children(min_n):
                weight = cur_weight + transfer.computation + min_n.computation
                if transfer not in visited or weight < visited[transfer.get_children[-1]]:
                    visited[transfer.children[-1]] = weight
                    path[transfer.children[-1]] = min_n
        return visited, path




class Node:
    def __init__(self, ind, comp):
        self.index = ind
        self.computation = comp

    def get_children(self):
        """DOGADAySYA :=)"""
        pass