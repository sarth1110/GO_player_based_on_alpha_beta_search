from copy import deepcopy
import sys

def readInput():
    lineCount = 1
    currBoard = []
    prevBoard = []
    with open('input.txt', 'r') as f:
        for line in f:
            if lineCount == 1:
                myPiece = int(line)
            elif lineCount < 7:
                prevBoard.append(list(line)[:-1])
            else:
                if(lineCount == 11):
                    currBoard.append(list(line))
                else:
                    currBoard.append(list(line)[:-1])
            lineCount+=1
    return myPiece, prevBoard, currBoard

def isValidIndex(row, col):
    if((row<5 and row>=0) and (col<5 and col>=0)):
        return True
    return False
    
def findNeighbourPositions(row, col):
    neighbours=[]
    neighbourList = [[-1,0],[1,0], [0,-1], [0,1]]
    for n in neighbourList:
        if(isValidIndex(row+n[0], col+n[1])):
            neighbours.append([row+n[0], col+n[1]])
    return neighbours

def findFriends(board, row, col, stone):
    friends = []
    BFS = [[row, col]]
    while(len(BFS)>0):
        curr = BFS.pop()
        friends.append(curr)
        neighbours = findNeighbourPositions(curr[0], curr[1])
        for n in neighbours:
            if(board[n[0]][n[1]] == stone):
                if(([n[0], n[1]] not in BFS) and ([n[0], n[1]] not in friends)):
                    BFS.append([n[0], n[1]])
    return friends

def checkLiberty(board, row, col, stone):
    count=0
    friends = findFriends(board, row, col, stone)
    for f in friends:
        neighbours = findNeighbourPositions(f[0], f[1])
        for n in neighbours:
            if board[n[0]][n[1]]==0:
                count+=1
    return count

def adjacentAttack(board, row, col, myPiece):
    neighbourList = [[-1,0],[1,0], [0,-1], [0,1]]
    for n in neighbourList:
        if(isValidIndex(row+n[0], col+n[1])):
            if(board[row+n[0]][col+n[1]] == (3-myPiece)):
                return True
    return False

def diagonalAttack(board, row, col, myPiece):
    diagonalList = [[-1,-1], [-1,1], [1,-1], [1,1]]
    for n in diagonalList:
        if(isValidIndex(row+n[0], col+n[1])):
            if(board[row+n[0]][col+n[1]] == (3-myPiece)):
                return True
    return False

def diagonalFriend(board, row, col, myPiece):
    diagonalList = [[-1,-1], [-1,1], [1,-1], [1,1]]
    for d in diagonalList:
        if(isValidIndex(row+d[0], col+d[1])):
            if(board[row+d[0]][col+d[1]] == (myPiece)):
                return True
    return False

def adjacentFriend(board, row, col, myPiece):
    neighbourList = [[-1,0],[1,0], [0,-1], [0,1]]
    for n in neighbourList:
        if(isValidIndex(row+n[0], col+n[1])):
            if(board[row+n[0]][col+n[1]] == (myPiece)):
                return True
    return False

def findDeadStones(board, stone):
    deadStones = []
    for i in range(5):
        for j in range(5):
            if board[i][j]==stone:
                lib = checkLiberty(board, i, j, stone)
                if(lib==0):
                    deadStones.append([i,j])
    return deadStones

def removeDeadStones(board, stone):
    deadStones = findDeadStones(board, stone)
    for deads in deadStones:
        board[deads[0]][deads[1]]=0
        
def compareBoards(currBoard, prevBoard):
    for i in range(5):
        for j in range(5):
            if(currBoard[i][j] != prevBoard[i][j]):
                return False
    return True 

def countStones(board, stone):
    count=0
    atRisk=0
    for i in range(5):
        for j in range(5):
            if(board[i][j] == stone):
                count+=1
                if checkLiberty(board, i, j, stone)<=1:
                    atRisk+=1
    return count, atRisk

