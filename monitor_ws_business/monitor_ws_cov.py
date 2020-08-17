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



class MonitorWSCOV(object):


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
		#region = 'unkown'
		if ip in bj_server_list:
			region = 'ws_server_bj'
		elif ip in gd_server_list:
			region = 'ws_server_gd'
		elif ip in js_server_list:
			region = 'ws_server_js'
		elif ip in sk_server_list:
			region = 'ws_server_bj_sk'
		elif ip in pweb_server_list:
			region = 'ws_server_pweb'
		else:
			region = 'unkown'
			#logging.info("unkown: %s" % (ip,))
		return region


	@classmethod
	def ws_cov(cls, data):
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

				#province_code = int(line[3])/100*100
				#ip = str(line[8])
				#is_ad = int(line[7])
				#region = cls.map_region(ip)
				
				#all_pv = cls.merge_pv('all', all_pv, is_ad)
				#machine_pv = cls.merge_pv(ip, machine_pv, is_ad)
				#region_pv = cls.merge_pv(region, region_pv, is_ad)
				#province_pv_a = cls.merge_pv(province, province_pv, is_ad)

				count = line[0]
				ad_num = line[5]
				ip = str(line[6])
				region = cls.map_region(ip)
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0

				all_pv = cls.merge_pv('all', all_pv, is_ad, count)
				machine_pv = cls.merge_pv(ip, machine_pv, is_ad, count)
				region_pv = cls.merge_pv(region, region_pv, is_ad, count)
		except IndexError as err:
			logging.error(err)
	
		#print all_pv

		try:
			all_cov = cls.calculation_cov(all_pv['all'])
		except KeyError as err:
			logging.error("all pv is zero[%s]"%(err,))
			all_cov = 0

		ws_server_cov.labels('all', 'all', 'all', '1').set(all_cov)

		for h in machine_pv:
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_cov = cls.calculation_cov(machine_pv[h])
			except KeyError as err:
				logging.error("all pv is zero[%s]"%(err,))
				machine_cov = 0

			ws_server_cov.labels(region, province, ip, '1').set(machine_cov)


		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_cov = cls.calculation_cov(region_pv[r])
			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_cov =  0

			ws_server_cov.labels(region, province, ip, '1').set(region_cov)



		#for p in province_pv:
		#	region = 'unkown'
		#	ip = 'unkown'
		#	province = p
		#	province_cov = cls.calculation_cov(province_pv[p])
		#	ws_server_cov.labels(region, province, ip).set(province_cov)
		#	




	@classmethod
	def ws_channel_cov(cls, data):
		cov = 0
		channel_pv = {}
		channel1 = 'unkown'
		channel2 = 'unkown'
		industry = 'unkown'

		channel_map = {
						'302': 'qq',
					   	'303': 'sogou',
					   	'304': 'waigou'
					  }

		try:
			for line in data:
				count = line[0]
				ad_num = line[5]
				ch_index = line[7]

				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0

				if ch_index in channel_map.keys():
					channel_pv = cls.merge_pv(ch_index, channel_pv, is_ad, count)

		except IndexError as err:
			logging.error(err)
	

		for ch in channel_pv:	
			try:
				channel1 = channel_map[ch]
			except IndexError as err:
				logging.error('[IndexError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'
			except KeyError as err:
				logging.error('[KeyError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'

			try:
				channel_cov = cls.calculation_cov(channel_pv[ch])
			except KeyError as err:
				logging.error("channel pv is zero[%s]"%(err,))
				channel_cov = 0

			ws_channel_cov.labels(channel1, channel2, 'unkown', industry).set(channel_cov)


