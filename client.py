import urllib, sys
from http.client import HTTPConnection

# Handle responses from server.
# Can be HTTP 200, 400, 410, 404
def handle_response(response):
    # Dictionary for converting server responses to the full ship type
    ship_dict = {'C': 'Carrier', 'B': 'Battleship', 'R':'Cruiser', 'S':'Submarine','D':'Destroyer'}

    # Store the response code and data
    code = response.code
    data = response.read().decode()

    # Check code values
    if code == 200:
        # OK, either a hit or a miss
        query_vars = urllib.parse.parse_qs(data)
        if int(query_vars['hit'][0]) == 0:
            # Miss
            print('That was a miss.')
        elif int(query_vars['hit'][0]) == 1:
            # Hit
            print('That was a hit!')
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

if __name__ == '__main__':
    # Setup connection with values passed on command line
    # argv[1] is the server's IP, argv[2] is the server's port
    http_conn = HTTPConnection(sys.argv[1], sys.argv[2])
    # Setup headers
    headers = {'Content-type':'application/x-www-form-urlencoded', 'Content-Length': 7}
    # Encode the parameters into ?x=val&y=val
    params = urllib.parse.urlencode({'x':sys.argv[3], 'y':sys.argv[4]})
    # Make the POST request for the fire
    http_conn.request('POST', params, None, headers)
    # Retrieve the response
    response = http_conn.getresponse()
    # Close the connection
    http_conn.close()
    # Have the client handle the response
    handle_response(response)