def checkValidMove(currBoard, prevBoard, row, col, stone):
    if not isValidIndex(row, col):
        return False
    if currBoard[row][col]!=0:
        return False
    
    boardAfterMove = deepcopy(currBoard)
    boardAfterMove[row][col] = stone
    
    if(checkLiberty(boardAfterMove, row, col, stone)>0):
        return True
    
    else:
        deadStones = findDeadStones(boardAfterMove, 3-stone)
        if(len(deadStones)==0):
            return False
        else:
            removeDeadStones(boardAfterMove, 3-stone)
            return not compareBoards(boardAfterMove, prevBoard)

def findAllValidMoves(currBoard, prevBoard, stone, step):
    validMoves=[]
    for i in range(5):
        for j in range(5):
            if currBoard[i][j]==0:
                if adjacentAttack(currBoard, i, j, stone) or diagonalAttack(currBoard, i, j, stone):
                    if checkValidMove(currBoard, prevBoard, i, j, stone):
                        if(adjacentFriend(currBoard, i, j, stone)):
                            validMoves.insert(0, [i,j])
                        else:
                            validMoves.append([i,j])
    return validMoves

def findAllValidMovesAdj(currBoard, prevBoard, stone, step):
    validMoves=[]
    for i in range(5):
        for j in range(5):
            if currBoard[i][j]==0:
                if adjacentFriend(currBoard, i, j, stone):
                    if checkValidMove(currBoard, prevBoard, i, j, stone):
                        validMoves.append([i,j])
    return validMoves

def calculateScore(board, stone):
    score, stonesAtRisk = countStones(board, stone)
    if(stone==2):
        score+=2.5
    return score, stonesAtRisk

def evalationFunction(board, stone, blackDead, whiteDead, move, step):
    blackStone, blackOnRisk = calculateScore(board, 1)
    whiteStone, whiteOnRisk = calculateScore(board, 2)
    
    if stone == 1:
        evalScore = blackStone - whiteStone
        evalScore += whiteOnRisk - blackOnRisk
        evalScore += whiteDead*attackFactor[GLOBALMYPIECE] - blackDead*defenseFactor[GLOBALMYPIECE]
    else:
        evalScore = whiteStone - blackStone
        evalScore += blackOnRisk - whiteOnRisk
        evalScore += blackDead*attackFactor[GLOBALMYPIECE] - whiteDead*defenseFactor[GLOBALMYPIECE]
    
    return evalScore    
    
def maxValue(currBoard, prevBoard, stone, alpha, beta, depth, step, blackDead, whiteDead, move):
    
    if depth == 0 or step>=24:
        return evalationFunction(currBoard, stone, blackDead, whiteDead, move, step)
    maxVali = -sys.maxsize
    validMoves = findAllValidMoves(currBoard, prevBoard, stone, step)
    for move in validMoves:
        
        boardAfterMove = deepcopy(currBoard)
        boardAfterMove[move[0]][move[1]] = stone
        
        deadStones = findDeadStones(boardAfterMove, 3-stone)
        if stone==2:
            blackDead+=len(deadStones)
        else:
            whiteDead+=len(deadStones)
        removeDeadStones(boardAfterMove, 3-stone)
        value = minValue(currBoard, prevBoard, 3-stone, alpha, beta, depth-1, step+1, blackDead, whiteDead, move)
        maxVali = max(maxVali, value)
        alpha = max(alpha, maxVali)
        
        if beta<=alpha:
            break
    return maxVali

def minValue(currBoard, prevBoard, stone, alpha, beta, depth, step, blackDead, whiteDead, move):
    if depth == 0 or step>=24:
        return evalationFunction(currBoard, stone, blackDead, whiteDead, move, step)
    minVali = sys.maxsize
    validMoves = findAllValidMoves(currBoard, prevBoard, stone, step)
    for move in validMoves:
        boardAfterMove = deepcopy(currBoard)
        boardAfterMove[move[0]][move[1]] = stone
        
        deadStones = findDeadStones(boardAfterMove, 3-stone)
        if stone==2:
            blackDead+=len(deadStones)
        else:
            whiteDead+=len(deadStones)
        removeDeadStones(boardAfterMove, 3-stone)
        value = maxValue(currBoard, prevBoard, 3-stone, alpha, beta, depth-1, step+1, blackDead, whiteDead, move)
        minVali = min(minVali, value)
        beta = min(beta, minVali)
        if beta<=alpha:
            break
    return minVali
        
