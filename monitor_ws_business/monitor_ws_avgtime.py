#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-22 21:30:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_ws_conf import *
from monitor_ws_conndb import ConnRedis
import logging
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSAvgTime(object):

	@classmethod
	def fetch_city_map(cls):
		try:
			redis = ConnRedis.conn_redis()
		except Exception as err:
			logging.error("Connecting Redis fail[%s]"%(err))
			sys.exit(1)

		try:
			city_code_map = redis.get('city_code_map')
		except Exception as err:
			logging.error("Fetch data from Redis fail[%s]"%(err))
			sys.exit(1)
		return eval(city_code_map)

	@classmethod
	def ws_avgtime(cls, data, interval):
		city_code_map = None
		timeout = 400000
		time_dict = {}
		timeout_dict = {}
		city_code_map = cls.fetch_city_map()

		
		try:
			for line in data:

				province_code = int(line[3])/100*100
				index="{}_{}".format(line[8], province_code)
				if index in time_dict.keys():
					time_dict[index] += line[1]
					if line[1] > timeout:
						timeout_dict[index] += line[1]
				else:
					time_dict[index] = line[1]
					if line[1] > timeout:
						timeout_dict[index] = line[1]
		except IndexError as err:
			logging.error(err)
	

		for k,v in time_dict.items():
			ip = k.split('_')[0]
			try:
				#city = city_code_map[k.split('_')[2]]
				province = city_code_map[k.split('_')[1]]
			except Exception as err:
				logging.error("Find city_code_map error[%s]"%(err,))
				
			avg_time = v/interval
			timeout_rate = timeout_dict[k]/v*100

			if ip in bj_server_list:
				region = 'ws_server_bj'
			if ip in gd_server_list:
				region = 'ws_server_gd'
			if ip in js_server_list:
				region = 'ws_server_js'
			if ip in sk_server_list:
				region = 'ws_server_bj_sk'
			if ip in pweb_server_list:
				region = 'ws_server_pweb'

			ws_server_avgtime.labels(region, province, ip).set(avg_time)
			ws_server_timeout.labels(region, province, ip).set(timeout_rate)






