# -*- coding: utf-8 -*-
import scrapy
import string
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from StockAnalysis.items import SZItem, SCItem, StockDailyDetailItem, SZSCDailyDetailItem
from  datetime import *
from dateutil import parser
import demjson


# 用来爬上证深成两市每日详细情况
class StockDailySpider(scrapy.Spider):
    name = "StockDaily"
    allowed_domains = ["xueqiu.com"]
    start_urls = (
        'https://xueqiu.com',
    )

    def parse(self, response):
        print type(response.headers.getlist('Set-Cookie'))
        cookieSet = response.headers.getlist('Set-Cookie')
        s = cookieSet[0].split(';')[0].split('=')[1]
        xq_a_token = cookieSet[1].split(';')[0].split('=')[1]
        xq_r_token = cookieSet[2].split(';')[0].split('=')[1]
        queryUrl = "https://xueqiu.com/v4/stock/quote.json?code=SH000001%2CSZ399001"
        yield Request(url=queryUrl, cookies={'s': s, 'xq_a_token': xq_a_token, 'xq_r_token': xq_r_token},
                      callback=self.parseJson)  # spider json

    def parseJson(self, response):
        jsonObj = demjson.decode(response.body)
        sz = jsonObj['SH000001']
        sc = jsonObj['SZ399001']
        szDaily = SZSCDailyDetailItem()
        szDaily['ct'] = datetime.now()
        szDaily['lt'] = parser.parse(sz['time'])
        szDaily['zdz'] = sz['change']
        szDaily['zdf'] = sz['percentage']
        szDaily['ss'] = 0
        szDaily['zs'] = sz['current']
        szDaily['op'] = sz['open']
        szDaily['h'] = sz['high']
        szDaily['l'] = sz['low']
        szDaily['h52'] = sz['high52week']
        szDaily['l52'] = sz['low52week']
        print szDaily
        scDaily = SZSCDailyDetailItem()
        scDaily['ct'] = datetime.now()
        scDaily['lt'] = parser.parse(sc['time'])
        scDaily['zdz'] = sc['change']
        scDaily['zdf'] = sc['percentage']
        scDaily['ss'] = 1
        scDaily['zs'] = sc['current']
        scDaily['op'] = sc['open']
        scDaily['h'] = sc['high']
        scDaily['l'] = sc['low']
        scDaily['h52'] = sc['high52week']
        scDaily['l52'] = sc['low52week']
        print scDaily
        yield scDaily
        yield szDaily
