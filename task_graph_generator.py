with open("dag.txt") as f:
    graph = dict()
    for line in f.readlines():
        if(not line.startswith("NODE ")):
            continue
        print(line.split())
