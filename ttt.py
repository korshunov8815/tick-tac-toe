N = 3
results = {}
iters = 0;
optimized = 0;

from operator import itemgetter
import time

class field:


    def __init__(self, fieldString):
        self.fieldString = fieldString

    def getPossibleMoves(self, move):

        fieldString = self.fieldString

        moves = []
        for i in range(0,N*N):
            if fieldString[i]==' ':
                moves.append(fieldString[:i]+move+fieldString[i+1:])

        return moves

    def getScore(self, turnNumber):
        winner = self.getWinner()
        if (winner=='X'):
            return N*N-turnNumber
        elif (winner=='O'):
            return -N*N+turnNumber
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
        return self.fieldString[:pos-1]+move+self.fieldString[pos:]

    def getString(self):
        return self.fieldString

    def getSymmetryStrings(self):

        fieldString = self.fieldString

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

        currentField=self.fieldString

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

def minimax(fieldString, move, depth):
    global iters, optimized
    iters += 1

    currentField = field(fieldString);

    symms = currentField.getSymmetryStrings()
    symmFound = False
    for symm in symms:
        if symm in results:
            optimized+=1
            currentField = field(symm)
            symmFound=True

    if (currentField.getWinner() is not None):
        return currentField.getScore(depth)

    if (currentField.gameEnded()):
        return 0;

    active_turn = move
    local_scores = []
    score = 0

    possibleMoves = currentField.getPossibleMoves(move)

    for possibleField in possibleMoves:
        if possibleField in results:
            local_scores.append([possibleField,results[possibleField]])
        else:
            score = minimax(possibleField, 'X' if (move=='O') else 'O', depth+1)
            local_scores.append([possibleField,score])
            results[possibleField] = score

    if depth==0:
        print(local_scores)

    #sorting local scores
    local_scores=sorted(local_scores, key=itemgetter(1), reverse=True)

    global mainField

    if (depth==0):
        print (field(local_scores[0][0]).printField())
        mainField = field(local_scores[0][0])
    if (active_turn=='X'):
        nextField = local_scores[0][0]
        return local_scores[0][1]
    if (active_turn=='O'):
        nextField = local_scores[-1][0]
        return local_scores[-1][1]

mainField = field(' '*N*N)

while (not mainField.gameEnded()):
    minimax(mainField.getString(),'X',0)

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

'''mainField = field('X               ')
symms = mainField.getSymmetryStrings()
for sym in symms:
    print(sym)'''
