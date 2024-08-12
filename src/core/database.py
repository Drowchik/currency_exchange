
import sqlite3
from contextlib import contextmanager

from exception import DataBaseError


class ConnectManager:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    @contextmanager
    def get_connection(self):
        connection = sqlite3.connect(self.db_name)
        try:
            yield connection
        except Exception as e:
            raise DataBaseError(str(e))
        finally:
            connection.close()

    @contextmanager
    def get_cursor(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
                connection.commit()
            finally:
                cursor.close()
