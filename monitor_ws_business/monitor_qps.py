#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-17 10:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_consume_conf import *
import logging


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSQPS(object):

	@classmethod
	def fetch_city_map(cls):
		try:
			redis = ConnRedis.conn_redis()
		except Exception as err:
			logging.error("Connecting Redis fail[%s]"%(err))
			sys.exit(1)

		try:
			city_code_map = redis.smembers('city_code')
		except Exception as err:
			logging.error("Fetch data from Redis fail[%s]"%(err))
			sys.exit(1)

	@classmethod
	def ws_qps(cls, data):
		city_code_map = None
		city_code_map = cls.fetch_city_map()
		
		try:
			for line in data:
				if line[3] in city_code_map.keys():
					city = city_code_map['city_name']
					city_qps += 1
				else:
					city = 'unknow'
					unknow_qps += 1
				
		except IndexError as err:
			logging.error(err)
			huazhang_search_consume = 0
		huazhang_channel_consume.labels('huazhang_channel_huazhang', '0.0.0.0').set(huazhang_search_consume/100)
