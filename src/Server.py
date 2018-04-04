from http.server import BaseHTTPRequestHandler, HTTPServer
import DiagQuery
import json
import logging

class Server(BaseHTTPRequestHandler):
    inquryer=DiagQuery.DiagInqury()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        data_string = (self.rfile.read(int(self.headers['Content-Length']))).decode('utf-8')
        logging.critical(data_string)
        result=self.inquryer.inqury(json.loads(data_string))
        respon=json.dumps(result)
        logging.critical(respon)
        self.wfile.write(respon.encode('utf-8'))

        
def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()