
from sys import version_info
import urllib.request
import json

if version_info > (3,9,0):
    def get_status(res): return res.code
else:
    # urllib.response.addinfo status is deprecated since version 3.9
    def get_status(res): return res.status


class BadRequest(urllib.error.URLError): pass

class IpLookUpError(LookupError): pass
def get_ip_location(ip_address: str) -> 'dict[str]':
    '''- On success, returns {'lat': <float>, 'lon': <float>, 'timezone': <str>, ... }
    - On failure, if responce code is not 200, raises BadRequest;
    - On failure, if ip look-up fails, e.g. a private ip is given, raise IpLookUpError'''

    url = "http://ip-api.com/json/" + ip_address

    with urllib.request.urlopen(url) as response:
        data = response.read()
        if get_status(response) != 200:
            raise BadRequest()
        location_data = json.loads(data.decode())
    if location_data['status'] == 'fail':
        raise IpLookUpError(location_data['message'])
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
  

