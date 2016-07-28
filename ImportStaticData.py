# -*- coding: utf-8 -*-
import tushare as ts
import pymongo
import json


def insertIndex(dict):
    list = []
    for k, v in dict.items():
        v['code'] = k
        list.append(v)
    return list


clinet = pymongo.MongoClient("localhost", 27017)

db = clinet["Stock"]
basics = db["Basics"]
industry = db['Industry']
concept = db['Concept']


basicDf = ts.get_stock_basics()
basicDict = json.loads(basicDf.to_json(orient='index'), encoding="UTF-8")
basicList = insertIndex(basicDict)
basics.insert(basicList)

industryDf = ts.get_industry_classified()
industryDict = json.loads(industryDf.to_json(orient='records'), encoding="UTF-8")
industry.insert(industryDict)

conceptDf = ts.get_concept_classified()
conceptDict = json.loads(conceptDf.to_json(orient='records'), encoding="UTF-8")
concept.insert(conceptDict)
