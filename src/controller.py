import json
from abc import ABC, abstractmethod
from decimal import Decimal

from dto import (BaseDTOCurrenciesGet, DTOConverted, DTOCurrenciesGet,
                 DTOCurrenciesPOST, DTOExchangeRatesPOST, ExchangeRates)
from exception import (CodeNotFoundError, DatabaseUnavailableError,
                       MissingFieldError)
from models import BaseModel
from service import ServiceConerted


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
        try:
            data = self.model.get_all_data()
        except DatabaseUnavailableError() as e:
            return {"message": f"str(e)"}
        return [DTOCurrenciesGet(id=item[0],
                                 code=item[1],
                                 name=item[2],
                                 sign=item[3]).to_dict() for item in data]

    def get_one_data(self, value: str):
        data = self.model.get_one_data(value)
        if not data:
            raise CodeNotFoundError()
        return DTOCurrenciesGet(id=data[0],
                                code=data[1],
                                name=data[2],
                                sign=data[3]).to_dict()

    def add_data(self, data: dict):
        try:
            dto_object = DTOCurrenciesPOST(data)
        except Exception as e:
            raise MissingFieldError(str(e))
        self.model.insert_data(dto_object)


class ControlerExchageRates(Controler):
    def __init__(self, model: BaseModel) -> None:
        super().__init__(model)

    def get_all(self):
        try:
            data_all = self.model.get_all_data()
            list_exchage_rates = []
            for data in data_all:
                base_target_currency = self.create_currency(data)
                list_exchage_rates.append(ExchangeRates(id=data[0],
                                                        base_currency=base_target_currency[1],
                                                        target_currency=base_target_currency[0],
                                                        rate=data[1]).to_dict())
            return list_exchage_rates
        except DatabaseUnavailableError() as e:
            return {"message": f"str(e)"}

    def get_one_data(self, code_all: str):
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
        raise CodeNotFoundError()

    def add_data(self, data: dict):
        self.model.insert_data(DTOExchangeRatesPOST(
            rate=data.get("rate")[0], base=data.get("baseCurrencyCode")[0], target=data.get("targetCurrencyCode")[0]))

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

    def patch_data(self, rate: dict, target_base: str):
        target_base = target_base.split('/')[2]
        self.model.update_data(rate=rate.get(
            "rate")[0], base_сode=target_base[:3], target_code=target_base[3:6])

    def converted_data(self, query_params: dict):
        dto_object = DTOConverted(query_params)
        result = ServiceConerted(self, dto_object)
        return result.convert_currency()
