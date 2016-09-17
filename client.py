import socket

player = input("Enter player (1 or 2): ")
p = int(player)
xString = input("Enter x coordinate: ")
x=int(xString)
yString = input("Enter y coordinate: ")
y=int(yString)

fire = "x=%s&y=%s"% (xString,yString)
print(fire)

answer = "20"

if p==1:
    file="eboard.txt"
else:
    file="eboard2.txt"

with open(file) as my_file:
    eboard = my_file.readlines()

if answer =="404 Not Found":
    print("out of bounds.")
    xString = input("Enter x coordinate: ")
    yString = input("Enter y coordinate: ")

if answer=="410 Gone":
    print("spot already fired upon")
    xString = input("Enter x coordinate: ")
    yString = input("Enter y coordinate: ")

if answer=="400 Bad Request":
    print("bad request")
    xString = input("Enter x coordinate: ")
    yString = input("Enter y coordinate: ")

if answer[0]=="2":
    if answer[1]=="1":
        row = list(eboard[y])
        row[x] = "X"
        eboard[y] = ''.join(row)
        f = open(file, 'w')
        f.truncate()
        for x in eboard:
            f.write(x)
    else:
        row = list(eboard[y])
        row[x] = "~"
        eboard[y] = ''.join(row)
        f= open(file, 'w')
        f.truncate()
        for x in eboard:
            f.write(x)