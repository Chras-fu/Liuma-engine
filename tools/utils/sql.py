import pymssql as mssql
import pymysql as mysql
import psycopg2 as pgsql
import cx_Oracle as oracle


class SQLConnect:

    def __init__(self, tpz, host, port, db, user, password):
        self.tpz = tpz
        self.host = host
        self.port = int(port)
        self.db = db
        self.user = user
        self.pwd = password
        self.conn = None

    def connect(self):
        """得到连接信息"""
        if self.tpz == "mysql":
            self.conn = mysql.connect(host=self.host, user=self.user,
                                      password=self.pwd, database=self.db, port=self.port, charset='utf8')
        elif self.tpz == "mssql":
            self.conn = mssql.connect(server=self.host, user=self.user,
                                      password=self.pwd, database=self.db, port=self.port, charset='utf8')
        elif self.tpz == "pgsql":
            self.conn = pgsql.connect(host=self.host, user=self.user,
                                      password=self.pwd, database=self.db, port=self.port)
        elif self.tpz == "oracle":
            try:
                self.conn = oracle.connect(self.user, self.pwd, f"{self.host}:{self.port}/{self.db}")
            except:
                sn = oracle.makedsn(self.host, self.port, sid=self.db)
                self.conn = oracle.connect(self.user, self.pwd, sn)
        else:
            raise TypeError("不支持的数据库类型")
        cur = self.conn.cursor()
        if not cur:
            raise RuntimeError("连接数据库失败")
        else:
            return cur

    def query(self, sql):
        """执行查询语句"""
        cur = self.connect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def exec(self, sql):
        """执行非查询语句"""
        cur = self.connect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()