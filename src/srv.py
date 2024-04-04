
import http.server
import socketserver

from os import getenv
from urllib.parse import urlparse, parse_qs

    
from time import sleep

import cal

MIME = "application/json"

# hook after handle one request
def inter():
    return
    # do nothing currecntly
    sleep(
      10
    )

# listen on:
env_port = getenv('MOONS_SRV_PORT')
if env_port is None:
    port = 3333
else:
    port = int(env_port)

address = ('', port)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        fullpath = self.path
        url = urlparse(fullpath)
        path = url.path[1:]  # skip '/'
        query_string = url.query
        # parse to get dict
        params = parse_qs(query_string)
        # `parse_qs`'s value is always `list`
        params_dict = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

        client_ip = self.client_address[0]
        res = cal.DEF_CALL(path, ip=client_ip, **params_dict)

        # set header
        self.send_response(200)
        self.send_header('Content-type', MIME)
        self.end_headers()
        # send response
        self.wfile.write(res)
        inter()


with socketserver.TCPServer(address, MyHttpRequestHandler) as httpd:
    print(f"Serving at port {port}...")
    httpd.serve_forever()

