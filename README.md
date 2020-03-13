# crawlForDaoMuBiJi
this is a crawl for novel-DaoMuBiJi
使用scrapy,redis, mongodb实现的一个分布式网络爬虫,底层存储mongodb集群,分布式使用redis实现。
实际是先利用框架将数据存储到redis数据库，再将数据取出（即运行main）存入到mongodb中
这个爬虫文件针对的是盗墓笔记网的小说文件的爬取。
需要的环境是：
安装scrapy
安装redispy
安装pymongo
安装mongodb
安装redis
下载本工程
启动redis server
搭建mongodb集群
ps:此文件还同样的增加了针对Mysql数据库存储的方法，需要使用是可以下载pymysql与mysql.然后在settings文件中配置相应的端口号，ip等即可

注意：scrapy-redis爬虫组件是基于redis数据库做数据持久化，不能是别的数据库
修改redis启动配置文件：redis.windows.conf 
将 bind 127.0.0.1 进行注释
将 protected-mode no 关闭保护模式

运行方式：
运行爬虫文件：scrapy runspider SpiderFile
# 调度器队列中等待请求对象
向调度器队列中扔入一个起始url（在redis客户端中操作）：lpush redis_key属性值  起始url（“http://www.dmbj.cc/daomubiji1/”）



#在实际使用时，需要配置UA池和地址池，如下（具体的User-Agent及代理ip可以自行查询更改）
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# UA池代码的编写（单独给UA池封装一个下载中间件的一个类）
# 导包UserAgentMiddleware类
class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        # 从列表中随机抽选一个ua值
        ua = random.choice(user_agent_list)
        # ua值进行当前拦截到请求的ua的写入操作
        request.headers.setdefault('User-Agent', ua)


# 可被选用的代理IP
PROXY_http = [
    '153.180.102.104:80',
    '195.208.131.189:56055',
]
PROXY_https = [
    '120.83.49.90:9000',
    '95.189.112.214:35508',
]

# 批量对拦截到的请求进行IP更换
class Proxy(object):
    def process_request(self, request, spider):
        # 对拦截到请求的url进行判断（协议头到底是http还是https）
        # request.url返回值：http://www.xxx.com
        h = request.url.split(':')[0]  # 请求的协议头
        if h == 'https':
            ip = random.choice(PROXY_https)
            request.meta['proxy'] = 'https://' + ip
        else:
            ip = random.choice(PROXY_http)
            request.meta['proxy'] = 'http://' + ip
