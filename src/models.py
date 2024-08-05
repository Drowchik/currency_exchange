from abc import ABC, abstractmethod
import sqlite3


class BaseModel(ABC):
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    @abstractmethod
    def insert_data(self):
        pass


class Currencies(BaseModel):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Currencies (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Code VARCHAR UNIQUE,
                FullName VARCHAR,
                Sign VARCHAR
            ) 
            ''')
        self.connection.commit()

    def insert_data(self, ):
        self.cursor.execute(
            'INSERT INTO Currencies (code, FullName, Sign) VALUES (?, ?, ?)')


class ExchangeRates(BaseModel):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExchangeRates (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                BaseCurrencyId INTEGER,
                TargetCurrencyId INTEGER,
                Rate Decimal(6,4),
                FOREIGN KEY(BaseCurrencyId) REFERENCES Currencies(ID),
                FOREIGN KEY(TargetCurrencyId) REFERENCES Currencies(ID)
            ) 
            ''')
        self.cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS unique_pair 
            ON ExchangeRates(BaseCurrencyId, TargetCurrencyId)
        ''')
        self.connection.commit()
