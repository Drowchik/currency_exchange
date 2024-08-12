from dto import DTOConverted, DTOCovertedGet
from exception import ImpossibleСonvert


class ServiceConerted:
    def __init__(self, controler, dto_object: DTOConverted) -> None:
        self.dto_object = dto_object
        self.controler_exchage_rates = controler

    def convert_currency(self):
        # 1 случай
        direct_key = f"{self.dto_object.from_value}{self.dto_object.to_value}"
        direct_rate = self.controler_exchage_rates.get_one_data(direct_key)
        if direct_rate:
            return DTOCovertedGet(baseCurrency=direct_rate["baseCurrency"],
                                  targetCurrency=direct_rate["targetCurrency"],
                                  amount=self.dto_object.amount,
                                  rate=direct_rate["rate"],
                                  convertedAmount=round(self.dto_object.amount*direct_rate["rate"], 2)).to_dict()
        # 2 случай
        inverse_key = f"{self.dto_object.to_value}{self.dto_object.from_value}"
        inverse_rate = self.controler_exchage_rates.get_one_data(inverse_key)
        if inverse_rate:
            rate = 1/inverse_rate["rate"]
            return DTOCovertedGet(baseCurrency=inverse_rate["targetCurrency"],
                                  targetCurrency=inverse_rate["baseCurrency"],
                                  amount=self.dto_object.amount,
                                  rate=round(rate, 2),
                                  convertedAmount=round(self.dto_object.amount*rate, 2)).to_dict()
        # 3 случай
        data_usd_to = self.controler_exchage_rates.get_one_data(
            f"USD{self.dto_object.to_value}")
        data_usd_from = self.controler_exchage_rates.get_one_data(
            f"USD{self.dto_object.from_value}")
        if data_usd_to and data_usd_from:
            rate = data_usd_to["rate"]/data_usd_from["rate"]
            return DTOCovertedGet(baseCurrency=data_usd_from["targetCurrency"],
                                  targetCurrency=data_usd_to["targetCurrency"],
                                  amount=self.dto_object.amount,
                                  rate=round(rate, 2),
                                  convertedAmount=round(rate*self.dto_object.amount, 2)).to_dict()
        raise ImpossibleСonvert()
