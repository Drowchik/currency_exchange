from decimal import Decimal


class DTOCurrenciesPOST:
    def __init__(self, data: dict) -> None:
        self.code = data.get("code")[0]
        self.name = data.get("name")[0]
        self.sign = data.get("sign")[0]


class DTOExchangeRatesPOST:
    def __init__(self, rate: Decimal, base: int, target: int) -> None:
        self.rate = rate
        self.base = base
        self.target = target


class BaseDTOCurrenciesGet:
    def __init__(self, id: int, code: str) -> None:
        self.id = id
        self.code = code

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code
        }


class DTOCurrenciesGet(BaseDTOCurrenciesGet):

    def __init__(self, id: int, code: str, name: str, sign: str) -> None:
        super().__init__(id, code)
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


class DTOCovertedGet:
    def __init__(self, baseCurrency, targetCurrency, rate, amount, convertedAmount) -> None:
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
        self.amount = amount
        self.convertedAmount = convertedAmount

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
