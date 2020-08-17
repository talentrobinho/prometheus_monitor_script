#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-17 10:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_ws_conf import *
from monitor_ws_conndb import ConnRedis
import logging
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSLKQPS(object):

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
	def wslk_qps(cls, data, interval):
		city_code_map = None
		qps_dict = {}
		city_code_map = cls.fetch_city_map()

		try:
			for line in data:
				count = line[0]
				ad_num = line[3]
				index = line[4]
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0
				if index in qps_dict.keys():
					qps_dict[index][0] += count
					qps_dict[index][1] += ad_num
					qps_dict[index][2] += is_ad
				else:
					qps_dict[index] = [count, ad_num, is_ad]

		except IndexError as err:
			logging.error(err)

		for ip in qps_dict.keys():
			province = 'unkown'
			qps = qps_dict[ip][0]/interval
			qps2 = qps_dict[ip][1]/interval
			qps3 = qps_dict[ip][2]/interval

			#region='unkown'
			#if ip in ws_server_lk:
			#	region = 'ws_server_lk_bj'
 			ip_prefix=".".join(ip.split(".")[0:2])
 			try:
 				region = "ws_server_lk_{}".format(region_list[ip_prefix])
 			except IndexError as err:
 				logging.error(err)
 				region = 'unkown'


			ws_lk_server_qps.labels(region, province, ip, '1').set(qps)
			ws_lk_server_qps.labels(region, province, ip, '2').set(qps2)
			ws_lk_server_qps.labels(region, province, ip, '3').set(qps3)




