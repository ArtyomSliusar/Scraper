# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScraperPipeline(object):
#     def process_item(self, item, spider):
#         return item

import re
import os
import json
from .mail_sender import MailSender
from scrapy.exceptions import DropItem


class MinfinHtmlPipeline(object):

    def process_item(self, item, spider):
        buf_list = []
        add_html_header(buf_list)
        buf_list.append("<h2>Interbank exchange rate:</h2>\n")
        buf_list.append("<p><a href='{}'>URL</a></p>\n".format(item['url']))
        buf_list.append("\n".join(item['html']))
        add_html_footer(buf_list)
        mail = MailSender("minfin_scraper", ["artyomsliusar@gmail.com"], "Minfin", buf_list, 'html')
        mail.send()


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.line_sep = ",\n"
        self.file = open('{}.json'.format(spider.name), 'wb')
        self.file.write(bytes('[', 'UTF-8'))

    def close_spider(self, spider):
        self.file.seek(-len(self.line_sep), os.SEEK_END)
        self.file.truncate()  # truncate last line separator
        self.file.write(bytes(']', 'UTF-8'))
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + self.line_sep
        self.file.write(bytes(line, 'UTF-8'))
        return item


class MoyoCleansingPipeline(object):

    def process_item(self, item, spider):
        if item['title']:
            title = re.sub(r'[^\x00-\x7F]+ |\n', ' ', item['title'])
            item['title'] = re.sub(r' +', ' ', title).strip()
        else:
            raise DropItem("Missing title in {}".format(item))
        if item['price']:
            item['price'] = item['price'].replace('\u00a0', '')
        else:
            raise DropItem("Missing price in {}".format(item))
        if item['link']:
            item['link'] = 'http://www.moyo.ua' + item['link']
        else:
            raise DropItem("Missing link in {}".format(item))
        return item


def add_html_header(buf_list):
    buf_list.append("<!DOCTYPE html>\n")
    buf_list.append("<html>\n")
    buf_list.append("<head>\n")
    buf_list.append('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
    buf_list.append("</head>\n")
    buf_list.append("<body>\n")


def add_html_footer(buf_list):
    buf_list.append("</body>\n")
    buf_list.append("</html>\n")
