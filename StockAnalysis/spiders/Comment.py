# -*- coding: utf-8 -*-
import scrapy
import pymongo
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
from StockAnalysis.items import CommentItem, PersonItem
from  datetime import *
from dateutil import parser
import demjson


# 用来爬雪球个股评论
class CommentSpider(scrapy.Spider):
    name = "Comment"
    allowed_domains = ["xueqiu.com"]
    start_urls = (
        'https://xueqiu.com/',
    )
    commentList = []
    userList = []
    cookies = {}

    def getCookie(self, response):
        cookieSet = response.headers.getlist('Set-Cookie')
        s = cookieSet[0].split(';')[0].split('=')[1]
        xq_a_token = cookieSet[1].split(';')[0].split('=')[1]
        xq_r_token = cookieSet[2].split(';')[0].split('=')[1]
        cookies = {'s': s, 'xq_a_token': xq_a_token, 'xq_r_token': xq_r_token}
        self.cookies = cookies
        return cookies

    def parse(self, response):
        cookies = self.getCookie(response)
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Stock"]
        sh = db['SH']
        shList = sh.find()
        for item in shList:
            symbol = 'SH'+str(item['code'])
            queryUrl = "https://xueqiu.com/statuses/search.json?count=1&symbol="+symbol+"&source=all&sort=alpha&page=1"
            yield Request(url=queryUrl, cookies=cookies, callback=self.getJson)  # spider json
        print 'commentList add:' + str(len(self.commentList))
        print 'userList add:' + str(len(self.userList))

    def getJson(self, response):
        cookies = self.cookies
        jsonObj = demjson.decode(response.body)
        count = jsonObj['count']
        symbol = jsonObj['symbol']
        totalPage = count / 20
        if totalPage >= 100:
            total = 100
        else:
            total = totalPage
        print 'totalPage:' + str(totalPage)
        print 'scanTotal:' + str(total)
        for i in range(total):
            print 'scanPage:' + str(i)
            queryUrl = 'https://xueqiu.com/statuses/search.json?count=20&symbol=' + str(symbol) + '&source=all&sort=alpha&page=' + str(i) + ''
            yield Request(url=queryUrl, cookies=cookies, callback=self.parseJson)

    def parseJson(self, response):
        jsonObj = demjson.decode(response.body)
        page = jsonObj['page']
        print 'page:' + str(page)
        code = jsonObj['symbol'].replace('SZ', '').replace('SH', '')
        list = jsonObj['list']
        commentList = self.commentList
        userList = self.userList
        for comment in list:
            u = PersonItem()
            c = CommentItem()
            if comment['user_id'] in userList:
                print 'userId:' + str(comment['user_id']) + 'has already in userList!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            else:
                userList.append(comment['user_id'])
                u['_id'] = comment['user_id']
                yield u
            if comment['id'] in commentList:
                print 'commentId:' + str(comment['id']) + ' has already in commentList!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                continue
            else:
                commentList.append(comment['id'])

            c['_id'] = comment['id']
            c['pd'] = comment['user_id']
            if comment['title'] is not None:
                c['tt'] = comment['title']
            c['c'] = comment['text'].lower().replace(' ', '').replace('&nbsp', '').replace('<strong>', '').replace('</strong>', '').replace('<br/>', '').replace('<br>', '').replace(';', '').replace('<span>','').replace('</span>', '')
            if comment['created_at'] is not None:
                c['ct'] = datetime.utcfromtimestamp(comment['created_at'] / 1000)
            if comment['edited_at'] is not None:
                c['le'] = datetime.utcfromtimestamp(comment['edited_at'] / 1000)
            c['f'] = comment['retweet_count']
            c['cn'] = comment['reply_count']
            c['k'] = comment['fav_count']
            c['stockCode'] = code
            c['lt'] = datetime.now()
            c['cf'] = comment['source']
            c['a'] = comment['donate_count']
            yield c

