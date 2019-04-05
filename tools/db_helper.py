import pymysql

DB_CONFIC = {
    "host" : "localhost",
    "user" : "root",
    "password":"123456",
    "database":"s8",
    "charset":"utf8"
}

#指定单条语句
def modify(sql,arg=None):
    conn = pymysql.connect(host=DB_CONFIC["host"], user=DB_CONFIC["user"], password=DB_CONFIC["password"], database=DB_CONFIC["database"], charset=DB_CONFIC["charset"])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql, arg)
    conn.commit()
    cursor.close()
    conn.close()

#多次提交，多次连接
def create(sql,arg=None):
    conn = pymysql.connect(host=DB_CONFIC["host"], user=DB_CONFIC["user"], password=DB_CONFIC["password"], database=DB_CONFIC["database"], charset=DB_CONFIC["charset"])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, arg)
    #lastrowid表示插入信息同时获取主键id
    the_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return the_id

#批量的modify
def pl_modify(sql,arg=None):
    conn = pymysql.connect(host=DB_CONFIC["host"], user=DB_CONFIC["user"], password=DB_CONFIC["password"], database=DB_CONFIC["database"], charset=DB_CONFIC["charset"])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #executemany的方法：达到效果为多次连接，一次提交的效果
    #但是executemany对于传入的参数有规定，必须是一个列表或一个元组
    cursor.executemany(sql, arg)
    conn.commit()
    cursor.close()
    conn.close()

#查询单个数据记录
def get_one(sql,arg=None):
    conn = pymysql.connect(host=DB_CONFIC["host"], user=DB_CONFIC["user"], password=DB_CONFIC["password"], database=DB_CONFIC["database"], charset=DB_CONFIC["charset"])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql, arg)
    ret = cursor.fetchone()
    cursor.close()
    conn.close()
    return ret

#查询多个数据记录
def get_list(sql,arg=None):
    conn = pymysql.connect(host=DB_CONFIC["host"], user=DB_CONFIC["user"], password=DB_CONFIC["password"],database=DB_CONFIC["database"], charset=DB_CONFIC["charset"])
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, arg)
    ret = cursor.fetchall()
    cursor.close()
    conn.close()
    return ret



#定义一个DBhelper()类
class DBHelper():
    #初始化方法
    def __init__(self):
        self.conn=None
        self.cursor=None
        #每次启动自动连接
        self.connect()
        #connect,连接方法  ,调用对象的连接方法，就把我们的连接和光标都拿到

    def connect(self):
        self.conn=pymysql.connect(
            host=DB_CONFIC["host"],
            user=DB_CONFIC["user"],
            password=DB_CONFIC["password"],
            database=DB_CONFIC["database"],
            charset=DB_CONFIC["charset"]
        )
        #光标的方法
        self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)


    # 指定单条语句
    def modify(self,sql, arg=None):
        self.cursor.execute(sql, arg)
        self.conn.commit()


    # 多次提交，多次连接
    def create(self,sql, arg=None):
        self.cursor.execute(sql, arg)
        # lastrowid表示插入信息同时获取主键id
        the_id = self.cursor.lastrowid
        self.conn.commit()
        return the_id

    # 批量的modify
    def pl_modify(self,sql, arg=None):
        self.cursor.executemany(sql, arg)
        self.conn.commit()


    # 查询单个数据记录
    def get_one(self,sql, arg=None):
        self.cursor.execute(sql, arg)
        ret = self.cursor.fetchone()
        return ret

    # 查询多个数据记录
    def get_list(self,sql, arg=None):
        self.cursor.execute(sql, arg)
        ret = self.cursor.fetchall()
        return ret

     #关闭的操作，关闭函数，自动关闭
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 进入with语句自动执行
    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()






#绑定实例化对象，可调取init函数
db = DBHelper()

