# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from policy_crawler_common.scrapy_extensions.items import RawItem, itemify


class NdrcSpider(scrapy.Spider):
    name = 'ndrc'
    allowed_domains = ['zfxxgk.ndrc.gov.cn']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # 请求间隔时间，提升该数字可降低爬取频率
        'TELNETCONSOLE_PORT': [6245],  # telnet端口号
        'REDIRECT_ENABLED': False,  # 关闭302重定向
        'RETRY_TIMES': 50,  # 重试次数
        'RETRY_HTTP_CODES': [302, 307, 400, 403, 407, 429, 500, 503],  # 遇到这些httpcode会重试抓取
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

        'SPIDER_MIDDLEWARES': {
            'policy_crawler_common.scrapy_extensions.middlewares.deltafetch.DeltaFetchMiddleware': 901,
        },
        'DELTAFETCH_ENABLED': True,
        'DELTAFETCH_KEY_NAME': 'raw_key',
        'ITEM_PIPELINES': {
            'crawlab.pipelines.CrawlabMongoPipeline': 888,
        },
        'COOKIES_ENABLED': True,
    }

    def start_requests(self):
        # 首次抓取可全量扫描，后续每天增量可只抓10页
        # for i in range(1500):
            # yield self.req_list(i)

        # 增量
        # for i in range(10):
            # yield self.req_list(i)

        # 测试用
        yield self.req_list(1)

    def req_list(self, page=0):
        url = 'https://zfxxgk.ndrc.gov.cn/web/dirlist.jsp?dirid=0&pid=0'
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Origin': 'https://zfxxgk.ndrc.gov.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://zfxxgk.ndrc.gov.cn/web/dirlist.jsp?dirid=0&pid=0',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        }
        data = {
            "starttime": "",
            "endtime": "",
            "IndexCode": "",
            "ItemName": "",
            "UnitId": 0,
            "ItemCode": "",
            "itemCont": "",
            "SearchKeys": "",
            "pageNum": page,
        }
        return scrapy.Request(url=url,
                              method="POST",
                              headers=headers,
                              body=urllib.parse.urlencode(data),
                              callback=self.parse_list)

    def parse_list(self, response):
        urls = response.xpath('//div[@class="zwxxkg-result"]//a/@href')
        for url in urls:
            url = url.get()
            prefix = "iteminfo.jsp?id="
            if url.startswith(prefix):
                detail_id = url[url.find(prefix)+len(prefix):]
                yield self.req_detail(detail_id)

    def req_detail(self, detail_id):
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        }
        url = "https://zfxxgk.ndrc.gov.cn/web/iteminfo.jsp?id=" + detail_id
        return scrapy.Request(url=url,
                              headers=headers,
                              meta={"detail_id": detail_id,
                                    "deltafetch_key": str(detail_id)},
                              callback=self.parse_detail)

    def parse_detail(self, response):
        detail_id = response.meta["detail_id"]
        yield itemify(raw_key=detail_id, url=response.url, category="detail",
                      source="ndrc", html=response.body)



