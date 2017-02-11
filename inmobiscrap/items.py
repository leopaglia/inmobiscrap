# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Departamento(scrapy.Item):
    price = scrapy.Field()
    rooms = scrapy.Field()
    address = scrapy.Field()
    status = scrapy.Field()
    location = scrapy.Field()
    covered_area = scrapy.Field()
    total_area = scrapy.Field()
    url = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
