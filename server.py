board = []
eboard = []
hit=0
sink='A'
c=5
b=4
r=3
s=3
d=2


with open('board.txt') as my_file:
    board = my_file.readlines()

with open('eboard.txt') as my_file:
    eboard = my_file.readlines()



x=0
y=0

char = board[y][x]

charlist = list(board[y])

if char=='~':
    print("ERROR 410")

if char=='_':
    hit=0
    charlist[x] = '~'

if char=='C':
    hit=1
    c=c-1
    if c==0:
        sink='C'
    charlist[x] = '~'

if char=='B':
    hit=1
    b=b-1
    if b==0:
        sink='B'
    charlist[x] = '~'

if char=='R':
    hit=1
    r=r-1
    if r==0:
        sink='R'
    charlist[x] = '~'

if char=='S':
    hit=1
    s=s-1
    if s==0:
        sink='S'
    charlist[x] = '~'

if char=='D':
    hit=1
    d=d-1
    if d==0:
        sink='D'
    charlist[x] = '~'

print(hit,sink)