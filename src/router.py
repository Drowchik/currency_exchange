from controller import ControlerCurrencies, ControlerExchageRates
from core.database import ConnectManager
from models import Currencies, ExchangeRates
from core.config import settings


class Router:
    def __init__(self) -> None:
        self.coonect_manager = ConnectManager(settings.db_name)
        self.controler_currencies = ControlerCurrencies(
            Currencies(self.coonect_manager))
        self.controler_exchage_rates = ControlerExchageRates(
            ExchangeRates(self.coonect_manager))
        self.routers = {}
        self.setup_routers()

    def add_router(self, path, controller):
        self.routers[path] = controller

    def get_controller(self, command: str, path: str):
        parts = path.split("/")
        main_path: str = parts[1]
        controller = self.routers.get(f'{command}{main_path}')
        print(controller)
        if len(parts) > 2:
            return lambda: controller(parts[2])
        return controller

    def setup_routers(self) -> None:
        self.add_router(
            "GETcurrencies", self.controler_currencies.get_all)
        self.add_router(
            "GETexchangeRates", self.controler_exchage_rates.get_all)
        self.add_router(
            "GETcurrency", self.controler_currencies.get_one_data)
        self.add_router(
            "GETexchangeRate", self.controler_exchage_rates.get_one_data)
        self.add_router("POSTcurrencies",
                        lambda data: self.controler_currencies.add_data(data))
        self.add_router("POSTexchangeRates",
                        lambda data: self.controler_exchage_rates.add_data(data))
        self.add_router(
            "PATCHexchangeRate", self.controler_exchage_rates.patch_data)
