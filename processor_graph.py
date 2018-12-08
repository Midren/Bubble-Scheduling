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
    def __init__(self, tasks, graph, pivot_pe):
        self.graph = graph
        tasks[0].proc = pivot_pe
        for num, task in enumerate(tasks[1:]):
            task.proc = pivot_pe

            for t in graph.get_parents(task):
                for tsk in tasks:
                    if tsk == t:
                        self.parents.append(tsk)

            task.dat = max(task.dat, task.fn)# + graph.get_edge(t, task))
            task.st = max(tasks[num-1].fn, task.dat)
            task.fn = task.st + task.computation
        self.tasks = defaultdict(list)
        self.tasks[pivot_pe] = tasks
        self.links = defaultdict(list)

    def st_if_migrate_comp(self, task, proc):
        if not self.tasks[proc]:
            return 0
        for num, t in enumerate(self.tasks[proc][1:]):
            new_st = max(self.tasks[proc][num-1].fn, task.dat)
            if (t.st - new_st >= task.computation): # and new_st < task.st:
                return new_st
        return float("inf")

    def st_if_migrate_comm(self, message, proc):
        if not self.links[message.parent.proc]:
            return 0
        # Can be problem, cause first need to check how will change dat
        for num, m in enumerate(self.links[message.parent.proc][1:]):
            new_st = max(self.links[message.parent.proc][num-1].fn, message.parent.fn)
            if (m.st - new_st >= message.communication):
                return new_st
        return float("inf")

    def st_if_migrate(self, task, proc):
        new_st_2 = 0
        if task.parents:
            parent = max([(graph.get_edge(t, task), t) for t in task.parents])
            new_st_2 = self.st_if_migrate_comm(Message(Task(parent[1]), task, parent[0]))
        new_st_1 = self.st_if_migrate_comp(task, proc)
        # new_st_2 = st_if_migrate_comm(self, Message(Task(parent), task, self.graph.get_edge(parent, task)))
        return max(new_st_1, new_st_2)

    def migrate(self, task, proc):
        if not self.tasks[proc]:
                self.tasks[proc].append(task)
                self.tasks[task.proc].remove(task)
                pivot_pe = task.proc
                task.proc = proc
        else:
            for num, t in enumerate(self.tasks[proc][1:]):
                new_st = max(self.tasks[proc][num-1].fn, task.dat)
                if (t.st - new_st >= task.computation): # and new_st < task.st:
                    self.tasks[proc].insert(num, task)
                    self.tasks[task.proc].remove(task)
                    pivot_pe = task.proc
                    task.proc = proc
                    break

        if task.parents:
            parent = max([(graph.get_edge(t, task), t) for t in task.parents])
            message = Message(Task(parent[1]), task, parent[0])
            if not self.links[message.parent.proc]:
                self.links[message.parent.proc].append(message)
            else:
                for num, m in enumerate(self.links[message.parent.proc][1:]):
                    new_st = max(self.links[message.parent.proc][num-1].fn, message.parent.fn)
                    if (m.st - new_st >= message.communication):
                        self.links[message.parent.proc].insert(num, message)
                        break
        self.update(pivot_pe, proc)


    def update(self, proc, pivot_pe):
        for msg in self.links[pivot_pe]:
            msg.child.dat += self.graph.get_edge(msg.parent, msg.child)
        for proc in [proc, pivot_pe]:
            # pprint(self.tasks)
            for num, task in enumerate(self.tasks[proc][1:]):
                # for t in graph.get_parents(task):
                # task.dat = max(task.dat, t.fn)# + graph.get_edge(t, task))
                task.st = max(self.tasks[proc][num-1].fn, task.dat)
                task.fn = task.st + task.computation
            # pprint(self.tasks)

    def vip(self, task):
        vip = None
        for par in task.parents:
            for msg in self.links[par.proc]:
                if msg.parent == par:
                    if vip is None:
                        vip = msg
                    elif vip.communication < msg.communication:
                        vip = msg
        vip = vip.parent if vip is not None else None
        return vip

class Message:
    def __init__(self, parent_node, node, communication):
        self.parent = parent_node
        self.child = node
        self.communication = communication
        self.st = 0
        self.fn = self.communication_cost

class Task(Node):
    def __init__(self, node):
        super().__init__(node.index, node.computation, node.tranfering)
        self.st = 0
        self.fn = self.computation
        self.dat = 0
        self.proc = None
        self.parents = []
