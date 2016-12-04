def conflict(state,nextX):
    nextY = len(state)
    for i in range(nextY):
        if state[i]==nextX or abs(state[i]-nextX)==nextY-i:
            return True
    return False

def queens(num=8,state=()):
    for pos in range(num):
        if not conflict(state,pos):
            if len(state) == num-1:
                yield (pos,)
            else :
                for result in queens(num,state+(pos,)):
                    yield (pos,)+result

def printQueens(result):
    for i in result :
        print i*'.'+'X'+(len(result)-i-1)*'.'

print len(list(queens()))
print list(queens())

printQueens( random.choice(list(queens())))