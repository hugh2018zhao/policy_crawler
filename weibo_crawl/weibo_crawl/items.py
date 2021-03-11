# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    weibo_id       = scrapy.Field()
    raw_content    = scrapy.Field()
    search_keyword = scrapy.Field()
