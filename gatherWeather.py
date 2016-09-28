#!/bin/python

import weather
import time
from datetime import datetime


thisDate = '19831101'

def incrementDate(date):
	dummyTime = str(datetime.strptime(date, "%Y%m%d").date() + timedelta(days=1))
	thisDate = dummyTime.replace("-","")
	return thisDate
	
#if datetime.strptime(thisDate, "%Y%m%d").date() < datetime.now().date():
#	print("poop")
	
while datetime.strptime(date, "%Y%m%d").date() < datetime.now().date() -  timedelta(days=10):
	for i in range(10):
		thisDate = incrementDate(thisDate)
		print(thisDate)
	time.sleep(60)

#updateDB(thisDate)
