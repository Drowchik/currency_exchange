from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from controller import ControlerCurrencies, ControlerExchageRates
from models import Currencies, ExchangeRates
from urllib import parse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    controler_currencies = ControlerCurrencies(Currencies('currency.db'))
    controler_exchage_rates = ControlerExchageRates(
        ExchangeRates('currency.db'))

    def do_GET(self):
        # parsed_path = parse.urlparse(self.path)
        if self.path == "/currencies":
            self.send_my_response(
                200,
                'application/json',
                json.dumps(self.controler_currencies.get_all()))
        elif self.path.startswith("/currencies/"):
            path = self.path.split("/")[2]
            try:
                data = self.controler_currencies.get_one_data("Code", path)
            except Exception as e:
                self.send_my_response(
                    500, "text/html", "Извините, база данных недоступна")

            if data:
                self.send_my_response(
                    200, "application/json",  json.dumps(data))
            else:
                self.send_my_response(
                    404, "application/json", "Валюта не была найдена")
        elif self.path == "/exchangeRates":
            self.send_my_response(
                200,
                'application/json',
                json.dumps(self.controler_exchage_rates.get_all()))
        elif self.path.startswith("/exchangeRates/"):
            code_all = path = self.path.split("/")[2]
            data = self.controler_exchage_rates.get_one_data(code_all)
            self.send_my_response(
                200, "application/json", json.dumps(data))
        else:
            self.send_my_response(
                500, "text/html", "Извините, такой страницы нет")

    def send_my_response(self, code: int, content_type: str, message: str):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def do_POST(self):
        if self.path == "/currencies":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = parse.parse_qs(post_data)
            self.controler.add_data(data)
            data = self.controler.get_one_data("Code", data.get('code')[0])
            self.send_my_response(200, "application/json", json.dumps(data))


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
