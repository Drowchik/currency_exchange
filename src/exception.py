class DatabaseUnavailableError(Exception):
    def __init__(self, message="Internal Server Error: Database is unavailable."):
        self.message = message
        super().__init__(self.message)


class RouteNotFoundError(Exception):
    def __init__(self, message="Route Not Found Error"):
        self.message = message
        super().__init__(self.message)


class MissingFieldError(Exception):
    def __init__(self, message="Missing required field"):
        self.message = message
        super().__init__(self.message)


class CodeNotFoundError(Exception):
    def __init__(self, message="Code Value Not Found Error"):
        self.message = message
        super().__init__(self.message)


class DataBaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CurrencyAlreadyExists(Exception):
    def __init__(self, message="A currency with this code already exists"):
        self.message = message
        super().__init__(self.message)


class ImpossibleСonvert(Exception):
    def __init__(self, message="Conversion rate not found"):
        self.message = message
        super().__init__(self.message)
