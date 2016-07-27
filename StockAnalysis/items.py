# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class SZItem(scrapy.Item):
    _id = Field()
    code = Field()
    name = Field()
    lastUpdate = Field()


class SCItem(scrapy.Item):
    _id = Field()
    code = Field()
    name = Field()
    lastUpdate = Field()


class SZSCDailyDetailItem(scrapy.Item):
    _id = Field()
    ct = Field()  # 创建时间
    lt = Field()  # 记录时间
    zdz = Field()  # 涨跌值
    zdf = Field()  # 涨跌幅
    ss = Field()  # 上深  0表示上证  1表示深成
    zs = Field()  # 指数
    op = Field()  #开盘
    h = Field()   #最高
    l = Field()   #最低
    h52 = Field()   #52周最高
    l52 = Field()   #52周最低


class StockDailyDetailItem(scrapy.Item):
    _id = Field()
    stockCode = Field()  # 股票编码
    createdTime = Field()  # 创建时间
    date = Field()  # 该股记录时间
    s = Field()  # 今开
    h = Field()  # 今日最高
    h52 = Field()  # 52周最高
    z = Field()  # 昨天收盘价
    d = Field()  # 今日最低价
    l52 = Field()  # 52周最低
    e = Field()  # 今日成交额
    zt = Field()  # 涨停价
    zsz = Field()  # 总市值
    my = Field()  # 每股收益
    syl = Field()  # 市盈率
    dtj = Field()  # 跌停价
    zgb = Field()  # 总股本
    mgz = Field()  # 每股净资产
    sjl = Field()  # 市净率
    zf = Field()  # 振幅
    ltb = Field()  # 流通股本
    mgx = Field()  # 每股股息
    sxl = Field()  # 市销率


class Person(scrapy.Item):
    _id = Field()
    g = Field()  # 性别
    l = Field()  # location
    v = Field()  # 是否实名认证
    fc = Field()  # 关注股票数
    dc = Field()  # 参与讨论次数
    fans = Field()  # 粉丝数
    cc = Field()  # 圈子
    sn = Field()  # 个人签名


class CommentDailyDetail(scrapy.Item):
    stockCode = Field()  # 股票编码
    ct = Field()  # 创建时间
    lt = Field()  # 记录时间
    pd = Field()  # Person Id
    c = Field()  # 评论内容
    f = Field()  # 转发次数
    k = Field()  # 收藏次数
    a = Field()  # 打赏次数
    cn = Field()  # 评论数
    cf = Field()  # 来自
