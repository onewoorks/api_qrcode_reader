import os, pymysql
from dotenv import load_dotenv
load_dotenv()

class Models:

    def MySqlExecuteQuery(self, query):
        db = pymysql.connect(
            host=os.getenv('DB_MYSQL_HOST'),
            port=int(os.getenv('DB_MYSQL_PORT')),
            user=os.getenv('DB_MYSQL_USER'),
            password=os.getenv('DB_MYSQL_PASS'),
            db=os.getenv('DB_MYSQL_DATABASE'),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,)
        cursor = db.cursor()
        cursor.execute(query)
        data    = cursor.fetchall()
        cursor.close()
        return data
    
    def MysqlInsertQuery(self, query):
        db = pymysql.connect(
            host=os.getenv('DB_MYSQL_HOST'),
            port=int(os.getenv('DB_MYSQL_PORT')),
            user=os.getenv('DB_MYSQL_USER'),
            password=os.getenv('DB_MYSQL_PASS'),
            db=os.getenv('DB_MYSQL_DATABASE'),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            local_infile=1)
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()