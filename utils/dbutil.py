import sqlite3
import os
import pytz
from datetime import date, datetime
import time

class DBModel(object):
	def __init__(self,modelName):
		self.modelName = modelName
		self.conn = None
		
	def DBInit(self,dbName,initSql):
		if os.path.exists(dbName) is False:
			conn = sqlite3.connect(dbName)
			cursor = conn.cursor()
			cursor.execute(initSql)
			conn.commit()
			conn.close()

	def DBConnect(self,dbName):
		if self.conn is not None:
			self.conn.close()
			
		if os.path.exists(dbName) is False:
			print("Please invoke InitDB first!")
			return
		
		try:
			self.conn = sqlite3.connect(dbName)
			self.cursor = self.conn.cursor()
		except:
			print("Connect database {} faild!".format(dbName))

	def GetShanghaiTime(self):
		tz = pytz.timezone('Asia/Shanghai')
		ts = int(time.time())
		dt = datetime.fromtimestamp(ts,tz)
		return datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond)
            

	def DBClose(self):
		if self.conn != None:
			self.conn.close()
			self.conn = None
			self.cursor = None

	def DBSaveData(self,tableName,valueNames,values):
		if self.conn is None:
			print("Not connecte database")
			return
		s = ''
		valueCount = len(values)
		for x in range(valueCount):
			s += '?'
			if x + 1 < valueCount:
				s += ','
			
		sql = "insert into {} {} values({})".format(tableName,valueNames,s)
		self.cursor.execute(sql,values)
		self.conn.commit()



