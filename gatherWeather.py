#!/bin/python

import weather
import time
import datetime


thisDate = '19800101'
def incrementDate(date):
	dummyTime = str(datetime.datetime.strptime(date, "%Y%m%d").date() + datetime.timedelta(days=1))
	thisDate = dummyTime.replace("-","")
	return thisDate
	
while datetime.datetime.strptime(thisDate, "%Y%m%d").date() < datetime.datetime.now().date() -  datetime.timedelta(days=10):
	for i in range(10):
		print(datetime.datetime.strptime(thisDate, "%Y%m%d").date() )
		weather.updateDB(thisDate)
		thisDate = incrementDate(thisDate)
	time.sleep(61)
	
updateDB(thisDate)
