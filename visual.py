from graphviz import Digraph
from task_graph_generator import get_graph, generate_graph_txt
import sys, os

def visualize(graph):
    dot = Digraph(comment="DAG")
    for k, v in graph.inc_dct.items():
        dot.node(str(k.index), str(k.computation//100000000))
        for incedent in v:
            dot.node(str(incedent[0].index), label=str(incedent[1]))
            dot.edge(str(k.index), str(incedent[0].index),
                     label=str(incedent[1]//100000))
    dot.render('DAG.gv', view=True)


if __name__ == "__main__":
    graph = generate_graph_txt()
    visualize(graph)
