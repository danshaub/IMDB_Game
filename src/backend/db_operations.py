import mysql.connector
from neo4j import GraphDatabase
import pickle

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
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Password123"))

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

    @staticmethod
    def run_depth_query(tx, startNodeID=int, depth=int):
        result = tx.run('''
            MATCH (n)
            WHERE n.id = $startNodeID
            WITH $depth AS maxLevel,n
            CALL apoc.path.spanningTree(n, {relationshipFilter: "COSTARS_WITH", minLevel:1, maxLevel:maxLevel, bfs:TRUE}) 
            YIELD path
            WITH COLLECT(path) AS paths,n,maxLevel
            WITH [p IN paths WHERE length(p) = maxLevel] AS maxPaths,n
            WITH [p IN maxPaths | LAST(NODES(p))] as lastNodes,n
            RETURN lastNodes
        ''', startNodeID=startNodeID, depth=depth)
        return result.single()[0]

    def run_shortest_path_query(tx, startNodeID=int, endNodeID=int):
            result = tx.run('''
                MATCH (p1:Person),(p2:Person)
                WHERE p1.id = $startNodeID AND p2.id = $endNodeID
                WITH shortestPath((p1)-[:COSTARS_WITH*]-(p2)) as p
                RETURN length(p)
            ''', startNodeID=startNodeID, endNodeID=endNodeID)
            return result.single()[0]

    def get_nodes_at_depth(self, startNodeID, depth):
        with self.driver.session(database="costars") as session:
            result = session.read_transaction(db_operations.run_depth_query, startNodeID, depth)
            return result

    def calculate_optimal_score(self, startNodeID, endNodeID):
        with self.driver.session(database="costars") as session:
            result = session.read_transaction(db_operations.run_shortest_path_query, startNodeID, endNodeID)
            return result

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

    def commit_transation(self):
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()

    def destructor(self):
        self.connection.close()
        self.driver.close()
