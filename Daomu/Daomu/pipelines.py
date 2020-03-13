# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 导入settings模块,可使用定义的相关变量
from Daomu import settings
import pymongo
import pymysql

class DaomuPipeline(object):
    def process_item(self, item, spider):
        print("==================")
        print(item["bookName"])
        print(item["bookTitle"])
        print(item["zhName"])
        print(item["zhNum"])
        print(item["zhLink"])
        print("==================")


#此方法只能用于非分布式，因为scrapy_redis只支持redis数据库的存储
class DaomumongoPipeline(object):
    def __init__(self):
        # 从settings.py中获取变量的值
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        # 创建数据库连接对象、库对象、集合对象
        conn = pymongo.MongoClient(host=host,port=port)
        db = conn.daomudb
        self.myset = db.daomubiji


    def process_item(self,item,spider):
        # 把item对象转为字典
        bookInfo = dict(item)
        self.myset.insert(bookInfo)
        print("存入数据库成功")
        # return item

#此方法只能用于非分布式，因为scrapy_redis只支持redis数据库的存储
class DaomumysqlPipeline(object):
    def __init__(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        pwd = settings.MYSQL_PWD
        dbName = settings.MYSQL_DB
        self.db = pymysql.connect(host=host,user=user,
                     password = pwd,
                     db = dbName,
                     charset = "utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        ins = 'insert into daomubiji values(%s,%s,%s,%s,%s,%s)'
        L = [item['bookName'],item['bookTitle'],\
             item['zhName'],item['zhNum'],item['zhLink'],item['zhTxt']]
        self.cursor.execute(ins,L)
        self.db.commit()

## redis.windows.conf配置：
#bind 127.0.0.1，表示可以让其他ip访问redis

#将yes该为no：protected-mode no，表示可以让其他ip操作redis

class DaomuRedisPipeline(obj):
    def open_spider(self, spider):
        # 连接数据库
        self.conn = redis.Redis(host='192.168.1.10', port=6379)

    def process_item(self, item, spider):
        data_dict = item
        self.conn.lpush('data', data_dict)
        return item
