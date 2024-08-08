from abc import ABC, abstractmethod
import sqlite3

from dto import DTOCurrenciesPOST, DTOExchangeRatesPOST


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
    def get_one_data(self, value):
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

    def get_one_data(self, value: str):
        self.cursor.execute(
            'SELECT * FROM Currencies WHERE Code = ?', (value,))
        return self.cursor.fetchone()

    def get_two_data(self, one_val: str, two_val: str):
        self.cursor.execute('''SELECT cur.id, cur.Code
                                FROM Currencies cur
                                WHERE cur.Code = ? OR cur.Code=?''', (one_val, two_val))

        return self.cursor.fetchall()


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

    def insert_data(self, dto: DTOExchangeRatesPOST):
        self.cursor.execute(
            'INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)', (dto.base, dto.target, dto.rate))
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

    def update_data(self, rate, base_id, target_id):
        self.cursor.execute(
            'UPDATE ExchangeRates SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?', (rate, base_id, target_id))
        self.connection.commit()
