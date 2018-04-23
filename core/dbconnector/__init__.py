import sqlite3
import pymysql
from time import ctime

ISALITE_MYSQL = 1
ISALITE_SQLITE = 2


# 数据库返回结果对象
class DBResult:
    suc = False  # 执行成功与否
    result = None  # 执行结果，通常是查询结果集，一个 list 嵌套 dict 的结构
    error = None  # 异常信息
    rows = None  # 结果条目数量

    # 返回结果集合中指定位置的一条数据
    def index_of(self, index):
        # 判断是否执行成功，是的话接着判断 index 是否为整型，是的话最后再判断 index 是否在有效范围内
        if self.suc and isinstance(index, int) and self.rows > index >= -self.rows:
            # 条件都成立，返回对应下标的结果
            return self.result[index]

        return None

    # 返回结果集合中的第一条数据
    def get_first(self):
        return self.index_of(0)

    # 返回结果集合中的最后一条数据
    def get_last(self):
        return self.index_of(-1)

    @staticmethod
    def print_debug_info(obj, sql, ret):
        if obj.debug:
            print('\033[00;37m/ \033[01;35mSql Statement', sql)
            print('\033[00;37m/ \033[01;31mError:', ret.error) if ret.error is not None else print(
                '\033[00;37m/ \033[01;32mError:', ret.error)
            print('\033[00;37m/ \033[01;33mRows:', ret.rows)
            print('\033[00;37m/ \033[01;36mResult:', ret.result, '\033[00;37m\n')

    @staticmethod
    def capture_sqlite(func):
        def decorator(*args, **options):
            # 实例化
            ret = DBResult()

            cursor = args[0].conn.cursor()

            options['cursor'] = cursor

            # 捕获异常
            try:
                # 为 DBResult 对象的 rows 和 result 成员赋值
                ret.rows, ret.result = func(*args, **options)

                # 关闭游标
                cursor.close()

                # 修改执行状态为 True 表示成功
                ret.suc = True

                if options.get('commit', False):
                    args[0].conn.commit()

            except Exception as e:
                # 如果捕获到异常，将异常放进 DBResult 对象的 error 属性中
                ret.error = e

                if options.get('commit', False):
                    args[0].conn.rollback()

            DBResult.print_debug_info(args[0], options['sql'], ret)

            # 返回 DBResult 对象
            return ret

        # 返回 decorator 方法，其实就相当于返回 DBResult 对象
        return decorator

    @staticmethod
    def capture_mysql(func):
        def decorator(*args, **options):
            # 实例化
            ret = DBResult()

            # 捕获异常
            try:
                # 为 DBResult 对象的 rows 和 result 成员赋值
                ret.rows, ret.result = func(*args, **options)
                # 修改执行状态为 True 表示成功
                ret.suc = True
            except Exception as e:
                print(e)
                # 如果捕获到异常，将异常放进 DBResult 对象的 error 属性中
                ret.error = e
            # 返回 DBResult 对象

            DBResult.print_debug_info(args[0], options['sql'], ret)

            return ret

        # 返回 decorator 方法，其实就相当于返回 DBResult 对象
        return decorator

    def to_dict(self):
        return {
            'suc': self.suc,
            'result': self.result,
            'error': self.error,
            'rows': self.rows
        }


# 数据库模块
class BaseDB:
    # 实例对象初始 方法
    def __init__(self, db_type):
        SQL_ENGINE_MAP = {
            ISALITE_SQLITE: self.__init_sqlite,
            ISALITE_MYSQL: self.__init_mysql
        }

        self.init = SQL_ENGINE_MAP[db_type]

    def __init_sqlite(self, database='', debug=False):
        self.database = database  # 选择的数据库
        self.connect = self.connect_sqlite
        self.conn = self.connect()  # 数据库连接对象
        self.conn.row_factory = BaseDB.dict_factory
        self.debug = debug  # 是否开启调试模式
        self.execute = self.execute_sqlite

        return self

    def __init_mysql(self, user, password, database='', host='127.0.0.1', port=3306, charset='utf8',
                     cursor_class=pymysql.cursors.DictCursor, debug=False):
        self.user = user  # 连接用户
        self.password = password  # 连接用户密码
        self.database = database  # 选择的数据库
        self.host = host  # 主机名，默认 127.0.0.1
        self.port = port  # 端口号，默认 3306
        self.charset = charset  # 数据库编码，默认 UTF-8
        self.cursor_class = cursor_class  # 数据库游标类型，默认为 DictCursor，返回的每一行数据集都是个字典
        self.debug = debug  # 是否开启调试模式
        self.execute = self.execute_mysql
        self.connect = self.connect_mysql
        self.conn = self.connect()  # 数据库连接对象

        return self

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # 建立连接
    def connect_mysql(self):
        # 返回一个数据库连接对象
        return pymysql.connect(host=self.host, user=self.user, port=self.port,
                               passwd=self.password, db=self.database,
                               charset=self.charset, connect_timeout=10,
                               cursorclass=self.cursor_class)

    # 建立连接
    def connect_sqlite(self):
        # 返回一个数据库连接对象
        return sqlite3.connect(self.database, check_same_thread=False)

    # 断开连接
    def close(self):
        # 关闭数据库连接
        self.conn.close()

    # 数 操作，增，删，改，查
    @DBResult.capture_sqlite
    def execute_sqlite(self, **options):

        sql = options['sql'].replace('None', 'NULL')

        if not options['cursor']:
            cursor = self.conn.cursor()
        else:
            cursor = options['cursor']

        params = options.get('params', None)

        # 执行语句并获取影响条目数量
        cursor.execute(sql, params) if params and isinstance(params, dict) else cursor.execute(sql)
        rows = cursor.rowcount

        # 获取执行结果
        if 'INSERT' in sql or 'insert' in sql:
            result = cursor.lastrowid
        else:
            result = cursor.fetchall()

        ######################
        # 关闭数据重连，不要问我为什么要关闭，都是血与泪的教训，防止上一个连接中有未清空读完的数据导致下次复用这个连接会发生一些不可描述的事情
        ######################
        # self.close()

        # 返回影响条目数量和执行结果
        return rows, result

    @DBResult.capture_mysql
    def execute_mysql(self, **options):

        sql = options['sql'].replace('None', 'NULL')

        params = options.get('params', None)

        # 超时重连 MySQL
        try:
            self.conn.ping()

            if self.debug:
                print('/\033[00;37m *********** Database Debug ***********/')
                print('\033[00;37m/ \033[01;34mTime:', ctime())
                print('\033[00;37m/ \033[01;32mPing: Success')
        except:
            if self.debug:
                print('/\033[00;37m *********** Database Debug ***********/')
                print('\033[00;37m/ \033[01;34mTime:', ctime())
                print('\033[00;37m/ \033[01;31mPing: Failure')

            self.conn = self.connect()

        # 获取数据库连接对象上下文
        with self.conn as cursor:
            # 如果参数不为空并且时 Dict 类型时，把 SQL 语句与参数一起传入 execute 中调用，反之直接调用 exevute

            # 执行语句并获取影响条目数量
            rows = cursor.execute(sql, params) if params and isinstance(params, dict) else cursor.execute(sql)

            # 获取执行结果
            # 获取执行结果
            if 'INSERT' in sql or 'insert' in sql:
                result = self.conn.insert_id()
            else:
                result = cursor.fetchall()

        ######################
        # 关闭数据重连，不要问我为什么要关闭，都是血与泪的教训，防止上一个连接中有未清空读完的数据导致下次复用这个连接会发生一些不可描述的事情
        ######################
        self.close()

        # 返回影响条目数量和执行结果
        return rows, result
