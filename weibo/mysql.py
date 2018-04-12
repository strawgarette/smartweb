#!/usr/bin/python
#coding=utf-8


"""
https://pypi.python.org/pypi/mysqlclient
https://mysqlclient.readthedocps.io/en/latest/
http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
希望把此文件封装成笔者最方便使用的python操作mysql的库
"""
'''
import MySQLdb


class MySqlTest(object):

    def __init__(self,):
        self.con = None

    def get_conn(self):
        """ 获取连接 """
        try:
            self.con = MySQLdb.connect(
                host="120.25.147.9",
                port=3306,
                user="moonstar",
                passwd="979897757",
                db="moonstar",
                charset='utf8')
        except MySQLdb.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
        return self.con

    def close_con(self):
        """ 关闭连接 """
        if self.con:
            self.con.close()
            print('connection closed.')

    def get_list(self):
        """ 获取所有数据 """
        # 获取连接
        con = self.get_conn()
        # 准备SQL
        sql = 'SELECT * FROM `news`;'
        # 执行SQL
        cursor = con.cursor()
        try:
            rest = cursor.execute(sql)
            print(rest)
            # 打印结果
            rows = cursor.fetchall()
            print(cursor.description)
            for row in rows:
                print(row)
        except MySQLdb.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
        # 关闭连接
        self.close_con()

    def get_one(self):
        """ 获取一条数据记录 """
        # 获取连接
        con = self.get_conn()
        # 准备SQL
        sql = 'SELECT * FROM `news`;'
        # 执行SQL
        cursor = con.cursor()
        try:
            rest = cursor.execute(sql)
            print(rest)
            # 打印结果
            data = cursor.fetchone()
            print(cursor.description)
            print(data)
        except MySQLdb.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
        # 关闭连接
        self.close_con()

    def insert_one(self):
        """ 插入数据 """
        # 获取连接
        con = self.get_conn()
        # 准备SQL
        sql = "INSERT INTO `news`(`title`, `content`, `created_at`, `updated_at`) VALUES ('标题V', '内容3', now(), now());"
        # 执行SQL
        cursor = con.cursor()
        try:
            rest = cursor.execute(sql)
            con.commit()
            # 打印结果
            print(rest)
        except MySQLdb.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
        # 关闭连接
        self.close_con()

    def insert_cus(self, *args):
        """ 自定义插入 """
        # 获取连接
        con = self.get_conn()
        # 准备SQL
        sql = "INSERT INTO `news`(`title`, `content`, `created_at`, `updated_at`) VALUES (%s, %s, now(), now());"
        # 执行SQL
        cursor = con.cursor()
        try:
            rest = cursor.execute(sql, args)
            con.commit()
            # 打印结果
            print(rest)
        except MySQLdb.Error as e:
            print ("Error %d: %s" % (e.args[0], e.args[1]))
        # 关闭连接
        self.close_con()

    def delete_one(self, pk):
        """ 删除一条数据 """
        # 获取连接
        con = self.get_conn()
        # 准备SQL
        sql = "DELETE FROM `news` WHERE `id` = %s;"
        # 执行SQL
        cursor = con.cursor()
        rest = cursor.execute(sql, (pk, ))
        con.commit()
        # 打印结果
        print(rest)
        # 关闭连接
        self.close_con()


def main():
    obj = MySqlTest()
    # obj.insert_one()
    # obj.get_list()
    # obj.get_one()
    # obj.insert_cus("标题NN", "内容XXX")
    #obj.delete_one(2)

if __name__ == '__main__':
    main()


'''

#import MySQLdb python2环境下的库
import pymysql



