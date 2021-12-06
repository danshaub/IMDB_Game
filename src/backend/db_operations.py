import mysql.connector


class db_connector():
    # initialize connection and cursor
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        print("connection made...")

class db_dql():
    def __init__(self) -> None:
        pass

class db_dml():
    def __init__(self) -> None:
        pass
