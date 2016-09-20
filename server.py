import urllib, sys, socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from shutil import copyfile
# Dictionary to track state of ships
ship_info = {'C':[5, 'Carrier'],
             'B':[4, 'Battleship'],
             'R':[3, 'Cruiser'],
             'S':[3, 'Submarine'],
             'D':[2, 'Destroyer']}


def process_fire(params):
    try:
        x = int(params['x'][0])
        y = int(params['y'][0])
        print('Recieved fire request on coordinates X: ' + str(x) + ' y: ' + str(y))
        # Check for out of bounds
        if x>9 or x<0 or y>9 or y<0:
            print('Out of bounds')
            return 404, None
        # look for a hit
        elif board[y][x] in list(ship_info.keys()):
            # Still need to determine if it was a sink
            print('Client hit a ' + ship_info[board[y][x]][1])
            msg = 'hit=1'
            if ship_info[board[y][x]][0] > 1:
                ship_info[board[y][x]][0] -= 1
            elif ship_info[board[y][x]][0] == 1:
                ship_info[board[y][x]][0] = 0
                msg += '&sink=' + board[y][x]
                print('Client sunk ' + ship_info[board[y][x]][1])
            # Change state of board to track shots
            board[y][x] = '~'
            return 200, msg
        elif board[y][x] == '_':
            # Change state of board to track shots
            board[y][x] = '~'
            print('Miss')
            return 200, 'hit=0'
        elif board[y][x] == '~':
            print('Already fired on')
            return 410, None
        else:
            print('Bad request')
            return 400, None
    except:
        print('Bad request')
        return 400, None

class BattleshipHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        if self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            query_vars = urllib.parse.parse_qs(self.path)
            fire_result = process_fire(query_vars)

            code = fire_result[0]
            msg = fire_result[1]
            self.send_response(code)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            if msg:
                self.wfile.write(msg.encode())
        else:
            self.send_response(404)

        def log_message(self, format, *args):
            pass


if __name__ == "__main__":
    # Setup a new enemy board for the client.
    copyfile('eboard.blank.txt', 'eboard.txt')
    host = socket.gethostbyname(socket.gethostname())
    port = int(sys.argv[1])
    server = HTTPServer((host, port), BattleshipHandler)

    # Read board file into memory
    with open(sys.argv[2]) as file:
        board = []
        for line in file:
            board.append(list(line))
    print('Board loaded.')
    # Start server
    try:
        print('Server starting on ' + host + ':' + str(port) +'...')
        server.serve_forever()
    except KeyboardInterrupt:
        # Close the server
        print('Server closing...')
        server.socket.close()

