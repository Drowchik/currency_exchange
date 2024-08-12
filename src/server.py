import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse

from controller import ControlerCurrencies, ControlerExchageRates
from core.config import settings
from core.database import ConnectManager
from dto import DTOConverted
from models import Currencies, ExchangeRates
from router import Router
from service import ServiceConerted


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.router = Router()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        result = self.router.get_controller(self.command, self.path)()
        self.send_my_response(200, 'application/json', json.dumps(result))

    def do_POST(self):
        data = self.help_function()
        result = self.router.get_controller(self.command, self.path)(data)
        self.send_my_response(200, 'application/json', json.dumps(result))

    def do_PATCH(self):
        data = self.help_function()
        result = self.router.get_controller(self.command, self.path)(data)
        self.send_my_response(200, 'application/json',
                              '{"message: "all_good"}')

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
