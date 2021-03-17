import scrapy

import json
# from weibo_search_crawl.weibo_search_crawl.items import WeiboSearchItem
from weibo_crawl.items import WeiboItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class WeiboSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['weibo.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.04,  # 请求间隔时间，提升该数字可降低爬取频率
        'TELNETCONSOLE_PORT': [6245],  # telnet端口号
        'REDIRECT_ENABLED': False,  # 关闭302重定向
        'RETRY_TIMES': 50,  # 重试次数
        'RETRY_HTTP_CODES': [302, 307, 400, 403, 407, 429, 500, 503],  # 遇到这些httpcode会重试抓取
        'DEFAULT_REQUEST_HEADERS': {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        },

        'DOWNLOADER_MIDDLEWARES': {
            'policy_crawler_common.scrapy_extensions.middlewares.ua_rotate.RandomUserAgent': 1,
            'policy_crawler_common.scrapy_extensions.middlewares.abu_proxy.AbuProxyMiddleware': 901,
        },
        'USER_AGENT_ROTATE_ENABLED': False,
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
            'policy_crawler_common.scrapy_extensions.pipelines.MysqlExportPipeline': 300,
            'crawlab.pipelines.CrawlabMongoPipeline': 888,
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
        },
        "MySQL_EXPORT_ENABLED": False,
        'COOKIES_ENABLED': False,

        # "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        # "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        # "SCHEDULER_PERSIST": False,
        # "SCHEDULER_IDLE_BEFORE_CLOSE": 30,
    }

    def start_requests(self):
        self.TEST = self.settings["TEST"]
        search_keywords = {
            "天官赐福", "天官赐福漫画", "天官漫画", "天官", "社交温度", "灰灰",
        }

        if self.TEST is True:
            search_keywords = {search_keywords.pop(), search_keywords.pop()}
        for keyword in search_keywords:
            yield self.req_search(keyword)

    def req_search(self, keyword):
        url = 'https://s.weibo.com/weibo?q={}'
        return scrapy.Request(url=url.format(keyword),
                              meta={"keyword": keyword},
                              callback=self.parse_search)

    def parse_search(self, response):
        keyword = response.meta['keyword']

        tweets = response.xpath('//*[@id="pl_feedlist_index"]//*[@action-type="feed_list_item"]')
        for tweet in tweets:
            item = WeiboItem()
            item['search_keyword'] = keyword
            item['weibo_id'] = tweet.xpath("@mid").get() or ''
            if not item['weibo_id']:
                continue
            item['raw_content'] = tweet.get() or ''
            if not item['raw_content']:
                continue
            yield item
