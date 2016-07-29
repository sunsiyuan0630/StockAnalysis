# -*- coding: utf-8 -*-
import scrapy
import string
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from StockAnalysis.items import SHItem, SZItem
from datetime import *


# 用来爬上证深成两市所有股票，制成字典表
class SZSCSpider(scrapy.Spider):
    name = "SHSZ"
    allowed_domains = ["eastmoney.com"]
    start_urls = (
        'http://quote.eastmoney.com/stocklist.html',
    )

    def parse(self, response):
        sel = response.xpath('//div[@id="quotesearch"]').extract()[0].strip()
        soup = BeautifulSoup(sel,'lxml')
        print soup.prettify()
        szsiblings = soup.select('ul')[0].select('a')
        i = 0
        for sibling in szsiblings:
            mystr = sibling.string
            print mystr
            tmpstr = mystr.replace('(', ' ').replace(')', '')
            tmpArr = tmpstr.split(' ', 1)
            name = tmpArr[0].encode("utf-8")
            code = tmpArr[1].encode("utf-8")
            szItem = SHItem()
            szItem['_id'] = i
            szItem['name'] = name
            szItem['code'] = code
            szItem['lastUpdate'] = datetime.now()
            i += 1
            yield szItem

        scsiblings = soup.select('ul')[1].select('a')
        j = 0
        for sibling in scsiblings:
            mystr = sibling.string
            print mystr
            tmpstr = mystr.replace('(', ' ').replace(')', '')
            tmpArr = tmpstr.split(' ', 1)
            name = tmpArr[0].encode("utf-8")
            code = tmpArr[1].encode("utf-8")
            scItem = SZItem()
            scItem['_id'] = j
            scItem['name'] = name
            scItem['code'] = code
            scItem['lastUpdate'] = datetime.now()
            j += 1
            yield scItem
