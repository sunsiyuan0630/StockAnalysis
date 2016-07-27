# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import SZItem,SCItem

class StockanalysisPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Stock"]
        self.SZItem = db["SZ"]
        self.SCItem = db["SC"]

    def process_item(self, item, spider):
        if isinstance(item, SZItem):
            try:
                self.SZItem.insert(dict(item))
            except Exception:
                pass
        if isinstance(item, SCItem):
            try:
                self.SCItem.insert(dict(item))
            except Exception:
                pass
        return item
