

import urllib.request
import json

class BadRequest(urllib.error.URLError): pass

def get_ip_location(ip_address: str) -> 'dict[str]':
    '''- On success, returns {'lat': <float>, 'lon': <float>, 'timezone': <str>, ... }
    - On failure, raises BadRequest'''

    url = "http://ip-api.com/json/" + ip_address

    with urllib.request.urlopen(url) as response:
        data = response.read()
        if response.code != 200:
            raise BadRequest()
        location_data = json.loads(data.decode())
    if location_data['status'] == 'fail':
        raise BadRequest(location_data['message'])
    return location_data



def _demo_succ():

    from socket import gethostbyname as g
    ip_address = g('google.com')

    location_info = get_ip_location(ip_address)
    print(location_info)

def _demo_fail():
    ip = '255.255.255.255'
    print(get_ip_location(ip))

if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) == 1:
        _demo_succ()
        _demo_fail()
        exit()
    ip = argv[1]
    loc_d = get_ip_location(ip)
    print(loc_d)
  

