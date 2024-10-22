
import copy

width = 0
def partial_digest(L):
    width = max(L)
    newL = L
    L.remove(width)
    X = {0, width}
    is_subset_of(0, 1)
    print("Given L:", L)
    place(L, X)

def is_subset_of(main, subset):
    mainList = copy.deepcopy(main)
    subList = copy.deepcopy(subset)

    if not isinstance(mainList, list):
        mainList = [mainList, 'JJ']
    if not isinstance(subList, list):
        subList = [subList, 'JJ']

    for x in subList:
            if x in mainList:
                mainList.remove(x)
            else:
                return False    
    return True


   

def place(L, X):
    if len(L) == 0:
        print("Answer", X)
        return
    
    # print("L: ", L)
    # print("X: ", X)

    L.sort()
    for y in L[::-1]:
        listX = list(X)
        deltaYX = []
        for x_i in listX:
            deltaYX.append(abs(y-x_i))

        if is_subset_of(L, deltaYX):
            X.add(y)
            for l in deltaYX:
                L.remove(l)
            place(L, X)
            if len(L) == 0:
                return
            X.remove(y)
            for l in deltaYX:
                L.append(l)

        deltaWidthYX = []
        for x_i in listX:
            deltaWidthYX.append(abs(x_i - abs(width-y)))

        if is_subset_of(L, deltaWidthYX):
            
            X.add(abs(width-y))
            for l in deltaWidthYX:
                L.remove(l)
            
            place(L, X)
            if len(L) == 0:
                return
            X.remove(abs(width-y))
            for l in deltaWidthYX:
                L.append(l)
            
    return


if __name__ == "__main__":

    # Given Case
    L = [2, 2, 3, 3, 4, 5, 6, 7, 8, 10]
    
    # Test Case 2
    # L = [3, 5, 5, 8, 9, 14, 14, 17, 19, 22]

    # Test Case for Backtracking
    # L = [1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 6, 7, 7, 7, 8, 9, 10, 11, 12]

    partial_digest(L)

