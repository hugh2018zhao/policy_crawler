import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.04,  # 请求间隔时间，提升该数字可降低爬取频率
        'TELNETCONSOLE_PORT': [6245],  # telnet端口号
        'REDIRECT_ENABLED': False,  # 关闭302重定向
        'RETRY_TIMES': 50,  # 重试次数
        'RETRY_HTTP_CODES': [302, 307, 400, 403, 407, 429, 500, 503],  # 遇到这些httpcode会重试抓取
        'DEFAULT_REQUEST_HEADERS': {
        },

        'DOWNLOADER_MIDDLEWARES': {
            'policy_crawler_common.scrapy_extensions.middlewares.ua_rotate.RandomUserAgent': 1,
            'policy_crawler_common.scrapy_extensions.middlewares.abu_proxy.AbuProxyMiddleware': 901,
        },
        'USER_AGENT_ROTATE_ENABLED': False,  # 开启RandomUserAgent middleware
        'USER_AGENT_TYPE': 'MOBILE',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36',
        'PROXY_ENABLED': False,  # AbuProxyMiddleware的开关

        'SPIDER_MIDDLEWARES': {
            'policy_crawler_common.scrapy_extensions.middlewares.deltafetch.DeltaFetchMiddleware': 901,
        },
        'DELTAFETCH_ENABLED': False,
        'DELTAFETCH_KEY_NAME': 'raw_key',
        'ITEM_PIPELINES': {
            'policy_crawler_common.scrapy_extensions.pipelines.MysqlExportPipeline': 300,
            'crawlab.pipelines.CrawlabMongoPipeline': 888,
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
        },
        "MySQL_EXPORT_ENABLED": False,
        'COOKIES_ENABLED': False,

        # 分布式爬虫，切换调度器
        # "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        # 分布式爬虫，切换爬虫请求的去重策略
        # "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        # 分布式爬虫，队列持久化，即爬虫结束时是否清理队列
        # "SCHEDULER_PERSIST": False,
        # 分布式爬虫: 爬虫启动后先等待30秒时间，用于往redis中的请求队列填充req对象，若该队列为空则爬虫会结束
        # "SCHEDULER_IDLE_BEFORE_CLOSE": 30,
    }

    def parse(self, response):
        pass

