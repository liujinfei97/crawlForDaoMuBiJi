# -*- coding: utf-8 -*-
import pymongo
import redis
import json

#此方法只能用于非分布式，因为scrapy_redis只支持redis数据库的存储
class DaomumongoPipeline(object):
    def main():
        # 指定Redis数据库信息
        rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        # 指定MongoDB数据库信息
        mongocli = pymongo.MongoClient(host='localhost', port=27017)
        # 创建数据库名
        db = mongocli['daomu']
        # 创建表名
        sheet = db['daomu_item']
        offset = 0
        while True:
            # FIFO模式(先进先出)为 blpop，LIFO模式(先进后出)为 brpop，获取键值
            source, data = rediscli.blpop(["daomu:items"])  #daomu为自己写的解析程序的name属性
            item = json.loads(data.decode("utf-8"))
            sheet.insert(item)
            offset += 1
            print(offset)
            try:
                print("Processing: %s " % item)
            except KeyError:
                print("Error procesing: %s" % item)

    if __name__ == '__main__':
        main()



