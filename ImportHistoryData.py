# -*- coding: utf-8 -*-
import tushare as ts
import pymongo
from dateutil import parser
import json

def insertIndex(dict,code):
    list = []
    for k, v in dict.items():
        v['date'] = parser.parse(k)
        v['code'] = code
        list.append(v)
    return list

clinet = pymongo.MongoClient("localhost", 27017)

db = clinet["Stock"]
basics = db['Basics']
histData = db["HistoryData"]
basicList = basics.find()
i = 0
for basic in basicList:
    print i
    print basic['code']
    histDf = ts.get_hist_data(basic['code'], start='2016-01-01', end='2016-07-27')
    if histDf is None:
        print basic['code'] +" is None"
        continue
    histDict = json.loads(histDf.to_json(orient='index'), encoding="UTF-8")
    histList = insertIndex(histDict,basic['code'])
    if len(histList) > 0:
        print 'add:' + str(len(histList))
        histData.insert(histList)
    i+=1

