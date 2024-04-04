
import http.server
import socketserver

import sys
import os.path
from os import getenv
from urllib.parse import urlparse, parse_qs

    
from time import sleep

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import cal

MIME = "application/json"

# hook after handle one request
def inter():
    return
    # do nothing currecntly
    sleep(
      10
    )

SKIP_PARAMS = {
        "vercelToolbarCode"
        }

class handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        fullpath = self.path
        url = urlparse(fullpath)
        path = url.path.rsplit('/', 1)[1]  # skip '/'
        if path == 'api': path = ''
        query_string = url.query
        # parse to get dict
        params = parse_qs(query_string)
        # `parse_qs`'s value is always `list`
        params_dict = {k: v[0] if len(v) == 1 else v for k, v in params.items() if k not in SKIP_PARAMS}

        client_ip = self.client_address[0]
        try:
            res = cal.DEF_CALL(path, ip=client_ip, **params_dict)
            status = 200
        except cal.IpLookUpError as e:
            res = cal.BAD_REQ_RES(e, "ip-loc lookup failed")
            status = 400
        except TypeError as e:
            res = cal.BAD_REQ_RES(e, "axtra/invalid params given")
            status = 400


        # set header
        self.send_response(status)
        self.send_header('Content-type', MIME)
        self.end_headers()
        # send response
        self.wfile.write(res)
        inter()


if __name__ == '__main__':
    # listen on:
    env_port = getenv('MOONS_SRV_PORT')
    if env_port is None:
        port = 3333
    else:
        port = int(env_port)

    address = ('', port)
    with socketserver.TCPServer(address, handler) as httpd:
        print(f"Serving at port {port}...")
        httpd.serve_forever()

