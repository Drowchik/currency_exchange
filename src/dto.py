from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DTOExchangeRatesPOST:
    rate: Decimal
    base: int
    target: int


@dataclass
class BaseDTOCurrenciesGet:
    id: int
    code: str

    def to_dict(self):
        return self.__dict__


@dataclass
class DTOCurrenciesGet(BaseDTOCurrenciesGet):
    name: str
    sign: str

    def to_dict(self):
        return self.__dict__


@dataclass
class ExchangeRates:
    id: int
    base_currency: DTOCurrenciesGet
    target_currency: DTOCurrenciesGet
    rate: Decimal

    def to_dict(self):
        return {
            "id": self.id,
            "baseCurrency": self.base_currency,
            "targetCurrency": self.target_currency,
            "rate": self.rate
        }


@dataclass
class DTOCovertedGet:
    baseCurrency:  DTOCurrenciesGet
    targetCurrency:  DTOCurrenciesGet
    rate: Decimal
    amount: int
    convertedAmount: Decimal

    def to_dict(self):
        return {
            "baseCurrency": self.baseCurrency,
            "targetCurrency": self.targetCurrency,
            "rate": self.rate,
            "amount": self.amount,
            "convertedAmount": self.convertedAmount,
        }


class DTOConverted:
    def __init__(self, query: dict) -> None:
        self.from_value = query["from"][0]
        self.to_value = query["to"][0]
        self.amount = float(query["amount"][0])


class DTOCurrenciesPOST:
    def __init__(self, data: dict) -> None:
        self.code = data.get("code")[0]
        self.name = data.get("name")[0]
        self.sign = data.get("sign")[0]
