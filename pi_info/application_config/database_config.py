class DatabaseConfig(object):
    def __init__(self, username, password, host, database) -> None:
        self.database = database
        self.host = host
        self.password = password
        self.username = username
