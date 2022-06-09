# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UoocItem(scrapy.Item):
    # define the fields for your item here like:
    chapter_name = scrapy.Field()
    sub_name     = scrapy.Field()
    sub_url      = scrapy.Field()
    caption      = scrapy.Field()
    choice       = scrapy.Field()