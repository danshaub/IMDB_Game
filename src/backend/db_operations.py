import mysql.connector


class db_operations():
    # initialize connection and cursor
    # def __init__(self, host, user, password, database):
    #     self.connection = mysql.connector.connect(
    #         host=host,
    #         user=user,
    #         password=password,
    #         database=database
    #     )
    #     self.cursor = self.connection.cursor()
    #     print("connection made...")

    def __init__(self, key_path):  # constructor with connection path to db
        info = self.parse_key(key_path)
        self.connection = mysql.connector.connect(
            host=info["host"],
            user=info["user"],
            password=info["password"],
            database=info["database"])
        self.cursor = self.connection.cursor()
        print("connection made..")

    def parse_key(self, key_path):
        info = {}
        with open(key_path, 'r') as f:
            info["host"] = f.readline()[0:-1]
            info["user"] = f.readline()[0:-1]
            info["password"] = f.readline()[0:-1]
            info["database"] = f.readline()
        return info

    # function to return a single value from table
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def call_proc(self, proc_name, args=()):
        self.cursor.callproc(proc_name, args)
        results = []
        for result in self.cursor.stored_results():
            results.append(result.fetchall())
        return results

    def insert_game(self, game_tuple):
        query = '''
        INSERT INTO Game (Player, Starter, Ender, GamePath)
        VALUES :
        '''

        self.cursor.execute(query, game_tuple)


    def destructor(self):
        self.connection.close()