class MoonMysql(object):

    def get_conn(self):
        # 打开数据库连接
        db = pymysql.connect('120.25.147.9', 'moonstar', '979897757', 'moonstar')


        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()

        print ("Database version : %s " % data)

        # 关闭数据库连接
        db.close()




    def creat_table():
        # 打开数据库连接
        db = pymysql.connect('119.23.237.255', 'user1', 'user1', 'web_data')
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("DROP TABLE IF EXISTS CONTROL")
        
        # 使用预处理语句创建表
        sql_USER = """CREATE TABLE USER (
                FIRST_NAME  CHAR(20) NOT NULL,
                LAST_NAME  CHAR(20),
                AGE INT,
                Phone CHAR(20),  
                SEX CHAR(1),
                INCOME FLOAT )"""
        
        
        # 使用预处理语句创建表
        TIME = """CREATE TABLE `TIME`(
            `ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `TASK` VARCHAR(128) NOT NULL,
            `IS_VALID` INT DEFAULT 1,
            `START_TIME` DATETIME NOT NULL,
            `END_TIME` DATETIME NOT NULL);"""

        TEST = """CREATE TABLE `TIME_SEND`(
            `ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `TASK` VARCHAR(128) NOT NULL,
            `START_TIME` DATETIME NOT NULL,
            `IS_VALID` INT DEFAULT 1,
            `%s` DATETIME NOT NULL);""" % 'NOW'

        CONTROL = """CREATE TABLE `CONTROL_DATA`(
            `ID` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `NAME` VARCHAR(128) NOT NULL,
            `STATUS` VARCHAR(128) NOT NULL);"""          
        
        

        cursor.execute(CONTROL)
        
        # 关闭数据库连接
        db.close()


    #获取开始和结束的时间
    def get_time(TASK):
        # 打开数据库连接
        db = pymysql.connect(
            host = '119.23.237.255',
            user = 'user1', 
            passwd = 'user1', 
            db = 'web_data', 
            port = 3306, 
            charset='utf8', 
            cursorclass = pymysql.cursors.DictCursor # 加了此句返回的是字典　查表否则返回为元组类型
            )
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS USER")
        
        # 使用预处理语句创建表
        sql = """SELECT * FROM `TIME` WHERE `TASK` = '%s';""" % TASK

        cursor.execute(sql)

        #获取数据
        results = cursor.fetchall()

        # 关闭数据库连接
        db.close()
        return results

    def get_control_status(NAME_DATA):
        # 打开数据库连接
        db = pymysql.connect(
            host = '119.23.237.255',
            user = 'user1', 
            passwd = 'user1', 
            db = 'web_data', 
            port = 3306, 
            charset='utf8', 
            cursorclass = pymysql.cursors.DictCursor # 加了此句返回的是字典　查表否则返回为元组类型
            )
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS USER")
        
        # 使用预处理语句创建表
        sql = """SELECT * FROM `CONTROL_DATA` WHERE `NAME` = '%s';""" % NAME_DATA
        cursor.execute(sql)
        #获取数据
        results = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        return results



    #更新比赛起始时间和结束时间
    def update_time(TIME_TYPE, TASK, TIME_DATA):
        # 打开数据库连接
        db = pymysql.connect(
            host = '119.23.237.255',
            user = 'user1', 
            passwd = 'user1', 
            db = 'web_data', 
            port = 3306, 
            charset='utf8', 
            cursorclass = pymysql.cursors.DictCursor # 加了此句返回的是字典　查表否则返回为元组类型
            )
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS USER")
        
        # 使用预处理语句创建表
        sql = """UPDATE `TIME` SET `%s` = '%s' WHERE `TASK` = '%s';""" % (TIME_TYPE, TIME_DATA, TASK)
        
        try:
        # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            print("输入有误")

        # 关闭数据库连接
        db.close()




    #更新比赛起始时间和结束时间
    def update_left_time(TIME_TYPE, TASK, TIME_DATA):
        # 打开数据库连接
        db = pymysql.connect(
            host = '119.23.237.255',
            user = 'user1', 
            passwd = 'user1', 
            db = 'web_data', 
            port = 3306, 
            charset='utf8', 
            cursorclass = pymysql.cursors.DictCursor # 加了此句返回的是字典　查表否则返回为元组类型
            )
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS USER")
        
        # 使用预处理语句创建表
        #sql = """UPDATE `TIME` SET `%s` = '%d' WHERE `TASK` = '%s';""" % (TIME_TYPE, TIME_DATA, TASK)
        sql = """UPDATE `TIME` SET `%s` = '%d' WHERE `TASK` = '%s';""" % (TIME_TYPE, TIME_DATA, TASK)
        
        try:
        # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            print("输入有误")

        # 关闭数据库连接
        db.close()






    #更新控制数据
    def update_control_data(NAME_DATA, STATUS_DATA):
                # 打开数据库连接
        db = pymysql.connect(
            host = '119.23.237.255',
            user = 'user1', 
            passwd = 'user1', 
            db = 'web_data', 
            port = 3306, 
            charset='utf8', 
            cursorclass = pymysql.cursors.DictCursor # 加了此句返回的是字典　查表否则返回为元组类型
            )
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS USER")
        
        # 使用预处理语句创建表
        sql = """UPDATE `CONTROL_DATA` SET `STATUS` = '%s' WHERE `NAME` = '%s';""" % (STATUS_DATA, NAME_DATA)
        
        try:
        # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            print("输入有误")

        # 关闭数据库连接
        db.close()



    def write_time_test():
        # 打开数据库连接
        db = pymysql.connect(
            host = '119.23.237.255',
            user = 'user1', 
            passwd = 'user1', 
            db = 'web_data', 
            port = 3306, 
            charset='utf8', 
            cursorclass = pymysql.cursors.DictCursor # 加了此句返回的是字典　查表否则返回为元组类型
            )
        
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS USER"
        
        # 使用预处理语句创建表
        sql = """DELETE FROM `TIME` WHERE `id` = 3;"""

        try:
        # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()





if __name__ == '__main__':
    app=MoonMysql
    #app.update_left_time(TIME_TYPE = 'PASSING',TASK = 'nxp',TIME_DATA = 100)
    #app.update_left_time(TIME_TYPE = 'REMAIN',TASK = 'nxp',TIME_DATA = 99)
    app.creat_table()
    '''
    results=app.get_time(TASK='nxp')

    r=results[0]
    print(r['END_TIME'])
    #for row in results:
       #print(row[4])

    app.write_time_test()
    '''