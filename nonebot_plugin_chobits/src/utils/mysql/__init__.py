"""
MySQL 数据库操作
    效果: 对数据库的增删改查

configure: MySql 工具类的配置设置
create_connection: 创建 MySql 连接话柄
create_field_string: 创建字段位置字符串,用于保存生成 SQL
create_variable_string: 创建变量变量字符串,用于保存生成 SQL
create_key_value_pair: 创建键值对字符串,用于编辑生成 SQL
create_where_clause: 创建where子句,用于条件 SQL
create_order_by_clause: 生成排序SQL语句,用于查询排序 SQL
create_table: 创建表
insert: 保存数据
insert_all: 批量保存数据
delete: 删除数据
update: 更新数据
select: 查询数据
select_column: 查询数据,返回带键名格式
find_info: 查询一条数据
has_info: 查询信息是否存在

使用类库:
    MySQL Connector:
        安装: pip install mysql-connector
"""
import mysql.connector
import nonebot
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


class MySql:
    """
    数据库配置
    """
    host = "localhost"
    port = 3306
    user = None
    password = None
    database = None
    """
    数据库连接
    """
    connection = None

    def __init__(self):
        """
        初始化 MySQL
        """
        flag = self.configure()
        if flag:
            self.connection = self.create_connection()
            if self.connection is None:
                # 抛出异常
                raise Exception("创建连接失败")
        else:
            # 抛出异常
            raise Exception("请查看MYSQL配置信息")

    def __str__(self) -> str:
        """
        返回 MySQL 配置信息
        """
        return f"Redis({self.host}:{self.port})"

    def __del__(self):
        """
        销毁MySQL
        """
        if self.connection:
            self.connection.close()

    def configure(self) -> bool:
        """
        配置MySQL
        """
        if hasattr(nonebot.get_driver().config, "chobits_mysql"):
            config = nonebot.get_driver().config.chobits_mysql
            if "host" in config:
                self.host = config['host']
            else:
                print("未配置MySQL host")
                return False
            if "port" in config:
                self.port = config['port']
            if "user" in config:
                self.user = config['user']
            else:
                print("未配置MySQL user")
                return False
            if "password" in config:
                self.password = config['password']
            else:
                print("未配置MySQL password")
                return False
            if "database" in config:
                self.database = config['database']
            else:
                print("未配置MySQL database")
                return False
            print("已配置MySQL")
            return True
        else:
            print("未配置MySQL")
            return False

    def create_connection(self) -> PooledMySQLConnection | MySQLConnectionAbstract:
        """
        创建并返回数据库连接
        """
        # 建立连接
        return mysql.connector.connect(
            raise_on_warnings=True,
            autocommit=False,
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
        )

    @staticmethod
    def create_field_string(data) -> str:
        """
        创建字段字符串
        """
        field_string = ""
        for index, row in enumerate(data):
            if index:
                field_string += ', '
            field_string += f"`{row}`"
        return field_string

    @staticmethod
    def create_variable_string(data) -> str:
        """
        创建变量字符串
        """
        variable_string = ""
        for index, row in enumerate(data):
            if index:
                variable_string += ', '
            if data[row] == 'NULL':
                variable_string += 'NULL'
            else:
                variable_string += f"'{data[row]}'"
        return variable_string

    @staticmethod
    def create_key_value_pair(data) -> str:
        """
        创建键值对字符串
        """
        key_value_pair = ""
        for index, row in enumerate(data):
            if index:
                key_value_pair += ', '
            if data[row] == 'NULL':
                key_value_pair += f"`{row}` = NULL"
            else:
                key_value_pair += f"`{row}` = '{data[row]}'"
        return key_value_pair

    @staticmethod
    def create_where_clause(where_list) -> str:
        """
        创建where子句
        """
        if where_list:
            where_clause = " WHERE "
            for index, key in enumerate(where_list):
                if index:
                    where_clause += ' AND '
                if type(where_list[key]) is list:
                    if len(where_list[key]) == 2:
                        where_clause += f"`{key}` {where_list[key][0]} "
                        if where_list[key][0] == 'between':
                            where_clause += f" '{where_list[key][1][0]}' AND '{where_list[key][1][1]}' "
                        elif where_list[key][0] == 'like':
                            where_clause += f" '%{where_list[key][1]}%' "
                        elif where_list[key][0] == 'in':
                            where_clause += " ('" + "', '".join([str(item) for item in where_list[key][1]]) + "') "
                        else:
                            where_clause += f" '{where_list[key][1]}' "
                else:
                    if where_list[key] == 'NULL':
                        where_clause += f"`{key}` IS NULL"
                    else:
                        where_clause += f"`{key}` = '{where_list[key]}'"
            return where_clause
        else:
            return ""

    @staticmethod
    def create_order_by_clause(order_list):
        """
        生成排序SQL语句
        """
        if order_list:
            order_by_clause = ' ORDER BY '
            for key, value in order_list.items():
                order_by_clause += f'`{key}` {value}, '
            order_by_clause = order_by_clause[:-2]
            return order_by_clause
        else:
            return ''

    def create_table(self, sql) -> bool:
        """
        创建表
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
            print("创建表成功")
            return True
        except mysql.connector.Error as e:
            # 回滚事务
            connection.rollback()
            print(e)
            return False
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def insert(self, table, data) -> int | bool:
        """
        保存数据
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "INSERT INTO `" + table + "` (" + self.create_field_string(data) + ") VALUES (" + self.create_variable_string(data) + ")"
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
            # 获取新插入行的ID
            last_row_id = cursor.lastrowid
            print("保存数据成功")
            return last_row_id
        except mysql.connector.Error as e:
            # 回滚事务
            connection.rollback()
            print(e)
            return False
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def insert_all(self, table, data) -> int | bool:
        """
        批量保存数据
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 初始化SQL语句
            sql = "INSERT INTO `" + table + "` (" + self.create_field_string(data[0]) + ") VALUES "
            # 循环遍历数据
            for index, row in enumerate(data):
                if index:
                    sql += ', '
                sql += "(" + self.create_variable_string(row) + ")"
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
            # 获取新插入行的ID
            last_row_id = cursor.lastrowid
            print("保存数据成功")
            return last_row_id
        except mysql.connector.Error as e:
            # 回滚事务
            connection.rollback()
            print(e)
            return False
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def delete(self, table, where) -> bool:
        """
        删除数据
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "DELETE FROM `" + table + "`" + self.create_where_clause(where)
            print(sql)
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
            print("删除数据成功")
            return True
        except mysql.connector.Error as e:
            # 回滚事务
            connection.rollback()
            print(e)
            return False
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def update(self, table, data, where) -> bool:
        """
        更新数据
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "UPDATE `" + table + "` SET " + self.create_key_value_pair(data) + self.create_where_clause(where)
            print(sql)
            # 执行SQL语句
            cursor.execute(sql)
            # 提交事务
            connection.commit()
            print("更新数据成功")
            return True
        except mysql.connector.Error as e:
            # 回滚事务
            connection.rollback()
            print(e)
            return False
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def select(self, table, where=None, order=None, limit=None) -> list | None:
        """
        查询数据
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "SELECT * FROM `" + table + "`" + self.create_where_clause(where)
            # 执行SQL语句
            cursor.execute(sql)
            # 获取查询结果
            result = cursor.fetchall()
            print("查询数据成功")
            return result
        except mysql.connector.Error as e:
            print(e)
            return None
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def select_column(self, table, where=None, order=None, limit=None) -> list | None:
        """
        查询数据,返回带键名格式
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "SELECT * FROM `" + table + "`" + self.create_where_clause(where) + self.create_order_by_clause(order)
            # 执行SQL语句
            cursor.execute(sql)
            # 获取查询结果的列名
            column_names = cursor.description
            # 获取查询结果
            result = cursor.fetchall()
            # 合并字段名
            all_result = []
            for row in result:
                info = {}
                for index, cell in enumerate(row):
                    info[column_names[index][0]] = cell
                all_result.append(info)
            print("查询数据成功")
            return all_result
        except mysql.connector.Error as e:
            print(e)
            return None
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def find_info(self, table, where=None) -> dict | None:
        """
        查询一条数据
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "SELECT * FROM `" + table + "`" + self.create_where_clause(where)
            print(sql)
            # 执行SQL语句
            cursor.execute(sql)
            # 获取查询结果的列名
            column_names = cursor.description
            # 获取查询结果
            result = cursor.fetchall()
            if len(result) <= 0:
                return None
            # 合并字段名
            all_result = []
            for row in result:
                info = {}
                for index, cell in enumerate(row):
                    info[column_names[index][0]] = cell
                all_result.append(info)
            print("查询数据成功")
            return all_result[0]
        except mysql.connector.Error as e:
            print(e)
            return None
        finally:
            # 关闭游标
            if cursor is not None:
                cursor.close()
                print("关闭游标")
            # 关闭连接
            if connection.is_connected():
                connection.close()
                print("关闭连接")

    def has_info(self, table, where=None) -> bool:
        """
        查询信息是否存在
        """
        info_list = self.select(table, where)
        if len(info_list):
            return True
        else:
            return False

    def get_count(self, table, where=None) -> int:
        """
        获取数据总数
        """
        # 创建连接
        connection = self.connection
        # 声明游标
        cursor = None
        try:
            # 创建游标
            cursor = connection.cursor()
            # 创建SQL语句
            sql = "SELECT COUNT(*) FROM `" + table + "`" + self.create_where_clause(where)
            # 执行SQL语句
            cursor.execute(sql)
            # 获取查询结果
            result = cursor.fetchall()
            print("查询数据成功")
            return result[0][0]
        except mysql.connector.Error as e:
            print(e)
            return 0
