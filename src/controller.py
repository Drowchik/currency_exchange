from abc import ABC, abstractmethod
from decimal import Decimal
import json
from dto import BaseDTOCurrenciesGet, DTOCurrenciesGet, DTOCurrenciesPOST, DTOExchangeRatesPOST, ExchangeRates
from models import BaseModel


class Controler(ABC):
    def __init__(self, model: BaseModel) -> None:
        self.model = model

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_one_data(self, find_val, value):
        pass

    @abstractmethod
    def add_data(self, data: dict):
        pass


class ControlerCurrencies(Controler):
    def __init__(self, model: BaseModel) -> None:
        super().__init__(model)

    def get_all(self):
        data = self.model.get_all_data()
        return json.dumps([DTOCurrenciesGet(id=item[0],
                                            code=item[1],
                                            name=item[2],
                                            sign=item[3]).to_dict() for item in data])

    def get_one_data(self, value):
        data = self.model.get_one_data(value)
        return DTOCurrenciesGet(id=data[0],
                                code=data[1],
                                name=data[2],
                                sign=data[3]).to_dict()

    def add_data(self, data: dict):
        self.model.insert_data(DTOCurrenciesPOST(data))

    def get_two_data(self, val_one, val_two):
        data = self.model.get_two_data(val_one, val_two)
        target, base = [BaseDTOCurrenciesGet(
            id=val[0], code=val[1]) for val in data]
        return target, base


class ControlerExchageRates(Controler):
    def __init__(self, model: BaseModel) -> None:
        super().__init__(model)

    def get_all(self):
        data_all = self.model.get_all_data()
        list_exchage_rates = []
        for data in data_all:
            base_target_currency = self.create_currency(data)
            list_exchage_rates.append(ExchangeRates(id=data[0],
                                                    base_currency=base_target_currency[1],
                                                    target_currency=base_target_currency[0],
                                                    rate=data[1]).to_dict())
        return json.dumps(list_exchage_rates)

    def get_one_data(self, code_all):
        code_one = code_all[:3]
        code_two = code_all[3:]
        data = self.model.get_one_data(code_one, code_two)
        if data:
            data = data[0]
            base_target_currency = self.create_currency(data)
            return ExchangeRates(id=data[0],
                                 base_currency=base_target_currency[1],
                                 target_currency=base_target_currency[0],
                                 rate=data[1]).to_dict()
        return False

    def add_data(self, rate: Decimal, base: ControlerCurrencies, target: ControlerCurrencies):
        self.model.insert_data(DTOExchangeRatesPOST(
            rate=rate, base=base.id, target=target.id))

    def create_currency(self, data: list):
        target_currency = DTOCurrenciesGet(id=data[2],
                                           code=data[3],
                                           name=data[4],
                                           sign=data[5]).to_dict()
        base_currency = DTOCurrenciesGet(id=data[6],
                                         code=data[7],
                                         name=data[8],
                                         sign=data[9]).to_dict()
        return target_currency, base_currency

    def patch_data(self, target, base, rate):
        self.model.update_data(rate=rate, base_id=base, target_id=target)
