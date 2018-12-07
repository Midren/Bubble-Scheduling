from graph import Graph, Node
from visual import visualize
from task_graph_generator import get_graph
from processor_graph import *

def cpn_first_ordering(graph):
    seq = []
    seq_set = set()
    cpn = graph.get_cpn_list()

    nd = cpn[0]
    seq.append(nd)
    seq_set.add(nd)
    pos = 1

    nd = cpn[1]
    while(len(cpn) != pos):
        nd = cpn[pos]
        for node in graph.get_parents(nd):
            if node not in seq_set:
                break
        else:
            seq.append(nd)
            seq_set.add(nd)
            pos += 1
            continue

        def add_ibn(graph, seq, seq_set, node):
            for nd in graph.get_parents(node):
                if nd not in seq_set:
                    break
            else:
                seq.append(node)
                seq_set.add(node)
                return
            add_ibn(graph, seq, seq_set, nd)

        add_ibn(graph, seq, seq_set, node)

    top_sorted = graph.topological_sort()
    for node in top_sorted:
        if node not in seq_set:
            seq.append(node)

    return seq


def bsa(graph, processor_graph):
    pivot_pe = processor_graph.max_degree_node()
    processor_list = processor_graph.bfs(pivot_pe)
    print(cpn_first_ordering(graph))


if __name__ == "__main__":
    graph = get_graph("dag.txt")
    processor_graph = ProcessorsGraph({1:{2, 3}, 2:{1, 4}, 3:{1, 4}, 4:{2, 3}})
    bsa(graph, processor_graph)
