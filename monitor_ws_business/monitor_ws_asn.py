#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-13 10:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_ws_conf import *
from monitor_ws_conndb import ConnRedis
import logging
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSASN(object):


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
	def calculation_asn(cls, pv_list):
		asn = 0
		try:
			ad_num_pv = pv_list[0]
			ad_pv = pv_list[1]

		except IndexError as err:
			asn = 0
			logging.error("asn is zero.[%s]"%(err,))
			return asn


		try:
			asn = round(ad_num_pv*1.0/ad_pv,2)
		except ZeroDivisionError as err:
			asn = 0
			logging.error("asn is zero.[%s]"%(err,))
			return asn
		return asn

	@classmethod
	def merge_pv(cls, index, pv_dict, is_ad, reserved, count):

		if index in pv_dict.keys():
			if is_ad == 1:
				ad_top = 0
				for id_pos in reserved.split(','):
					if (int(id_pos) >> 1 & 15) < 8:
						ad_top += 1
				pv_dict[index][0] += ad_top*count
				pv_dict[index][1] += count
				
		else:
			if is_ad == 1:
				ad_top = 0
				for id_pos in reserved.split(','):
					if (int(id_pos) >> 1 & 15) < 8:
						ad_top += 1
				pv_dict[index] = [ad_top*count, count]

		return pv_dict


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
	def ws_asn(cls, wsielog):
		city_code_map = None
		#is_ad_qps_dict = {}
		qps_dict = {}
		city_code_map = cls.fetch_city_map()
		asn = 0
		machine_pv = {}
		province_pv = {}
		region_pv = {}
		all_pv = {}


		try:
			
			for line in wsielog:

				count = line[0]
				ad_num = line[5]
				ip = str(line[6])
				reserved = line[8]
				region = cls.map_region(ip)
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0
				all_pv = cls.merge_pv('all', all_pv, is_ad, reserved, count)
				machine_pv = cls.merge_pv(ip, machine_pv, is_ad, reserved, count)
				region_pv = cls.merge_pv(region, region_pv, is_ad, reserved, count)

		except IndexError as err:
			logging.error(err)


		try:
			all_asn = cls.calculation_asn(all_pv['all'])
		except KeyError as err:
			all_asn = 0
			logging.error("all pv is zero[%s]"%(err,))

		ws_server_asn.labels('all', 'all', 'all', 'unkown').set(all_asn)



		for h in machine_pv.keys():
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_asn = cls.calculation_asn(machine_pv[h])

			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				machine_asn = 0



			ws_server_asn.labels(region, province, ip, 'unkown').set(machine_asn)



		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_asn = cls.calculation_asn(region_pv[r])

			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_asn = 0

			ws_server_asn.labels(region, province, ip, 'unkown').set(region_asn)



		#for p in province_pv:
		#	region = 'unkown'
		#	ip = 'unkown'
		#	province = p
		#	province_asn = cls.calculation_asn(province_pv[p])
		#	ws_server_asn.labels(region, province, ip).set(province_asn)
		#	


	@classmethod
	def ws_channel_asn(cls, wsielog):
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
			
			for line in wsielog:

				count = line[0]
				ad_num = line[5]
				ch_index = line[7]
				reserved = line[8]
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0
				if ch_index in channel_map.keys():
					channel_pv = cls.merge_pv(ch_index, channel_pv, is_ad, reserved, count)


		except IndexError as err:
			logging.error(err)


		for ch in channel_pv.keys():

			try:
				channel1 = channel_map[ch]
			except IndexError as err:
				logging.error('[IndexError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'
			except KeyError as err:
				logging.error('[KeyError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'

			try:
				channel_asn = cls.calculation_asn(channel_pv[ch])

			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				channel_asn = 0



			ws_channel_asn.labels(channel1, channel2, 'unkown', industry).set(channel_asn)




