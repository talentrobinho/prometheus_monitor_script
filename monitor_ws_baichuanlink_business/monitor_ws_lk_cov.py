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



class MonitorWSLKCOV(object):


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
	def calculation_cov(cls, pv_list):
		cov = 0.0
		ad_pv = 0.0
		pv = 0.0
		try:
			ad_pv = pv_list[0]
			pv = pv_list[1]
		except IndexError as err:
			cov = 0
			#print pv_list
			logging.error("cov is zero.[%s]"%(err,))

		try:
			cov = round(ad_pv*100.0/pv,2)
		except ZeroDivisionError as err:
			cov = 0
			#print pv_list
			logging.error("cov is zero.[%s]"%(err,))
		return cov

	@classmethod
	def merge_pv(cls, index, data_dict, is_ad, count):

		if index in data_dict.keys():
			if is_ad == 1:
				data_dict[index][0] += count
			data_dict[index][1] += count
		else:
			if is_ad == 1:
				data_dict[index] = [count, count]
			else:
				data_dict[index] = [0,count]


		return data_dict


	@classmethod
	def map_region(cls, ip):
		#if ip in ws_server_lk:
		#	region = 'ws_server_lk_bj'
		#else:
		#	region = 'unkown'
		#return region
 		ip_prefix=".".join(ip.split(".")[0:2])
 		try:
 			region = "ws_server_lk_{}".format(region_list[ip_prefix])
 		except IndexError as err:
 			logging.error(err)
 			region = 'unkown'

 		return region

	@classmethod
	def wslk_cov(cls, data):
		city_code_map = None
		#is_ad_qps_dict = {}
		qps_dict = {}
		city_code_map = cls.fetch_city_map()
		cov = 0
		machine_pv = {}
		province_pv = {}
		region_pv = {}
		all_pv = {}


		try:
			
			for line in data:

				count = line[0]
				ad_num = line[3]
				ip = str(line[4])
				region = cls.map_region(ip)
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0

				machine_pv = cls.merge_pv(ip, machine_pv, is_ad, count)
				region_pv = cls.merge_pv(region, region_pv, is_ad, count)
		except IndexError as err:
			logging.error(err)
	

		for h in machine_pv:
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_cov = cls.calculation_cov(machine_pv[h])
			except KeyError as err:
				logging.error("all pv is zero[%s]"%(err,))
				machine_cov = 0

			ws_lk_server_cov.labels(region, province, ip, '1').set(machine_cov)


		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_cov = cls.calculation_cov(region_pv[r])
			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_cov =  0

			ws_lk_server_cov.labels(region, province, ip, '1').set(region_cov)


