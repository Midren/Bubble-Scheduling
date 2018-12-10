from graph import Graph, Node
from visual import visualize
from task_graph_generator import get_graph
from processor_graph import *

from pprint import pprint

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
    tasks_node = cpn_first_ordering(graph)
    tasks = list(map(Task, tasks_node))
    tasks = Tasks(tasks, tasks_node, graph, pivot_pe)

    while processor_list:
        pivot_pe = processor_list[0]
        for task in tasks.tasks[pivot_pe][:]:
            if task.st >= task.dat or ((tasks.vip(task) is not None) and (tasks.vip(task).proc != pivot_pe)):

                for proc in processor_list[1:]:
                    if tasks.st_if_migrate(task, proc) < task.st:
                        tasks.migrate(task, proc)
                        break
            else:
                for proc in processor_list[1:]:
                    a = tasks.st_if_migrate(task, proc) >= task.st
                    b = (tasks.vip(task) is not None and tasks.vip(task).proc == pivot_pe)
                    if a and b:
                        tasks.migrate(task, proc)
                        break
        processor_list = processor_list[1:]
    return tasks

if __name__ == "__main__":
    graph = get_graph("example.txt")
    processor_graph = ProcessorsGraph({1:[2, 3, 4], 2:[1, 3, 4], 3:[1, 2, 4], 4:[1, 2, 3]})

    tasks = bsa(graph, processor_graph)
    work_time = max([tasks.tasks[proc][-1].fn for proc in tasks.tasks])
    print("Work time using parallel architecture:", work_time)

    processor_list = processor_graph.bfs(1)
    tasks_node = cpn_first_ordering(graph)
    tasks = list(map(Task, tasks_node))
    tasks = Tasks(tasks, tasks_node, graph, 1)
    work_time = max([tasks.tasks[proc][-1].fn for proc in tasks.tasks])
    print("Work time using one processor:", work_time)
