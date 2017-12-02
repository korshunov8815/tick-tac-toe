N = 3
results = {}

from operator import itemgetter

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

    def getScore(self):
        winner = self.getWinner()
        if (winner=='X'):
            return 10
        elif (winner=='O'):
            return -10
        else:
            return 0;

    def gameEnded(self):
        if (' ' not in self.fieldString or self.getScore()!=0):
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

    currentField = field(fieldString);

    if (currentField.getWinner() is not None):
        return currentField.getScore()

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


    #sorting local scores
    local_scores=sorted(local_scores, key=itemgetter(1), reverse=True)
    if depth==0:
        print(local_scores)
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

'''mainField = field('XO XO    ')
mainField.printField()
minimax(mainField.getString(),'X',0)'''
