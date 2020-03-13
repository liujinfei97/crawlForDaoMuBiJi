# -*- coding: utf-8 -*-
import scrapy
from Daomu.items import DaomuItem
from scrapy_redis.spiders import RedisSpider

class DaomuSpider(RedisSpider):
    name = 'daomu'
    #allowed_domains = ['daomubiji.com']
    #start_urls = ['http://www.daomubiji.com/dao-mu-bi-ji-1']
    redis_key = "daomu"

    def parse(self, response):
        # 创建item对象(items.py里面的class)
        item = DaomuItem()
        # 匹配书名(单独匹配)
        item["bookName"] = response.xpath('//h1[@class="focusbox-title"]/text()').extract()[0]
        # 匹配所有章节对象(基准xpath),获取选择器对象中的文本内容，把选择器中的文本都取出，首先xpath中要有/text()
        articles = response.xpath('//article[@class="excerpt excerpt-c3"]')
        for article in articles:
            info = article.xpath('./a/text()').extract()[0].split(' ')
            # ['七星鲁王','第十二章','门']
            item["bookTitle"] = info[0]
            item["zhName"] = info[2]
            item["zhNum"] = info[1]
            item["zhLink"] = article.xpath('./a/@href').extract()[0]

            # 需要对url发起请求,获取页面数据进行指定的解析
            url = item["zhlink"]
            # meta参数值可以赋值一个字典(将item对象先封装到一个字典中)
            yield scrapy.Request(url=url,callback=self.secondParse,meta={'item':item})

    def secondParse(self,response):
        txts = response.xpath('.//div[@class="m-post"]/p/text()')
        # 取出Request方法的meta参数传递过来的字典(response.meta)
        item = response.meta['item']
        for txt in txts:
            item["zhTxt"]+=txt
        # 将item提交给管道
        yield item
        
