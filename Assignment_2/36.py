import networkx as nx
import matplotlib.pyplot as plt
import random

# Code for Drawing Tree, used from Stackoverflow
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc+vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def draw_tree(adjacency_list, root):
    G = nx.Graph()

    # Add nodes from adjacency list
    for node in adjacency_list:
        G.add_node(node)

    # Add edges from adjacency list
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Draw the graph
    plt.figure(num="Phylogenetic Tree")


    pos = hierarchy_pos(G,root)    
    nx.draw(G, pos, with_labels=True, node_size=1100, node_color='#88E079', font_size=10, font_color='black', font_weight='bold', width=1.2)
    plt.show()

# Below is my Implementation

#Finds distance between two strings
def findDistanceBetweenStrings(S1, S2):
    count = 0
    for i in range(len(S1)):
        if(S1[i] != S2[i]):
            count = count +1
    return count

#Makes the initial distance matrix
def makeDistanceMatrix():
    for i in range(len(S)):
        S_i = S[i]
        distance = []
        for j in range(len(S)):
            S_j = S[j]
            if(i == j):
                # break
                distance.append({str("(" + str(StringName[i]) + "," + str(StringName[j]) + ")"):-1})   
            else:
                distance.append({str("(" + str(StringName[i]) + "," + str(StringName[j]) + ")"):findDistanceBetweenStrings(S_i,S_j)})
        DistanceMatrix.append(distance)

#for printing the Distance Matrix
def printDistanceMatrix(Matrix):
    print("Distance Matrix")
    for i in range(1, len(Matrix)):
        distances = Matrix[i]
        for j in range(len(distances)):
            if i==j:
                break
            print(distances[j], end=" ")
        print()

#Finds the DNA Sequence with minimum distance
def findMinDistStrings(Matrix):
    minS1 = -1
    minS2 = -1
    minDist = 99999999
    for i in range(len(Matrix)):
        distances = Matrix[i]
        for j in range(i+1, len(distances)):
            d = list(distances[j].values())
            d = d[0]
            if minDist > d:
                minDist = d
                minS1 = i
                minS2 = j
        
    return minDist, minS1, minS2

#Finds element in List
def find_element(lst, target):
    for index, item in enumerate(lst):
        if item == target:
            return index
    return -1

#Deletes redundant entries from DistanceMatrix
def clearMatrixIndex(distance_matrix, in1, in2):
    
    for i in range(len(distance_matrix)):
        distances = distance_matrix[i]
        if in1 < 0 or in1 >= len(distances) or in2 < 0 or in2 >= len(distances):
            continue
        else:
            distances[in1] = "del"
            distances[in2] = "del"
            StringName[in1] = "del"
            StringName[in2] = "del"
    
    for i in range(len(distance_matrix)):
        distances = distance_matrix[i]
        
        delIndex = find_element(distances, "del")
        if delIndex != -1:
            del distances[delIndex]

        delIndex = find_element(distances, "del")
        if delIndex != -1:
            del distances[delIndex]

        delIndex = find_element(StringName, "del")
        if delIndex != -1:
            del StringName[delIndex]

        delIndex = find_element(StringName, "del")
        if delIndex != -1:
            del StringName[delIndex]

    non_empty_lists = [lst for lst in distance_matrix if lst]

    return non_empty_lists

#Updates DistanceMatrix
def updateDistanceMatrix(distance_matrix, i, j, key):
    new_row = []
    for k in range(len(distance_matrix)):
      if k != i and k != j:
        d_i = list(distance_matrix[k][i].values())[0]
        d_j = list(distance_matrix[k][j].values())[0]
        newD = (d_i + d_j) / 2
        new_row.append({str("(" + key + "," + str(StringName[k]) + ")"):newD})  

    for k in range(len(distance_matrix)):
      if k != i and k != j:
        di_k = list(distance_matrix[i][k].values())[0]
        dj_k = list(distance_matrix[j][k].values())[0]
        newD = (di_k + dj_k) / 2
        distance_matrix[k].append({str("(" + StringName[k] + "," + str(key) + ")") : newD})

    new_row.append({str("(" + key + "," + key + ")"):-1})
    
    distance_matrix[i] = []
    distance_matrix[j] = []
    distance_matrix = clearMatrixIndex(distance_matrix, i, j)
    distance_matrix.append(new_row)
    StringName.append(key)
    
    return distance_matrix


def sortLexicographically(s):
    alphabets = s.split("+")
    alphabets.sort()
    retS = ""
    for i in alphabets:
        retS = retS + i
    return retS

#Tha main UPMGA algorithm that uses functions defined above
def UPMGA():
    makeDistanceMatrix()
    Matrix = DistanceMatrix
    iteration = 1
    while(len(Matrix) != 1):
        print(f"###Iteration {iteration} ###")
        iteration = iteration + 1

        printDistanceMatrix(Matrix)

        minD, s1, s2 = findMinDistStrings(Matrix)

        print("Minimum Distance:" , minD , "For", "(" + StringName[s1] + "-" + StringName[s2] + ")")

        newString = StringName[s1] + "+" + StringName[s2]
        newString = sortLexicographically(newString)

        AdjacencyList[newString] = [StringName[s1], ]
        AdjacencyList[newString].append(StringName[s2])
        Matrix = updateDistanceMatrix(Matrix, s1, s2, newString)
        print()

#Input
S = ["ACGCGTTGGGCGATGGCAAC", "ACGCGTTGGGCGACGGTAAT", "ACGCATTGAATGATGATAAT", "ACGCATTGAATGATGATAAT", "ACACATTGAGTGATAATAAT"]

# String Names
StringName = ["A", "B", "C", "D", "E"]

DistanceMatrix = []
AdjacencyList = {}

UPMGA()

print("Root:", StringName[-1])
print("Adjacency List for Tree:")
print(AdjacencyList)

draw_tree(AdjacencyList, StringName[-1])