from graph import Node, Graph

with open("dag.txt") as f:
    graph = Graph()
    lines = f.readlines()
    end = int((lines[-1]).split()[1])
    node_lst = [None for i in range(end+1)]
    for line in lines[:-1]:
        if(not line.startswith("NODE ")):
            continue
        line = line.split()
        if line[3] == 'ROOT' or line[3] == 'COMPUTATION':
            node = Node(int(line[1]), float(line[4]))
            node_lst[node.index] = node
            if line[2] == str(end):
                graph.inc_dct[node].append((end, 0))
            if line[3] == 'ROOT':
                for ind in line[2].split(","):
                    graph.inc_dct[node].append((int(ind), 0))
        else:
            weight = float(line[4])
            node_lst[node.index] = node
            for ind in line[2].split(","):
                graph.inc_dct[node].append((int(ind), weight))
    node_lst[end] = Node(end, 0)
    for nd in graph.inc_dct.keys():
        for ind in graph.inc_dct[nd][:]:
            if isinstance(ind[0], int):
                graph.inc_dct[nd].append((node_lst[ind[0]], ind[1]))
                graph.inc_dct[nd].remove(ind)
    a = list(graph.inc_dct.keys())[0]
    c, b = graph.dijkstra(a)