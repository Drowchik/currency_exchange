from dynaconf import Dynaconf

_settings = Dynaconf(
    settings_file=["configs.yaml"],
)


class Settings:
    def __init__(self, db_name: str = 5) -> None:
        self.db_name: str = db_name


settings = Settings(db_name=_settings.database.name)
