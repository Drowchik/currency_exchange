class DatabaseUnavailableError(Exception):
    def __init__(self, message="Internal Server Error: Database is unavailable."):
        self.message = message
        super().__init__(self.message)


class RouteNotFoundError(Exception):
    def __init__(self, message="Route Not Found Error"):
        self.message = message
        super().__init__(self.message)
