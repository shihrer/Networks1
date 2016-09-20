import urllib, sys
from http.client import HTTPConnection

# Dictionary for converting server responses to the full ship type
ship_dict = {'C': 'Carrier', 'B': 'Battleship', 'R': 'Cruiser', 'S': 'Submarine', 'D': 'Destroyer'}
# State of enemy board
e_board = []
e_file = 'eboard.txt'


# Handle responses from server.
# Can be HTTP 200, 400, 410, 404
def handle_response(the_response, coords):
    # Store the response code and data
    code = the_response.code
    data = the_response.read().decode()
    read_file()

    # Check code values
    if code == 200:
        # OK, either a hit or a miss
        query_vars = urllib.parse.parse_qs(data)
        if int(query_vars['hit'][0]) == 0:
            # Miss
            print('That was a miss.')
            e_board[coords[1]][coords[0]] = '~'
        elif int(query_vars['hit'][0]) == 1:
            # Hit
            print('That was a hit!')
            e_board[coords[1]][coords[0]] = 'X'
            if 'sink' in list(query_vars.keys()):
                # Sunk a ship
                print('You sunk a ' + ship_dict[query_vars['sink'][0]])
    elif code == 400:
        # Bad request
        print('Your request was invalid.  Ensure that you supplied an x and y coordinate.')
    elif code == 404:
        # Not Found
        print('Your coordinates were invalid.  Please try new coordinates.')
    elif code == 410:
        # Gone
        print('You already fired on those coordinates.')
    else:
        # Any other response
        print('Unhandled response.')

    save_result()

def save_result():
    with open(e_file, 'w') as file:
        for line in e_board:
            file.write(''.join(line))

def read_file():
    with open(e_file) as the_file:
        for line in the_file:
            e_board.append(list(line))

if __name__ == '__main__':
    # Setup connection with values passed on command line
    # argv[1] is the server's IP, argv[2] is the server's port
    http_conn = HTTPConnection(sys.argv[1], sys.argv[2])
    # Setup headers
    headers = {'Content-type':'application/x-www-form-urlencoded', 'Content-Length': 7}
    # Encode the parameters into ?x=val&y=val
    fire_coords = (int(sys.argv[3]), int(sys.argv[4]))
    params = urllib.parse.urlencode({'x':fire_coords[0], 'y':fire_coords[1]})
    # Make the POST request for the fire
    http_conn.request('POST', params, None, headers)
    # Retrieve the response
    the_response = http_conn.getresponse()
    # Close the connection
    http_conn.close()
    # Have the client handle the response
    handle_response(the_response, fire_coords)