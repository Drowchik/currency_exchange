import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from exception import RouteNotFoundError
from router import Router


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.router = Router()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            result = self.router.get_controller(self.command, self.path)()
            self.send_my_response(200, 'application/json', json.dumps(result))
        except RouteNotFoundError as e:
            self.send_my_response(404, 'application/json',
                                  json.dumps({"message": str(e)}))

    def do_POST(self):
        try:
            data = self.help_function()
            result = self.router.get_controller(self.command, self.path)(data)
            self.send_my_response(200, 'application/json', json.dumps(result))
        except RouteNotFoundError as e:
            self.send_my_response(404, 'application/json',
                                  json.dumps({"message": str(e)}))

    def do_PATCH(self):
        try:
            data = self.help_function()
            result = self.router.get_controller(
                self.command, self.path)(data, self.path)
            self.send_my_response(200, 'application/json',
                                  '{"message: "all_good"}')
        except RouteNotFoundError as e:
            self.send_my_response(404, 'application/json',
                                  json.dumps({"message": str(e)}))

    def send_my_response(self, code: int, content_type: str, message: str):
        self.send_response(code)
        self.set_headers()
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def set_headers(self):
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header(keyword="Access-Control-Allow-Origin", value='*')
        self.send_header(keyword="Access-Control-Allow-Methods",
                         value='GET, POST, OPTIONS, PATCH')
        self.send_header(keyword='Access-Control-Allow-Headers',
                         value='Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.set_headers()
        self.end_headers()

    def help_function(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        return parse.parse_qs(post_data)


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
