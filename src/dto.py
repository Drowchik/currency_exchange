from decimal import Decimal


class DTOCurrenciesPOST:
    def __init__(self, data: dict) -> None:
        self.code = data.get("code")[0]
        self.name = data.get("name")[0]
        self.sign = data.get("sign")[0]


class DTOCurrenciesGet:

    def __init__(self, id: int, code: str, name: str, sign: str) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.sign = sign

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "code": self.code,
                "sign": self.sign
                }


class ExchangeRates:

    def __init__(self, id: int, base_currency: DTOCurrenciesGet, target_currency: DTOCurrenciesGet, rate: Decimal) -> None:
        self.id = id
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.rate = rate

    def to_dict(self):
        return {"id": self.id,
                "baseCurrency": self.base_currency,
                "targetCurrency": self.target_currency,
                "rate": self.rate
                }
