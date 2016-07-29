# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import SHItem, SZItem, SHSZDailyDetailItem, CommentItem, PersonItem


class StockanalysisPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Stock"]
        self.SHItem = db["SH"]
        self.SZItem = db["SZ"]
        self.SHSZDailyDetailItem = db['SHSZDaily']
        self.CommentItem = db['Comment']
        self.PersonItem = db['Person']

    def process_item(self, item, spider):
        if isinstance(item, SZItem):
            try:
                self.SZItem.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, SHItem):
            try:
                self.SHItem.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, SHSZDailyDetailItem):
            try:
                self.SHSZDailyDetailItem.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, CommentItem):
            try:
                self.CommentItem.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, PersonItem):
            try:
                self.PersonItem.insert(dict(item))
            except Exception:
                pass
        return item
