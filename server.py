import urllib, sys, socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from shutil import copyfile
# Dictionary to track state of ships
ship_info = {'C':[5, 'Carrier'],
             'B':[4, 'Battleship'],
             'R':[3, 'Cruiser'],
             'S':[3, 'Submarine'],
             'D':[2, 'Destroyer']}
own_board = ''

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
            # Client hit
            print('Client hit a ' + ship_info[board[y][x]][1])
            # Setup message for hit
            msg = 'hit=1'
            # Check to see if client sunk a ship
            if ship_info[board[y][x]][0] > 1:
                # No sink, update ship state
                ship_info[board[y][x]][0] -= 1
            elif ship_info[board[y][x]][0] == 1:
                # This was a sink.  Update state and modify message.
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

def board_html(file_name):
    if file_name:
        with open(file_name) as the_file:
            return the_file.read()
    else:
        return ''

def display_board(title, header, board_file=None):
    if board_file:
        html_string = board_html(board_file)
    else:
        html_string = ''
    return '<html><head><title>{:s}</title></head><body><h1>{:s}</h1><pre>{:s}</pre></body></html>'.format(title, header, html_string)


class BattleshipHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('Received GET request to path: ' + self.path)
        route = self.path
        code = 404
        if route == '/own_board.html':
            print('Displaying own_board.html...')
            code = 200
            message = display_board('Your Board', "Player's Board", own_board)
        elif route == '/opponent_board.html':
            print('Displaying opponent_board.html...')
            code = 200
            message = display_board('Opponent Board', "The Opponenet's Board", 'eboard.txt')
        else:
            message = display_board('Oops', 'HTTP 404 Not Found')

        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(message.encode())

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
    own_board = sys.argv[2]
    with open(own_board) as file:
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

