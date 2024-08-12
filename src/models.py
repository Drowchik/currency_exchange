import sqlite3
from abc import ABC, abstractmethod

from core.database import ConnectManager
from dto import DTOCurrenciesPOST, DTOExchangeRatesPOST


class BaseModel(ABC):
    def __init__(self, coonect_manager: ConnectManager) -> None:
        self.connect_manager = coonect_manager

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
    def __init__(self, coonect_manager: ConnectManager) -> None:
        super().__init__(coonect_manager)

    def insert_data(self, dto: DTOCurrenciesPOST):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute(
                'INSERT INTO Currencies (code, FullName, Sign) VALUES (?, ?, ?)', (dto.code, dto.name, dto.sign))

    def get_all_data(self):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute('SELECT * FROM Currencies')
            return cursor.fetchall()

    def get_one_data(self, value: str):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute(
                'SELECT * FROM Currencies WHERE Code = ?', (value,))
            return cursor.fetchone()

    def get_two_data(self, one_val: str, two_val: str):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute('''SELECT cur.id, cur.Code
                                FROM Currencies cur
                                WHERE cur.Code = ? OR cur.Code=?''', (one_val, two_val))
            return cursor.fetchall()


class ExchangeRates(BaseModel):
    def __init__(self, coonect_manager: ConnectManager) -> None:
        super().__init__(coonect_manager)

    def insert_data(self, dto: DTOExchangeRatesPOST):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute(
                '''INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
                    SELECT 
                        (SELECT id FROM Currencies WHERE code = ?),
                        (SELECT id FROM Currencies WHERE code = ?),
                        ?
                    WHERE
                        EXISTS (SELECT 1 FROM Currencies WHERE code = ?)
                        AND EXISTS (SELECT 1 FROM Currencies WHERE code = ?);
                    ''', (dto.base, dto.target, dto.rate, dto.base, dto.target))

    def get_all_data(self):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute('''SELECT er.ID,
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
            return cursor.fetchall()

    def get_one_data(self, code_one, code_two):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute('''SELECT er.ID,
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
            return cursor.fetchall()

    def update_data(self, rate, base_сode, target_code):
        with self.connect_manager.get_cursor() as cursor:
            cursor.execute(
                '''UPDATE ExchangeRates
                    SET Rate = ?
                    WHERE BaseCurrencyId = (
                        SELECT id FROM Currencies WHERE code = ?
                    )
                    AND TargetCurrencyId = (
                        SELECT id FROM Currencies WHERE code = ?
                    );''', (rate, base_сode, target_code))
