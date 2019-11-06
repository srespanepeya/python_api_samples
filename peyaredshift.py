import psycopg2
from psycopg2.extras import RealDictCursor
import yaml
import json

class PeyaRedshift:

    def __init__(self):
        print("--->Initiating PeyaRedshift Instance...")
        f = open('config.yml')
        params = yaml.load(f,Loader=yaml.BaseLoader)
        f.close()
        self.db_host = params['audit-db']['host']
        self.db_port = params['audit-db']['port']
        self.db_user = params['audit-db']['user']
        self.db_password = params['audit-db']['password']
        self.db_database = params['audit-db']['database']

    def runQuery(self,pQuery):
        try:
            print("--->Connecting to DB...")
            connection = psycopg2.connect(user=self.db_user,
                                          password=self.db_password,
                                          host=self.db_host,
                                          port=self.db_port,
                                          database=self.db_database)
            print("--->Done...")
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            queryToRun = pQuery
            print("<---Running query...")
            cursor.execute(queryToRun)
            print("<---Done...")
            result = cursor.fetchall()
            jResults = result
            return jResults
        except (Exception, psycopg2.Error) as error :
            print ("Error while fetching data from PostgreSQL", error)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
