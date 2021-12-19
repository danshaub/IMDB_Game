import mysql.connector
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import pickle

class db_operations():

    def __init__(self, key_path):  # constructor with connection path to db

        info = self.parse_key(key_path)
        self.connection = mysql.connector.connect(
            host=info["host"],
            user=info["user"],
            password=info["password"],
            database=info["database"])
        self.cursor = self.connection.cursor()
        
        self.driver = GraphDatabase.driver(
            info['n_uri'], auth=(info['n_user'], info['n_password']))
    
        print("connection made..")

    def parse_key(self, key_path):
        info = {}
        with open(key_path, 'r') as f:
            info["host"] = f.readline().strip()
            info["user"] = f.readline().strip()
            info["password"] = f.readline().strip()
            info["database"] = f.readline().strip()
            info["n_uri"] = f.readline().strip()
            info["n_user"] = f.readline().strip()
            info["n_password"] = f.readline().strip()
        return info

    @staticmethod
    def run_depth_query(tx, startNodeID, depth):
        query = '''
            MATCH (n)
            WHERE n.id = $startNodeID
            WITH $depth AS maxLevel,n
            CALL apoc.path.spanningTree(n, {relationshipFilter: "COSTARS_WITH", minLevel:1, maxLevel:maxLevel, bfs:TRUE}) 
            YIELD path
            WITH COLLECT(path) AS paths,n,maxLevel
            WITH [p IN paths WHERE length(p) = maxLevel] AS maxPaths,n
            WITH [p IN maxPaths | LAST(NODES(p))] as lastNodes,n
            RETURN lastNodes
        ''' 
        result = tx.run(query, startNodeID=startNodeID, depth=depth)
        
        try:
            return result.single()[0]
        except ServiceUnavailable as exception:
            print("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def run_shortest_path_query(tx, startNodeID=int, endNodeID=int):
        query = '''
                MATCH (p1:Person),(p2:Person)
                WHERE p1.id = $startNodeID AND p2.id = $endNodeID
                WITH shortestPath((p1)-[:COSTARS_WITH*]-(p2)) as p
                RETURN length(p)
        '''
        result = tx.run(query, startNodeID=startNodeID, endNodeID=endNodeID)
        
        try:
            return result.single()[0]
        except ServiceUnavailable as exception:
            print("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
                

    def get_nodes_at_depth(self, startNodeID, depth):
        with self.driver.session() as session:
            result = session.read_transaction(db_operations.run_depth_query, startNodeID, depth)
            return result

    def calculate_optimal_score(self, startNodeID, endNodeID):
        with self.driver.session() as session:
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
