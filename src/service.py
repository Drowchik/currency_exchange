from dto import DTOConverted, DTOCovertedGet


class ServiceConerted:
    def __init__(self, controler, dto_object: DTOConverted) -> None:
        self.dto_object = dto_object
        self.controler_exchage_rates = controler

    def first_func(self):
        data = self.controler_exchage_rates.get_one_data(
            self.dto_object.from_value+self.dto_object.to_value)
        if data:
            data["amount"] = self.dto_object.amount
            data["convertedAmount"] = self.dto_object.amount*data["rate"]
            return data
        data = self.controler_exchage_rates.get_one_data(
            self.dto_object.to_value+self.dto_object.from_value)
        if data:
            data["amount"] = self.dto_object.amount
            data["rate"] = round(1/data["rate"], 2)
            data["baseCurrency"], data["targetCurrency"] = data["targetCurrency"], data["baseCurrency"]
            data["convertedAmount"] = self.dto_object.amount*data["rate"]
            return data

        data_usd_to = self.controler_exchage_rates.get_one_data(
            "USD"+self.dto_object.to_value)
        data_usd_from = self.controler_exchage_rates.get_one_data(
            "USD"+self.dto_object.from_value)
        if data_usd_to and data_usd_from:
            return DTOCovertedGet(baseCurrency=data_usd_from["targetCurrency"],
                                  targetCurrency=data_usd_to["targetCurrency"],
                                  amount=self.dto_object.amount,
                                  rate=round(
                data_usd_from["rate"]/data_usd_to["rate"], 2),
                convertedAmount=round(data_usd_to["rate"]/data_usd_from["rate"], 2)*self.dto_object.amount).to_dict()
        return '{"message": "all bad"}'
