from collections import defaultdict

class Graph:
    def __init__(self):
        # dict with indicidence lists
        self.inc_dct = defaultdict(list)

    def __repr__(self):
        return repr(self.inc_dct.items())

    def get_nodes(self):
        """Returns set of vertices(keys of the dict)"""
        pass

    def children(self, node):
        """Returns children of the given vertice`s"""

    def get_parents(self, node):
        # Test
        parents = []
        for nd in self.get_nodes():
            if node in self.get_children(nd):
                parents.append(nd)
        return parents


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

    def find_cpn_list(self):
        # Test
        fst, lst = None, None
        for i in self.get_nodes():
            if i.index == 0:
                fst = i
            elif len(self.inc_dct[i]) == 0:
                lst = i
            if fst is not None and lst is not None:
                break
        # This don't work now -- Yura fix pls
        cp = self.dijkstra(self, fst)[lst]
        return cp

    def find_ibn_list(self):
        # Test
        cpn = self.find_cpn_list()
        ibn = []
        for node in self.get_nodes():
            children = self.get_children(node)
            for nd in cpn:
                if nd in children:
                    ibn.append(node)
            else:
                continue
            break
        return ibn

    def topological_sort(self):
        # Test
        visited = defaultdict(bool)
        nodes = []

        def topological_sort_util(self, v, visited, nodes):
            visited[v] = True

            for i in self.get_children(v):
                if visited[i] == False:
                    topological_sort_util(self, i, visited, nodes)

            nodes.insert(0, v)

        for i in self.get_nodes():
            if visited[i] == False:
                topological_sort_util(self, i, visited, nodes)

        return nodes


class Node:
    def __init__(self, ind, comp):
        self.index = ind
        self.computation = comp

    def __repr__(self):
        return "Node( " + str(self.index) +", " + str(self.computation) + " )"

    def get_children(self):
        """DOGADAySYA :=)"""
        pass
