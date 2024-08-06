from abc import ABC, abstractmethod
import sqlite3

from dto import DTOCurrenciesPOST


class BaseModel(ABC):
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    @abstractmethod
    def insert_data(self):
        pass

    @abstractmethod
    def get_all_data(self):
        pass

    @abstractmethod
    def get_one_data(self, find_one, find_two):
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

    def insert_data(self, dto: DTOCurrenciesPOST):
        self.cursor.execute(
            'INSERT INTO Currencies (code, FullName, Sign) VALUES (?, ?, ?)', (dto.code, dto.name, dto.sign))
        self.connection.commit()

    def get_all_data(self):
        self.cursor.execute('SELECT * FROM Currencies')
        return self.cursor.fetchall()

    def get_one_data(self, find_val: str, value: str):
        self.cursor.execute(
            f'SELECT * FROM Currencies WHERE {find_val} = ?', (value,))
        return self.cursor.fetchone()


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

    def insert_data(self, BaseCurrencyId, TargetCurrencyId, Rate):
        self.cursor.execute(
            'INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)', (BaseCurrencyId, TargetCurrencyId, Rate))
        self.connection.commit()

    def get_all_data(self):
        self.cursor.execute('''SELECT er.ID,
                                      er.Rate,
                                      cur.ID,
                                      cur.Code,
                                      cur.FullName,
                                      cur.Sign,
                                      Curs.ID,
                                      Curs.Code,
                                      Curs.FullName,
                                      Curs.Sign
                            FROM ExchangeRates er
                            JOIN Currencies Cur
                            ON er.TargetCurrencyId = Cur.ID
                            JOIN Currencies Curs
                            ON er.BaseCurrencyId = Curs.ID''')
        return self.cursor.fetchall()

    def get_one_data(self, code_one, code_two):
        self.cursor.execute('''SELECT er.ID,
                                    er.Rate,
                                    cur.ID,
                                    cur.Code,
                                    cur.FullName,
                                    cur.Sign,
                                    Curs.ID,
                                    Curs.Code,
                                    Curs.FullName,
                                    Curs.Sign
                            FROM ExchangeRates er
                            JOIN Currencies Cur
                            ON er.TargetCurrencyId = Cur.ID
                            JOIN Currencies Curs
                            ON er.BaseCurrencyId = Curs.ID
                            WHERE Cur.Code = ? AND Curs.Code=?                            
                            ''', (code_two, code_one))
        return self.cursor.fetchall()
