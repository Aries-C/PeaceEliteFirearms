# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pymysql as pymysql


class PeaceelitefirearmsPipeline:
    # 构造方法
    def __init__(self):
        self.fp = None  # 定义一个文件描述符属性

    # 下列都是在重写父类的方法：
    # 开始爬虫时，执行一次
    def open_spider(self, spider):
        print('爬虫开始')
        self.fp = open('./data.txt', 'w')

    # 因为该方法会被执行调用多次，所以文件的开启和关闭操作写在了另外两个只会各自执行一次的方法中。
    def process_item(self, item, spider):
        # 将爬虫程序提交的item进行持久化存储
        self.fp.write(item['name'] + '\n'
                      + "优点：" + item['youdian'] + '\n'
                      + "缺点：" + item['quedian'] + '\n')
        return item

    # 结束爬虫时，执行一次
    def close_spider(self, spider):
        self.fp.close()
        print('爬虫结束')



class PeaceelitefirearmsPipelinedb:
    def __init__(self):
        # 连接数据库
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '000000',
            'database': 'scrapy',
            'charset': 'utf8',
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()  # 获取游标
        self.sql = None

        # 创建表之前看是否存在当前要创建的表，有就删除
        self.cursor.execute("drop table if exists {}".format("gpdata") )
        # 创建搜索关键字表sql语句
        sql = """create table %s(
                    id  int primary key auto_increment,
                    枪械名称 varchar (255),
                    枪械优点 varchar (255),
                    枪械缺点 varchar (255),
                    爬取时间 datetime)"""
        # 执行创建表的语句
        self.cursor.execute(sql % "gpdata")

    def process_item(self, item, spider):
        # 插入数据的sql语句
        self.sql = "insert into gpdata" + "(枪械名称, 枪械优点, 枪械缺点, 爬取时间) values(%s,%s,%s,%s)"
        self.cursor.execute(self.sql, (item['name'], item['youdian'], item['quedian'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        self.conn.commit()  # 保存数据

        return item

    def close_spider(self, spider):
        self.conn.close()  # 关闭数据库连接
