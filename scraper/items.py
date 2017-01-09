# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaceItem(scrapy.Item):
    # define the fields for your item here like:
    track_name = scrapy.Field()
    race_time = scrapy.Field()
    race_id = scrapy.Field()
    participants = scrapy.Field()


class ParticipantItem(scrapy.Item):
    # define the fields for your item here like:
    participant_name = scrapy.Field()
    participant_id = scrapy.Field()
    participant_chances = scrapy.Field()
