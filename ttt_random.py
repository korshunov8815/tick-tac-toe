N = 5
maxDepth = 3
results = {}
import random,re
nextmove=''

from operator import itemgetter
import time, sys
sys.setrecursionlimit(1000000)

class field:

    def __init__(self, fieldString):
        self.fieldString = fieldString

    def getPossibleMoves(self, move):

        fieldString = self.fieldString

        moves = []
        for i in range(0,N*N):
            if fieldString[i]==' ':
                moves.append([fieldString[:i]+move.lower()+fieldString[i+1:],'N'])
            elif fieldString[i].lower()!=move.lower() and str.islower(fieldString[i]):
                moves.append([fieldString[:i]+move.upper()+fieldString[i+1:],'R'])
        return moves

    def getScore(self, turnNumber):
        winner = self.getWinner()
        if (winner=='X'):
            return (N*N-turnNumber)*10**(N-1)
            #return (N*N)*10**(N-1)
        elif (winner=='O'):
            return (-N*N+turnNumber)*10**(N-1)
            #return (N*N)*10**(N-1)
        else:
            return 0;

    def gameEnded(self):
        if (' ' not in self.fieldString or self.getScore(0)!=0):
            return True
        else:
            return False

    def printField(self):
        print('\n\n')
        for i in range(0,N):
            print('-'*(4*N+1))
            print('|',end='')
            for j in range(0,N):
                print(' '+self.fieldString[i*N+j]+' |', end='')
            print('')
        print('-'*(4*N+1))

    def newMoveString (self,pos,move):
        if (self.fieldString[pos-1]==' '):
            return self.fieldString[:pos-1]+move.lower()+self.fieldString[pos:]
        else:
            rand = random.uniform(0,1)
            print('player is trying to invade another players cell! rand value:',rand)
            if (rand>0.5):
                return self.fieldString[:pos-1]+move.upper()+self.fieldString[pos:]
            else:
                return self.fieldString

    def getString(self):
        return self.fieldString

    def heuristic(self):
        currentField = (self.fieldString).upper()
        points = 0

        #X perspective
        #diag1
        line=currentField[0:N*N:N+1]
        #finding consecutive length - stackoverflow
        lengthX = line.count('X')
        lengthO = line.count('O')
        #its pointless to continue row if there is other symbol
        if (lengthO==0):
            points += 10**(lengthX-1)
        if (lengthX==0):
            points -= 10**(lengthO-1)
        #diag2
        line=currentField[N-1:N*N-1:N-1]
        lengthX = line.count('X')
        lengthO = line.count('O')
        if (lengthO==0):
            points += 10**(lengthX-1)
        if (lengthX==0):
            points -= 10**(lengthO-1)
        #verticals
        for i in range (0,N):
            line=currentField[i:N*N:N]
            lengthX = line.count('X')
            lengthO = line.count('O')
            if (lengthO==0):
                points += 10**(lengthX-1)
            if (lengthX==0):
                points -= 10**(lengthO-1)
        #horizontals
        for i in range (0,N):
            line=currentField[i*N:(i+1)*N]
            lengthX = line.count('X')
            lengthO = line.count('O')
            if (lengthO==0):
                points += 10**(lengthX-1)
            if (lengthX==0):
                points -= 10**(lengthO-1)

        return round(points)

    def getSymmetryStrings(self):

        fieldString = (self.fieldString).upper()

        stringList = list(fieldString)
        symms = []

        #get vertical symmetry
        for i in range(0,N):
            for j in range(0,N//2):
                stringList[i*N+j], stringList[(i+1)*N-j-1] = stringList[(i+1)*N-j-1], stringList[i*N+j]
        symms.append(''.join(stringList))


        #get horizontal symmetry
        stringList = list(fieldString)
        for i in range(0,N):
            for j in range(0,N//2):
                stringList[j*N+i], stringList[(N-j-1)*N+i] = stringList[(N-j-1)*N+i], stringList[j*N+i]
        symms.append(''.join(stringList))


        '''#get reverse(?) symmetry
        stringList = list(fieldString)
        for i in range(0,N*N//2):
            stringList[i], stringList[N*N-1-i] = stringList[N*N-1-i], stringList[i]
        symms.append(''.join(stringList))'''

        #get diag1 symmetry
        stringList = list(fieldString)
        for i in range(0,N):
            for j in range(i,N):
                stringList[i*N+j], stringList[j*N+i] = stringList[j*N+i],stringList[i*N+j]
        symms.append(''.join(stringList))

        #get diag2 symmetry
        stringList = list(fieldString)
        for i in range(0,N):
            for j in range(0,N-i):
                stringList[i*N+j], stringList[(N-1-j)*N+(N-1-i)] = stringList[(N-1-j)*N+(N-1-i)],stringList[i*N+j]
        symms.append(''.join(stringList))

        return symms



    def getWinner(self):

        currentField=(self.fieldString).upper()

        #diag1
        line=currentField[0:N*N:N+1]
        if (line[0]!=' ' and len(set(line))==1):
            return line[0]

        #diag2
        line=currentField[N-1:N*N-1:N-1]
        if (line[0]!=' ' and len(set(line))==1):
            return line[0]

        #verticals
        for i in range (0,N):
            line=currentField[i:N*N:N]
            if (line[0]!=' ' and len(set(line))==1):
                return line[0]

        #horizontals
        for i in range (0,N):
            line=currentField[i*N:(i+1)*N]
            if (line[0]!=' ' and len(set(line))==1):
                return line[0]

        return None

def minimax(fieldString, move, depth, alpha, beta):

    currentField = field(fieldString);
    global mainField, nextmove

    symms = currentField.getSymmetryStrings()
    symmFound = False
    for symm in symms:
        if symm in results:
            if (depth>0):
                return results[symm]

    if (depth>maxDepth):
        return currentField.heuristic()

    if (currentField.getWinner() is not None):
        return currentField.getScore(depth)

    if (currentField.gameEnded()):
        return 0;

    active_turn = move
    local_scores = []
    score = 0

    possibleMoves = currentField.getPossibleMoves(move)

    for possibleField in possibleMoves:
        if possibleField[0] in results:
            score = results[possibleField[0]]
            local_scores.append([possibleField[0],score,possibleField[1]])
        else:
            if possibleField[1]=='R':
                if (depth>50):
                    return 0
                else:
                    #good scenario
                    score1 = minimax(possibleField[0], 'X' if (move=='O') else 'O', depth+1, alpha,beta)
                    #bad scenario
                    score2 = minimax(fieldString, 'X' if (move=='O') else 'O', depth+1, alpha,beta)
                    score = int((score1+score2)/2)
            else:
                score = minimax(possibleField[0], 'X' if (move=='O') else 'O', depth+1, alpha,beta)
            local_scores.append([possibleField[0],score,possibleField[1]])
            results[possibleField[0]] = score

        '''if (active_turn=='X'):
            if score > alpha:
                alpha = score
        else:
            if score < beta:
                beta = score
        if beta < alpha:
            break'''

    if (depth==0):
        print(local_scores, depth, N*N-depth,-N*N+depth )

    local_scores=sorted(local_scores, key=itemgetter(1), reverse=True)
    returnField = local_scores[0][0] if (active_turn=='X') else local_scores[-1][0]
    returnScore = local_scores[0][1] if (active_turn=='X') else local_scores[-1][1]
    moveType = local_scores[0][2] if (active_turn=='X') else local_scores[-1][2]
    candidates = []



    '''for candidate in local_scores:
        if abs(candidate[1]-returnScore < 0.1):
            if (depth==0):
                print('we are appending candidate here , coz ',abs(candidate[1]-returnScore), abs(candidate[1]-returnScore) < 0.1)
            candidates.append(candidate)
    suggestion = random.choice(candidates)
    if (depth==0):
        print(candidates)'''
    if (depth==0):
        if (moveType=='R'):
            rand = random.uniform(0,1)
            print ('computer is trying to capture your cell!! rand value', rand)
            if (rand>0.5):
                newFieldString = returnField
            else:
                newFieldString = fieldString
        else:
            newFieldString= returnField
        field(newFieldString).printField()
        mainField = field(newFieldString)
    return returnScore



mainField = field(' '*N*N)


while (not mainField.gameEnded()):
    minimax(mainField.getString(),'X',0,-99999,99999)

    if mainField.gameEnded():
        break;

    fieldNum = int(input('Choose your move number '))
    mainField = field(mainField.newMoveString(fieldNum,'O'))
    print('field after your move')
    mainField.printField()
    fieldNum = input('Press enter for computer move')

if mainField.getWinner() is not None:
    print('Player',mainField.getWinner(),'wins!')
else:
    print ('Its a draw!')

'''mainField = field('O   O     ')
symms = mainField.getPossibleMoves('X')
for sym in symms:
    print(sym)'''
