import socket, sys, requests
#
# board = []
# eboard = []
# hit=0
# sink='0'
# c=5
# b=4
# r=3
# s=3
# d=2
#
#
# with open('board.txt') as my_file:
#     board = my_file.readlines()
#
# with open('eboard.txt') as my_file:
#     eboard = my_file.readlines()
#
#
#
# x=0
# y=1
#
# char = board[y][x]
#
# charlist = list(board[y])
#
# if char=='~':
#     print("ERROR 410")
#
# if char=='_':
#     hit=0
#     charlist[x] = '~'
#     board[y] = ''.join(charlist)
#     f = open("board.txt", 'w')
#     f.truncate()
#     for x in board:
#         f.write(x)
#
# if char=='C':
#     hit=1
#     c=c-1
#     if c==0:
#         sink='C'
#     charlist[x] = '~'
#     board[y] = ''.join(charlist)
#     f = open("board.txt", 'w')
#     f.truncate()
#     for x in board:
#         f.write(x)
#
# if char=='B':
#     hit=1
#     b=b-1
#     if b==0:
#         sink='B'
#     charlist[x] = '~'
#     board[y] = ''.join(charlist)
#     f = open("board.txt", 'w')
#     f.truncate()
#     for x in board:
#         f.write(x)
#
# if char=='R':
#     hit=1
#     r=r-1
#     if r==0:
#         sink='R'
#     charlist[x] = '~'
#     board[y] = ''.join(charlist)
#     f = open("board.txt", 'w')
#     f.truncate()
#     for x in board:
#         f.write(x)
#
# if char=='S':
#     hit=1
#     s=s-1
#     if s==0:
#         sink='S'
#     charlist[x] = '~'
#     board[y] = ''.join(charlist)
#     f = open("board.txt", 'w')
#     f.truncate()
#     for x in board:
#         f.write(x)
#
# if char=='D':
#     hit=1
#     d=d-1
#     if d==0:
#         sink='D'
#     charlist[x] = '~'
#     board[y] = ''.join(charlist)
#     f = open("board.txt", 'w')
#     f.truncate()
#     for x in board:
#         f.write(x)
#
# print(hit,sink)
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer

def determine_response(params):
    ships = ['C', 'B', 'R', 'S', 'D']
    x = params['x'][0]
    y = params['y'][0]
    # look at board and see if x,y is hit, miss, out of bounds, already fired at, not formatted right
    # Check for out of bounds
    if x>9 or x<0 or y>9 or y<0:
        return (404, "HTTP Not Found")
    #look for a hit
    elif board[x][y] in ships:
        #
        return (200,'hit=1')

class BattleshipHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        if self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            length = int(self.headers['Content-Length'])
            print(self.headers['Content-Type'])
            query_vars = urllib.parse.parse_qs(self.path)
            print('x: ' + query_vars['x'][0] + ' y: ' + query_vars['y'][0])
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(determine_response(query_vars).encode())
        else:
            self.send_response_only(404)



if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 5001), BattleshipHandler)
    with open(sys.argv[2]) as file:
        board = file.readlines()

    try:
        print('Server starting ')
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

