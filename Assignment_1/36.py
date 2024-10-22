import networkx as nx
import matplotlib.pyplot as plt
import copy

class Node:
    def __init__(self, value, inDegree, outDegree):
        self.value = value
        self.inDegree = inDegree
        self.outDegree = outDegree
    
    def increaseIndegree(self):
        self.inDegree = self.inDegree + 1
    
    def increaseOutdegree(self):
        self.outDegree = self.outDegree + 1
    
    def __str__(self) -> str:
        return str(self.value)+ ": inDeg: " + str(self.inDegree) + ", outDeg: " + str(self.outDegree)

def generate_kmers(sequence, k):
    kmers = [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
    return kmers

def build_graph_and_nodes(kmers):
    nodes = {}
    graph = {}

    for k_mer in kmers:
        u = k_mer[:-1]
        v = k_mer[1:]

        if u not in nodes:
            nodes[u] = Node(u, 0, 1)
        else:
            nodes[u].increaseOutdegree()

        if v not in nodes:
            nodes[v] = Node(v, 1, 0)
        else:
            nodes[v].increaseIndegree()

        if u in graph:
            graph[u].append(v)
        else:
            graph[u] = [v]

    return nodes, graph

def findStartingNode(nodes):
    startingNode = None
    for n in nodes:
        if nodes[n].outDegree == nodes[n].inDegree + 1:
            startingNode = n
    if startingNode == None:
        print("KMERS", kmers)
        startingNode = kmers[0][:-1]
    return startingNode

def dfs(graph, start_node):
    copyOfGraph = copy.deepcopy(graph)
    unvisited = set(nodes)
    stack = [start_node]
    path = []

    while stack:
        u = stack[-1]
        if u not in copyOfGraph or len(copyOfGraph[u]) == 0:
            path.append(u)
            if u in unvisited:
                unvisited.remove(u)
            stack.pop()
        else:
            v = copyOfGraph[u].pop()
            stack.append(v)

    if not unvisited:
        path.reverse()
        return [path, True]
    else:     
        return ["-", False]

def formatResult(path):
    result = ""
    pathLength = len(path) - 1
    for i in range(len(path)):
        result += path[i]
        if i < pathLength:
            result += " -> "
    return result

def printIntro(sequence, k):
    print("Given Sequence:", sequence)
    print("Given k value:", k)
    print("Would you like to change these values?")
    print("1. Yes")
    print("2. No, continue with current sequence and k")  
    cmd = input()
    if cmd == "1":
        newSeq = input("Enter Sequence: ")
        newK = input("Enter k: ")
        k = int(newK)
        sequence = newSeq

    return [sequence, k]

def drawGraph(adjacency_list):
    G = nx.DiGraph()

    # Add nodes from adjacency list
    for node in adjacency_list:
        G.add_node(node)

    # Add edges from adjacency list
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Draw the graph
    plt.figure(num="De Brujin Graph")

    pos = nx.spring_layout(G)  # Layout algorithm
    nx.draw(G, pos, with_labels=True, node_size=1100, node_color='#88E079', font_size=10, font_color='black', font_weight='bold', connectionstyle="arc3,rad=0.4", width=1.2)
    
    plt.show()


sequence = "GACTTACGTACT"
k = 3

sequence, k = printIntro(sequence, k)

kmers = generate_kmers(sequence, k)

nodes, graph = build_graph_and_nodes(kmers)

startingNode = findStartingNode(nodes)

path, isAnswer = dfs(graph, startingNode)

if isAnswer:
    result = formatResult(path)
    print("Result:", result)
    drawGraph(graph)
else:
    for node in nodes: 
        # print(node)  
        copyOfGraph = graph 
        # print(copyOfGraph)
        path, isAnswer = dfs(graph, node)   
        if isAnswer:
            result = formatResult(path)
            print("Result:", result)
            drawGraph(graph)
            break
        graph = copyOfGraph