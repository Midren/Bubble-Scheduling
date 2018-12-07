from collections import defaultdict

class ProcessorsGraph:

    def __init__(self, my_dict):
        self.inc_dct = my_dict
    
    def bfs(self, start):
        visited, queue = set(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex is not visited:
                visited.add(vertex)
                queue.extend(self.inc_dct[vertex] - visited)
        return visited

class Processor:
    def __init__(self):
        self.tasks = []


a = ProcessorsGraph({1:{2, 3}, 2:{1, 4}, 3:{1, 4}, 4:{2, 3}})
print(a.bfs(1))
