# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScraperPipeline(object):
#     def process_item(self, item, spider):
#         return item


from .mail_sender import MailSender


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
