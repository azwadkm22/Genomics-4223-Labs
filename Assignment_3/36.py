ScoreMatrix = []
Path = []
ScoreMatch = 10
ScoreMismatch = -2
ScoreGap = -5

def scoring_function(a, b):
    if a==b and a != '-':
        return ScoreMatch
    if (a == '-' and b != '-') or (b == '-' and a != '-'):
        return ScoreGap
    if a != b:
        return ScoreMismatch
    
def initialize_score_matrix(s1, s2):
    for i in range(len(s1)):
        scoreRow = []
        for j in range(len(s2)):
            scoreRow.append(-100)
        ScoreMatrix.append(scoreRow)
    
    for i in range(len(s1)):
        for j in range(len(s2)):
            ScoreMatrix[i][0] = scoring_function('-', s2[j]) * i
            ScoreMatrix[0][j] = scoring_function(s1[i], '-') * j 

    for i in range(len(s1)):
        pathRow = []
        for j in range(len(s2)):
            pathRow.append([-1])
        Path.append(pathRow)

def find_max_val_and_index(s1, s2, i, j):
    a = ScoreMatrix[i][j]  + scoring_function(s1[i+1],s2[j+1])
    b = ScoreMatrix[i][j+1] + scoring_function(s1[i+1], '-')
    c = ScoreMatrix[i+1][j] + scoring_function('-', s2[j+1])
    maxx = max(a, b, c)
    node = []
    if maxx == a:
        node = [i, j]
    elif maxx == b:
        node = [i, j+1]
    elif maxx == c:
        node = [i+1, j]
    return maxx, node
    
def fillup_score_matrix(s1, s2):
    for i in range(len(s1)-1):
        for j in range(len(s2)-1):
            ScoreMatrix[i+1][j+1],  node = find_max_val_and_index(s1, s2, i, j) 
            Path[i+1][j+1] = node

def printScoreMatrix():
    print("Score Matrix:")        
    for i in ScoreMatrix:
        print(i)

def findTrace(s1, s2):
    p = Path[len(s1)-1][len(s2)-1]
    trace = [[len(s1)-1, len(s2)-1], ]
    scoreTrace = [ScoreMatrix[len(s1)-1][len(s2)-1], ]
    while p != [-1]:
        trace.append(p)
        scoreTrace.append(ScoreMatrix[p[0]][p[1]])
        p = Path[p[0]][p[1]]
    
    return trace, scoreTrace

def find_alignment(prev, nxt):
    if (nxt[0] == prev[0] + 1) and ((nxt[1] == prev[1] + 1)):
        return ('Diagonal')
    elif (nxt[0] == prev[0] + 1) and ((nxt[1] == prev[1])):
        return ("Insertion")
    elif (nxt[1] == prev[1] + 1) and (nxt[0] == prev[0]):
        return ("Deletion")

def create_command_list_from_trace(trace):
    commandList = []
    for i in range(len(trace) - 1):
        nextNode = trace[i]
        prevNode = trace[i+1]
        commandList.append(find_alignment(prevNode, nextNode))
    commandList.reverse()
    return commandList

def createTheSequences(commandList, s1, s2):
    i = 1
    j = 1
    seqA = ""
    seqB = ""
    for cmd in commandList:
        if cmd == "Diagonal":
            seqA = seqA + s1[i]
            seqB = seqB + s2[j]
            i =  i + 1
            j = j + 1
        elif cmd == "Deletion":
            seqA = seqA + "-"
            seqB = seqB + s2[j]
            j = j + 1
        elif cmd == "Insertion":
            seqA = seqA + s1[i]
            seqB = seqB + '-' 
            i = i + 1
    
    return seqA, seqB

def score_and_print(seqA, seqB):
    score = 0
    midLine = ""
    for i in range(len(seqA)):
        score = score + scoring_function(seqA[i], seqB[i])
        if (seqA[i] == seqB[i]):
            midLine = midLine + "|"
        else:
            midLine = midLine + " "
    
    print("Global Pairwise Alignment: ")
    print(seqA)
    print(midLine)
    print(seqB)
    print("Alignment Score: " + str(score))


def take_input(s1, s2, ScoreMatch, ScoreMismatch, ScoreGap):
    print("Would you like to continue with the following settings?")
    print("Seq1 = ", s1)
    print("Seq2 = ", s2)
    print("Scoring Function: ")
    print("Match: ", str(ScoreMatch), "Mismatch: ", str(ScoreMismatch), "Gap: ", str(ScoreGap))
    print("Enter command:")
    print("1. Yes continue with these settings.")
    print("2. Change settings.")
    k = int(input())
    if k == 2:
        print("Enter new Sequence 1: ")
        s1 = input()
        print("Enter new Sequence 2: ")
        s2 = input()
        print("Enter scoring function values.")
        print("For Match:")
        ScoreMatch = float(input())
        print("For MisMatch:")
        ScoreMismatch = float(input())
        print("For Gap:")
        ScoreGap = float(input())
        return s1, s2, ScoreMatch, ScoreMismatch, ScoreGap
    else:
        return s1, s2, ScoreMatch, ScoreMismatch, ScoreGap
    
def find_global_pairwise_alignment():    
    s1 = "CTCGCAGC"
    s2 = "CATTCAG"
    ScoreMatch = 10
    ScoreMismatch = -2
    ScoreGap = -5

    s1, s2, ScoreMatch, ScoreMismatch, ScoreGap = take_input(s1, s2, ScoreMatch, ScoreMismatch, ScoreGap)
    s1 = " " + s1
    s2 = " " + s2

    initialize_score_matrix(s1, s2)
    fillup_score_matrix(s1, s2)

    printScoreMatrix()
    trace, scoreTrace = findTrace(s1, s2)

    commandList = create_command_list_from_trace(trace)

    seqA, seqB = createTheSequences(commandList, s1, s2)

    score_and_print(seqA, seqB)


find_global_pairwise_alignment()