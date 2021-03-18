# -*- coding: utf-8 -*-
import scrapy

from scrapy.utils.project import get_project_settings

settings = get_project_settings()
BOT_NAME = settings.get('BOT_NAME')


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['abuyun.com']
    start_urls = ['http://test.abuyun.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.00,
        'TELNETCONSOLE_PORT': [6201],
        'REDIRECT_ENABLED': False,
        'RETRY_TIMES': 50,
        'RETRY_HTTP_CODES': [302, 307, 400, 403, 429, 500, 503],
        # 'DEFAULT_REQUEST_HEADERS': {
        # },
        'DOWNLOADER_MIDDLEWARES': {
            'policy_crawler_common.scrapy_extensions.middlewares.ua_rotate.RandomUserAgent': 1,
            'policy_crawler_common.scrapy_extensions.middlewares.abu_proxy.AbuProxyMiddleware': 901,
        },
        'USER_AGENT_ROTATE_ENABLED': True,
        'USER_AGENT_TYPE': 'MOBILE',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36',
        'PROXY_ENABLED': True,

        # 'SPIDER_MIDDLEWARES': {
            # BOT_NAME+'.middlewares.deltafetch.DeltaFetchMiddleware': 901,
        # },
        # 'DELTAFETCH_ENABLED': True,
        # 'DELTAFETCH_KEY_NAME': 'id',
        # 'DELTAFETCH_DB_NAME': 'crawl',
        # 'DELTAFETCH_TABLE_NAME': 'base',
        'ITEM_PIPELINES': {
            # 'manga_crawler_common.scrapy_extensions.pipelines.MysqlExportPipeline': 300,
        },
        "MySQL_EXPORT_ENABLED": False,

        'COOKIES_ENABLED': False,
        #  'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        #  'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderQueue',
        #  'SCHEDULER_PERSIST': True,
        #  'SCHEDULER_IDLE_BEFORE_CLOSE': 30,
    }

    def start_requests(self):
        url = 'http://test.abuyun.com'
        for i in range(1000):
            yield scrapy.Request(url,
                                 dont_filter=True,
                                 callback=self.parse)

    def parse(self, response):
        print(response.xpath("/html/body/table/tr[3]/td"))
        return {"success": True}
        # print(response.body)
        # print(response.text)
