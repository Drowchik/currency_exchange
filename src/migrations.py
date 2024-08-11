from core.database import ConnectManager
from core.config import settings


def migration_1(connect: ConnectManager):
    with connect.get_cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Currencies (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Code VARCHAR UNIQUE,
                FullName VARCHAR,
                Sign VARCHAR
            ) 
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExchangeRates (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                BaseCurrencyId INTEGER,
                TargetCurrencyId INTEGER,
                Rate Decimal(6,4),
                FOREIGN KEY(BaseCurrencyId) REFERENCES Currencies(ID),
                FOREIGN KEY(TargetCurrencyId) REFERENCES Currencies(ID)
            ) 
            ''')
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS unique_pair 
            ON ExchangeRates(BaseCurrencyId, TargetCurrencyId)
        ''')


def downgrade_migration(connect: ConnectManager):
    with connect.get_cursor() as cursor:
        cursor.execute('DROP INDEX IF EXISTS unique_pair')
        cursor.execute('DROP TABLE IF EXISTS ExchangeRates')
        cursor.execute('DROP TABLE IF EXISTS Currencies')


if __name__ == "__main__":
    migration_1(ConnectManager(settings.db_name))
