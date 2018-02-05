from utils.dbutil import DBModel
from utils import webutil
import time
from datetime import date,datetime
import threading
import sysconfig
import json
import os
import sys


url_buy_btc = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=1&tradeType=1&currentPage=1&payWay=&country=&online=1'
url_sell_btc = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=1&tradeType=0&currentPage=1&payWay=&country=&online=1'
url_buy_eth = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=3&tradeType=1&currentPage=1&payWay=&country=&online=1'
url_sell_eth = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=3&tradeType=0&currentPage=1&payWay=&country=&online=1'
url_buy_usdt = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=1&currentPage=1&payWay=&country=&online=1'
url_sell_usdt = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=0&currentPage=1&payWay=&country=&online=1'


class Recorder(DBModel):
    def __init__(self,url,name):
        super(Recorder,self).__init__(name)
        self.url = url
        self.name = name
        self.tableName = 'priceData'
        self.dbName = None
        
    def InitDB(self):
        sql = '''
            Create table priceData(
            p1 double,
            p2 double,
            p3 double,
            p4 double,
            p5 double,
            p6 double,
            p7 double,
            p8 double,
            p9 double,
            p10 double,
            created_at datetime);
        '''
        self.DBInit(self.dbName,sql)
        
    def __RefreshDbConnect(self):
        now = self.GetShanghaiTime()
        dbName = "{}_{}_{}_{}.db".format(self.name,now.year,now.month,now.day)
        if self.dbName is not None:
            if self.dbName != dbName:
                self.DBClose()
                print("Close Previous DB:",self.dbName)
        
        if self.dbName is None or self.dbName != dbName:
            self.dbName = dbName
            self.InitDB()
            self.DBConnect(self.dbName)
            print("Connect DB:",self.dbName)   
    
    def DoWork(self):
        self.working = True
        t = threading.Thread(target=self.__WorkingThread)
        t.setDaemon(True)
        t.start()
        
    def StopWork(self):
        self.working = False
        
    def __WorkingThread(self):
        print("WorkStarted:",self.name)
        while self.working:
            self.__RefreshDbConnect()
            try:
                priceData = webutil.http_get_request(self.url)
                if priceData['code'] != 200:
                    time.sleep(3)
                    continue
                priceSet = []
                for item in priceData['data']:
                    price = item['price']
                    priceSet.append(price)
                    
                priceCount = len(priceSet)
                additionAppend = 10 - priceCount
                
                for x in range(additionAppend):
                    priceSet.append(-1)
                    
                now = self.GetShanghaiTime()
                priceSet.append(now)
                self.DBSaveData(self.tableName,'(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,created_at)', tuple(priceSet))
                time.sleep(5)
            except Exception as e:
                print('e:',e)
                time.sleep(5)
        self.DBClose()
        print("Work terminated:",self.name)


recorderList = []
   
        
recorder = Recorder(url_buy_btc,'buybtc')
recorder.DoWork()
recorderList.append(recorder)

recorder = Recorder(url_sell_btc,'sellbtc')
recorder.DoWork()
recorderList.append(recorder)

recorder = Recorder(url_buy_eth,'buyeth')
recorder.DoWork()
recorderList.append(recorder)

recorder = Recorder(url_sell_eth,'selleth')
recorder.DoWork()
recorderList.append(recorder)

recorder = Recorder(url_buy_usdt,'buyusdt')
recorder.DoWork()
recorderList.append(recorder)

recorder = Recorder(url_sell_usdt,'sellusdt')
recorder.DoWork()
recorderList.append(recorder)

while True:
    if os.path.exists('terminate'):
        for recorder in recorderList:
            recorder.StopWork()
        
        time.sleep(10)
        sys.exit()
    time.sleep(10)