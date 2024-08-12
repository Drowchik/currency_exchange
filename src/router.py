from urllib.parse import parse_qs, urlparse

from controller import ControlerCurrencies, ControlerExchageRates
from core.config import settings
from core.database import ConnectManager
from exception import MissingFieldError, RouteNotFoundError
from models import Currencies, ExchangeRates


class Router:
    def __init__(self) -> None:
        self.coonect_manager = ConnectManager(settings.db_name)
        self.controler_currencies = ControlerCurrencies(
            Currencies(self.coonect_manager))
        self.controler_exchage_rates = ControlerExchageRates(
            ExchangeRates(self.coonect_manager))
        self.routers = {}
        self.setup_routers()

    def add_router(self, path, controller, with_id=False):
        self.routers[path] = {"controller": controller, "with_id": with_id}

    def get_controller(self, command: str, path: str):
        parsed_url = urlparse(path)
        parts = parsed_url.path.split("/")
        query_params = parse_qs(parsed_url.query)

        route = self.routers.get(f'{command}{parts[1]}')

        if not route:
            raise RouteNotFoundError()

        controller = route["controller"]
        with_id = route["with_id"]

        if with_id and len(parts) == 3:
            return lambda: controller(parts[2])
        elif with_id:
            raise MissingFieldError()
        elif query_params:
            return lambda: controller(query_params)

        return controller

    def setup_routers(self) -> None:
        self.add_router("GETcurrencies", self.controler_currencies.get_all)
        self.add_router("GETexchangeRates",
                        self.controler_exchage_rates.get_all)
        self.add_router(
            "GETcurrency", self.controler_currencies.get_one_data, with_id=True)
        self.add_router("GETexchangeRate",
                        self.controler_exchage_rates.get_one_data, with_id=True)
        self.add_router("POSTcurrencies",
                        lambda data: self.controler_currencies.add_data(data))
        self.add_router("POSTexchangeRates",
                        lambda data: self.controler_exchage_rates.add_data(data))
        self.add_router("PATCHexchangeRate", lambda rate, data: self.controler_exchage_rates.patch_data(rate,
                                                                                                        data))
        self.add_router(
            "GETexchange", self.controler_exchage_rates.converted_data)
