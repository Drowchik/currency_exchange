from models import Currencies, ExchangeRates


if __name__ == "__main__":
    db_name = 'currency.db'

    currencies = Currencies(db_name)

    exchange_rates = ExchangeRates(db_name)
