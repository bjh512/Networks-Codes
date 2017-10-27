import requests, os

from apscheduler.schedulers.blocking import BlockingScheduler
from influxdb import InfluxDBClient
import datetime
import logging
import telepot
from pprint import pprint
import json

def get_price():
	payload_USD = {'fsym' : "BTC", 
	'tsym' : "USD", 
	'markets' : 'Bitfinex',
	}
	payload_KRW = {'fsym' : "BTC", 
	'tsym' : "KRW", 
	'markets' : 'Bithumb',
	}
	payload_QTM = {'fsym' : "QTM",
	'tsym' : "USD",
	'markets' : 'Bitfinex'
	}

	u = requests.get('https://min-api.cryptocompare.com/data/generateAvg',params=payload_USD)
	k = requests.get('https://min-api.cryptocompare.com/data/generateAvg',params=payload_KRW)
	q = requests.get('https://min-api.cryptocompare.com/data/generateAvg',params=payload_QTM)

	return u,k,q


def store_price(usd,krw,qtm):
	client = InfluxDBClient(database='BTCdb')
	client = InfluxDBClient(host='127.0.0.1', port=8086, database='BTCdb')
	print('DB Connection Succeeded!')	
	
	json_body = [
	{
		'measurement' : 'btc_price',
		'fields' : {
			"Bitfinex-BTC-USD" : float(usd.json()['RAW']['PRICE']),
			"Bithumb-BTC-KRW" : float(krw.json()['RAW']['PRICE']),
			"Bitfinex-QTM-USD" : float(qtm.json()['RAW']['PRICE'])
		}
	}
	]
	
	client.write_points(json_body)
	lastdata = client.query('select * from btc_price order by time desc limit 1;')
	
	return lastdata

def executor():
	usd,krw,qtm=get_price()
	lastdata = store_price(usd,krw,qtm)


	bot = telepot.Bot('336851358:AAE3ep3drWtTMxdlKtgDYnPPPl9PUgCuMoc')
	pprint(lastdata.raw['series'][0])
	
	output = " "	
	
	output += str(lastdata.raw['series'][0]['columns'])+"\n"
	output += str(lastdata.raw['series'][0]['values'][0])+"\n"

	cost = 10.37
	now_qtm = lastdata.raw['series'][0]['values'][0][2]
	benefit = now_qtm-cost
	output += str(benefit) if benefit<0 else "+"+str(benefit)
	
	bot.sendMessage(414462743, output)
	

if __name__ == '__main__':
	logging.basicConfig()
	scheduler = BlockingScheduler()
	scheduler.add_executor('processpool')
	
	scheduler.add_job(executor, 'interval', seconds=60)

	
	print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

	try:
		scheduler.start()

	except(KeyboardInterrupt, SystemExit):
		pass

