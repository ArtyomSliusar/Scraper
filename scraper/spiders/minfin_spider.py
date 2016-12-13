#!/usr/bin/env python3

import sys
import os


sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))


import scrapy
from scraper.items import ScraperMinfin


class MinfinSpider(scrapy.Spider):
    name = "currency_rate"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MinfinHtmlPipeline': 300}
    }
    start_urls = [
        'http://minfin.com.ua/currency/mb/',
    ]

    def parse(self, response):
        item = ScraperMinfin()
        item['url'] = response.url
        item['html'] = response.css('table.mb-table-currency').extract()
        yield item
