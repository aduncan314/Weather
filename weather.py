import requests
import sys
import json
import MySQLdb
from config_Weather import WUkey, Wkey



	

#FUNCTION getWeather
#call WU API, get the hourly conditions for a certain date and return a dictionary
def getWeather(zc, date):
	zc = int(zc)
	#Check zipcode and convert to string
	if (zc <= 99999 and zc >= 501):
		zipcode = '%05d' %zc
	else:
		print('NOT A ZIPCODE: '+ str(zc) + '\n Failed before API call')#time too?
		sys.exit(1)
		
	
	
	#define the url for this call to the API
	print('zipcode is: ' + zipcode)
	print('date is: ' + date)
	thisCall = '/history_' + date + '/q/' + zipcode
	url ='http://api.wunderground.com/api/' + WUkey + thisCall + '.json'
	myRequest = requests.get(url)
	parsedRequest = myRequest.json()
	
	#dictionary of daily summary conditions
	conditions = {'location' : 'Boston',		#name from zipcode later
							#daily conditions
							'date' : str(parsedRequest['history']['dailysummary'][0]['date']['year']) + '-'
										+ str(parsedRequest['history']['dailysummary'][0]['date']['mon']) + '-'
										+ str(parsedRequest['history']['dailysummary'][0]['date']['mday'])			,
							'maxtemp' : str(parsedRequest['history']['dailysummary'][0]['maxtempm'])		,
							'mintemp ':  str(parsedRequest['history']['dailysummary'][0]['mintempm'])			,
							'meantemp' :  str(parsedRequest['history']['dailysummary'][0]['meantempm'])	,
							'maxhum' :  str(parsedRequest['history']['dailysummary'][0]['maxhumidity'])		,
							'minhum' :  str(parsedRequest['history']['dailysummary'][0]['minhumidity'])		,
							'precip' :			str(parsedRequest['history']['dailysummary'][0]['precipm'])
							}
#	#for lazy debug
#	for i in conditions:
#		print(i + ': '+ conditions[i])
	
	#create hourly dictionary to be added to conditions
	hourly = []
	for j in range(24):
		hourly.append({'time' : date[:4] + '-' + date[4:6] + '-' + date[6:8] + ' '
								+ str(parsedRequest['history']['observations'][j]['date']['hour']) + ':' 
								+ str(parsedRequest['history']['observations'][j]['date']['min']) +':00'	,
								'temp' : str(parsedRequest['history']['observations'][j]['tempm'])			,
								'hum' : str(parsedRequest['history']['observations'][j]['hum'])					,
								'press' : str(parsedRequest['history']['observations'][j]['pressurem'])		,
								'hprecip' : str(parsedRequest['history']['observations'][j]['precipm'])})
							
	conditions['hourly'] = hourly
#	print(hourly)
#	print(conditions)
	return conditions
#END getWeather


#FUNCTION updateDB
#take dictionary from getWeather() and add it to the database
def updateDB(date):
	locZip = '02215'
	loc = 'Boston'
	
	updateConditions = getWeather(locZip, date)
	myDB = MySQLdb.connect('localhost', 'root', Wkey , 'Weather')
	cursor = myDB.cursor()
	
	#loop through items in the daily summary to add to DB
	cursor.execute('INSERT INTO daily_summary (location, date) VALUES (\'' + loc + '\', \'' + str(updateConditions['date']) +'\');')
	for key in updateConditions:
		if (key != 'hourly' and  key !=  'location' and  key !=  'date'):
			#load dailysummary
			try:
				cursor.execute('UPDATE  daily_summary SET '+ str(key) + ' = \'' + str(updateConditions[key]) 
										+ '\' WHERE location = \'' + loc + '\' AND date = \'' + date + '\'')
				myDB.commit()
			except:
				#the following syntax is wrong! It will stay for now to 
				print('FAILED for: ' + 'UPDATE  daily_summary SET '+ str(key) + ' = \'' + str(updateConditions[key]) 
										+ '\' WHERE location = \'' + loc + '\' AND date = \'' + date + '\'')
				myDB.commit()
				myDB.rollback()

	#load hourly
	updateHourly = updateConditions['hourly']
	#fix so that location can be used instead of zip?
	for i in range(24):
		cursor.execute('INSERT INTO hourly (location, time) VALUES (\''+ loc + '\', \'' + str(updateHourly[i]['time']) +'\');')
		for key2 in updateHourly[i]:
			#load dailysummary
			if key2 != 'time':
				try:
					cursor.execute('UPDATE hourly SET ' + str(key2) + ' = \'' + str(updateHourly[i][key2]) 
											+ '\' WHERE location = \'' +loc + '\' AND time = \'' + str(updateHourly[i]['time']) +'\'')
					myDB.commit()
				except:
					print('FAILED for: ' + '(' + str(key) +':' + str(updateHourly[i][key]) + ')')
					myDB.rollback()
	
	myDB.close()
#END updateDB

