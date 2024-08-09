from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from controller import ControlerCurrencies, ControlerExchageRates
from dto import DTOConverted
from models import Currencies, ExchangeRates
from urllib import parse

from service import ServiceConerted


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    controler_currencies = ControlerCurrencies(Currencies('currency.db'))
    controler_exchage_rates = ControlerExchageRates(
        ExchangeRates('currency.db'))

    def do_GET(self):
        paths_all = {
            "/currencies": self.controler_currencies.get_all,
            "/exchangeRates": self.controler_exchage_rates.get_all,
        }
        paths_one = {
            "/currency/": self.controler_currencies.get_one_data,
            "/exchangeRate/": self.controler_exchage_rates.get_one_data,
        }
        if self.path in paths_all:
            handler = paths_all[self.path]
            try:
                result = handler()
                self.send_my_response(200, 'application/json', result)
            except Exception as e:
                self.send_my_response(
                    500, 'application/json', '{"message": "Database unavailable"}')
        elif any(self.path.startswith(key) for key in paths_one):
            param = self.path.split("/")
            handler = paths_one["/"+param[1]+"/"]
            try:
                data = handler(param[2])
                if data:
                    self.send_my_response(
                        200, "application/json", json.dumps(data))
                else:
                    self.send_my_response(
                        404, "application/json", '{"message": "Data not found"}')
            except:
                self.send_my_response(
                    400, "application/json", '{"message": "The currency code is missing from the address"}')
        elif self.path.startswith("/exchange?"):
            parsed_url = parse.urlparse(self.path)
            query_params = parse.parse_qs(parsed_url.query)
            a = ServiceConerted(self.controler_exchage_rates,
                                DTOConverted(query_params))
            self.send_my_response(
                200, "application/json", json.dumps(a.convert_currency()))
        else:
            self.send_my_response(
                500, "text/html", "Извините, такой страницы нет")

    def send_my_response(self, code: int, content_type: str, message: str):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header(keyword="Access-Control-Allow-Origin", value='*')
        self.send_header(keyword="Access-Control-Allow-Methods",
                         value='GET, POST, OPTIONS, PATCH')
        self.send_header(keyword='Access-Control-Allow-Headers',
                         value='Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header(keyword="Access-Control-Allow-Origin", value='*')
        self.send_header(keyword="Access-Control-Allow-Methods",
                         value='GET, POST, OPTIONS, PATCH')
        self.send_header(keyword='Access-Control-Allow-Headers',
                         value='Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == "/currencies":
            data = self.help_post()
            for field in ['code', 'name', 'sign']:
                if field not in data or not data[field]:
                    self.send_my_response(
                        400, "application/json", '{"message": "Отсутствует обязательное поыле"}'
                    )
                    return
            try:
                self.controler_currencies.add_data(data)
            except Exception as e:
                self.send_my_response(
                    409, "application/json", '{"message": "Валютная пара с таким кодом уже существует"}')
            else:
                data = self.controler_currencies.get_one_data(
                    data.get('code')[0])
                self.send_my_response(
                    200, "application/json", json.dumps(data))
        elif self.path == "/exchangeRates":
            data = self.help_post()
            target, base = self.controler_currencies.get_two_data(data.get("baseCurrencyCode")[0],
                                                                  data.get("targetCurrencyCode")[0])
            self.controler_exchage_rates.add_data(
                rate=data.get("rate")[0], base=base, target=target)
            result = self.controler_exchage_rates.get_one_data(
                data.get("baseCurrencyCode")[0]+data.get("targetCurrencyCode")[0])
            self.send_my_response(
                200, "application/json", json.dumps(result))

    def do_PATCH(self):
        if self.path.startswith("/exchangeRate/"):
            data = self.help_post()
            code_all = path = self.path.split("/")[2]
            target, base = self.controler_currencies.get_two_data(code_all[:3],
                                                                  code_all[3:6])
            self.controler_exchage_rates.patch_data(rate=data.get(
                "rate")[0], base=base.id, target=target.id)

    def help_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        return parse.parse_qs(post_data)


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
