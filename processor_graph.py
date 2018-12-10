from collections import defaultdict
from graph import Node

from pprint import pprint

class ProcessorsGraph:

    def __init__(self, my_dict):
        self.inc_dct = my_dict

    def bfs(self, start):
        visited, queue = list(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.append(vertex)
                queue.extend([element for element in self.inc_dct[vertex] if element not in visited])
        return visited

    def max_degree_node(self):
        node = None
        for i in self.inc_dct.keys():
            if node is None:
                node = i
            elif len(self.inc_dct[i]) > len(self.inc_dct[node]):
                node = i
        return i

class Tasks:
    def __init__(self, tasks, tasks_node, graph, pivot_pe):
        self.graph = graph
        self.comm_dict = dict()
        tasks[0].proc = pivot_pe
        for num, task in enumerate(tasks[1:]):
            task.proc = pivot_pe

            for t in graph.get_parents(tasks_node[num + 1]):
                for tsk in tasks:
                    if tsk.index == t.index:
                        task.parents.append(tsk)

            task.dat = tasks[1 +num-1].fn
            task.st = tasks[1 + num-1].fn
            task.fn = task.st + task.computation
        self.tasks = defaultdict(list)
        self.tasks[pivot_pe] = tasks
        self.links = defaultdict(list)
        for nd in graph.get_nodes():
            for node in graph.get_children_nodes(nd):
                self.comm_dict[(nd.index, node.index)] = graph.get_edge(nd, node)


    def st_if_migrate_comp(self, task, proc):
        if not self.tasks[proc]:
            return 0
        for num, t in enumerate(self.tasks[proc][1:]):
            new_st = max(self.tasks[proc][1 + num-1].fn, task.dat)
            if (t.st - new_st >= task.computation): # and new_st < task.st:
                return new_st
        return self.tasks[proc][len(self.tasks[proc])-1].fn

    def st_if_migrate_comm(self, message, proc):
        if not self.links[message.parent.proc]:
            return 0
        for num, m in enumerate(self.links[message.parent.proc][1:]):
            new_st = max(self.links[message.parent.proc][1 + num-1].fn, message.parent.fn)
            if (m.st - new_st >= message.communication):
                return new_st
        return self.links[message.parent.proc][len(self.links[message.parent.proc])-1].fn

    def st_if_migrate(self, task, proc):
        new_st_2 = 0
        if task.parents:
            parent = self.vip(task)
            message = Message(parent, task, self.comm_dict[(parent.index, task.index)])
            new_st_2 = self.st_if_migrate_comm(message, proc)
        new_st_1 = self.st_if_migrate_comp(task, proc)
        return max(new_st_1, new_st_2)

    def migrate(self, task, proc):
        pivot_pe = task.proc
        if not self.tasks[proc]:
                self.tasks[proc].append(task)
                self.tasks[task.proc].remove(task)
                task.proc = proc
        else:
            for num, t in enumerate(self.tasks[proc][1:]):
                new_st = max(self.tasks[proc][num-1].fn, task.dat)
                if (t.st - new_st >= task.computation): # and new_st < task.st:
                    self.tasks[proc].insert(1+num, task)
                    self.tasks[task.proc].remove(task)
                    task.proc = proc
                    break

        if task.parents:
            parent = self.vip(task)
            message = Message(parent, task, self.comm_dict[(parent.index, task.index)])
            if not self.links[message.parent.proc]:
                self.links[message.parent.proc].append(message)
            else:
                for num, m in enumerate(self.links[message.parent.proc][1:]):
                    new_st = max(self.links[message.parent.proc][1 + num-1].fn, message.parent.fn)
                    if (m.st - new_st >= message.communication):
                        self.links[message.parent.proc].insert(num, message)
                        break
        self.update(pivot_pe, proc)


    def update(self, proc, pivot_pe):
        for msg in self.links[pivot_pe]:
            msg.child.dat += self.comm_dict[(msg.parent.index, msg.child.index)]
        for proc in [pivot_pe, proc]:
            # pprint(self.tasks)
            for num, task in enumerate(self.tasks[proc][1:]):
                # for t in graph.get_parents(task):
                # task.dat = max(task.dat, t.fn)# + graph.get_edge(t, task))
                task.st = max(self.tasks[proc][1+num-1].fn, task.dat)
                task.fn = task.st + task.computation
            # pprint(self.tasks)

    def vip(self, task):
        if task.parents:
            parent = max([(self.comm_dict[(t.index, task.index)], t) for t in task.parents], key=lambda x: x[0])
        else:
            parent = (None, None)
        return parent[1]

class Message:
    def __init__(self, parent_node, node, communication):
        self.parent = parent_node
        self.child = node
        self.communication = communication
        self.st = 0
        self.fn = self.communication
    def __repr__(self):
        return self.__class__.__name__ + "( " + str(self.parent) + ", " + str(self.child) + " )"

class Task(Node):
    def __init__(self, node):
        super().__init__(node.index, node.computation, node.tranfering)
        self.st = 0
        self.fn = self.computation
        self.dat = -1
        self.proc = None
        self.parents = []
