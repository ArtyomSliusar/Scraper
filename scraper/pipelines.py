# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import csv


def write_to_csv(filename, order, item=None):
    with open('{}_result.csv'.format(filename), 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        if item is not None:
            writer.writerow([item[key] for key in order])
        else:
            writer.writerow(order)


class WriteToCsv(object):

    def open_spider(self, spider):
        try:
            self.order = spider.custom_settings["FEED_EXPORT_FIELDS"]
        except:
            raise Exception("FEED_EXPORT_FIELDS NOT SPECIFIED FOR SPIDER '{}'".format(spider.name))
        else:
            write_to_csv(spider.name, self.order)

    def process_item(self, item, spider):
        write_to_csv(spider.name, self.order, item)
        return item
