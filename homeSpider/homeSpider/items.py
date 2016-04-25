# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HomespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    location = scrapy.Field()
    floor = scrapy.Field()
    rooms = scrapy.Field()
    pow = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    town = scrapy.Field()
    sellType = scrapy.Field()

