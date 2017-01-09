# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperRozetka(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    link = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()


class ScraperMoyo(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    link = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()


class ScraperMinfin(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    html = scrapy.Field()