def alphaBetaSearch(currBoard, prevBoard, positionPoints, stone, alpha, beta, depth, step):
    validMoves = findAllValidMoves(currBoard, prevBoard, stone, step)
    if(len(validMoves)==0):
        validMoves = findAllValidMovesAdj(currBoard, prevBoard, stone, step)
    moveValue = {}
    maxVali = -sys.maxsize
    for move in validMoves:
        blackDead=0
        whiteDead=0
        
        boardAfterMove = deepcopy(currBoard)
        boardAfterMove[move[0]][move[1]] = stone
        
        deadStones = findDeadStones(boardAfterMove, 3-stone)
        
        if stone==2:
            blackDead=len(deadStones)
        else:
            whiteDead=len(deadStones)
        removeDeadStones(boardAfterMove, 3-stone)
        minimaxValue = minValue(currBoard, prevBoard, 3-stone, alpha, beta, depth-1, step+1, blackDead, whiteDead, move)
        
        liberty = checkLiberty(boardAfterMove, move[0], move[1], stone)
        
        if(step<=12):
            currValue = minimaxValue + positionPoints[move[0]][move[1]] + liberty*2 + attackFactor[GLOBALMYPIECE]*len(deadStones)
        else:
            currValue = minimaxValue + liberty*2 + attackFactor[GLOBALMYPIECE]*len(deadStones)
        
        if(step<=14):
            if(adjacentFriend(boardAfterMove, move[0], move[1], stone)):
                currValue += 3
            if(diagonalFriend(boardAfterMove, move[0], move[1], stone)):
                currValue += 1
            
            if(adjacentAttack(boardAfterMove, move[0], move[1], stone)):
                currValue += 3
            if(diagonalAttack(boardAfterMove, move[0], move[1], stone)):
                currValue += 1
        
        maxVali = max(maxVali, currValue)
        alpha = max(alpha, maxVali)
        moveValue[''.join([str(m) for m in move])] = currValue
        
    for move in moveValue:
        if moveValue[''.join([str(m) for m in move])] == maxVali:
            return move
    return []

def writeOutput(move):
    if len(move)==0:
        outputString = "PASS"
    else:
        outputString= str(move[0]) + "," + str(move[1])
    f = open("output.txt", "w")
    f.write(outputString)
    f.close()
    
def writeHelperFile(step):
    f = open("helper.txt", "w")
    f.write(str(step))
    f.close()

def readHelper(myPiece):
    step=myPiece
    with open('helper.txt', 'r') as f:
        for line in f:
            step=int(line)
    return step

#---------------------------------PLAY--------------------------------#

myPiece, prevBoard, currBoard = readInput()
      

GLOBALMYPIECE = myPiece
attackFactor = [0,13,10]
defenseFactor = [0,16,16]

positionPoints= [[-2, 0, 1, 0, -2], 
                [0, 0.5, 2, 0.5, 0], 
                [1, 2, 3, 2, 1], 
                [0, 0.5, 2, 0.5, 0], 
                [-2, 0, 1, 0, -2]]

for i in range(5):
    for j in range(5):
        prevBoard[i][j] = int(prevBoard[i][j])
        currBoard[i][j] = int(currBoard[i][j])

#start   

alpha = -sys.maxsize
beta = sys.maxsize

if prevBoard == [[0]*5]*5:
    step = myPiece-1
else:
    step = readHelper(myPiece)

maxDepth = 4

if prevBoard == [[0]*5]*5:
    if currBoard[2][2]==0:
        writeOutput([2,2])
    elif step == 1 :
        writeOutput([2,1])
else:
    move = alphaBetaSearch(currBoard, prevBoard, positionPoints, myPiece, alpha, beta, maxDepth, step)
    writeOutput(move)
step+=2
writeHelperFile(step)
