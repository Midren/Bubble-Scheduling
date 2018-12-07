from collections import defaultdict


class Graph:
    def __init__(self):
        # dict with indicidence lists
        self.inc_dct = defaultdict(list)

    def __repr__(self):
        return repr(self.inc_dct.items())

    def get_nodes(self):
        """Returns set of vertices(keys of the dict)"""
        return list(self.inc_dct.keys())

    def get_children(self, node):
        """Returns children of the given vertice`s"""
        return self.inc_dct[node]

    def get_children_nodes(self, node):
        """Returns children of the given vertice`s"""
        return list(map(lambda x: x[0], self.get_children(node)))

    def get_parents(self, node):
        parents = []
        for nd in self.get_nodes():
            if node in self.get_children_nodes(nd):
                parents.append(nd)
        return parents

    def get_edge(self, nd1, nd2):
        for nd in self.inc_dct[nd1]:
            if nd[0] == nd2:
                return nd[1]

    def get_graph_algo(self, proc_a):
        n_vertex = len(self.inc_dct.keys())
        n_edges = sum([len(i) for i in self.inc_dct.values()])
        inc_lst = list()
        for k, v in self.inc_dct.items():
            for inc_v in v:
                inc_lst.append((k.index, inc_v[0].index))

        with open('dag_v2.txt', 'w') as f:
            f.write(str(n_vertex) + ' ')
            f.write(str(n_edges) + ' ')
            f.write(str(proc_a))
            f.write('\n')
            for i in inc_lst:
                f.write(str(i[0]) + ' ')
                f.write(str(i[1]) + ' ')
                f.write('\n')

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
                weight = cur_weight + edge[0].computation + edge[1]
                if edge[0] not in visited or weight < visited[edge[0]]:
                    visited[edge[0]] = weight
                    path[edge[0]] = min_n
        return path

    def get_cpn_list(self):
        fst, lst = self.get_nodes()[0], self.get_nodes()[1]
        path = self.dijkstra(fst)
        last_item = self.get_nodes()[-1]
        cpn_list = [last_item]
        while last_item != fst:
            last_item = path[last_item]
            cpn_list.append(last_item)
        return cpn_list[::-1]

    def get_ibn_list(self):
        cpn = self.get_cpn_list()
        ibn = []

        def check_ibn(graph, node, cpn):
            for nd in graph.get_children_nodes(node):
                if nd in cpn:
                    return True
                if check_ibn(graph, nd, cpn):
                    return True
            return False

        for node in self.get_nodes():
            if node not in cpn and check_ibn(self, node, cpn):
                ibn.append(node)

        return ibn

    def get_obn_set(self):
        nodes = set(self.get_nodes())
        nodes -= set(self.get_cpn_list())
        nodes -= set(self.get_ibn_list())
        return list(nodes)


    def topological_sort(self):
        visited = defaultdict(bool)
        nodes = []

        def topological_sort_util(self, v, visited, nodes):
            visited[v] = True

            for i in self.get_children_nodes(v):
                if visited[i] == False:
                    topological_sort_util(self, i, visited, nodes)

            nodes.insert(0, v)

        for i in self.get_nodes():
            if visited[i] == False:
                topological_sort_util(self, i, visited, nodes)

        return nodes


class Node:
    def __init__(self, ind, comp, trans):
        self.index = ind
        self.computation = comp
        self.tranfering = trans

    def __repr__(self):
        return "Node( " + str(self.index) + ", " + str(self.computation) + ', ' + str(self.tranfering) + " )"

    def __cmp__(self, other):
        if self.index == other.index and self.computation == other.computation:
            return True
        return False
