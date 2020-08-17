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



class MonitorWSRPM(object):


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
	def calculation_rpm(cls, consume, pv_list, num):
		rpm = 0
		try:
			pv = pv_list[num-1]

		except IndexError as err:
			rpm = 0
			logging.error("rpm is zero.[%s]"%(err,))
			return rpm


		try:
			rpm = round(consume*1.0/pv*10, 2)
		except ZeroDivisionError as err:
			rpm = 0
			#print pv_list
			logging.error("rpm is zero.[%s]"%(err,))
			return rpm
		return rpm

	@classmethod
	def merge_pv(cls, index, pv_dict, is_ad, ad_num, count):

		if index in pv_dict.keys():
			if is_ad == 1:
				pv_dict[index][2] += count
				pv_dict[index][1] += (ad_num*count)
			pv_dict[index][0] += count
		else:
			if is_ad == 1:
				pv_dict[index] = [count, (ad_num*count), count]
			else:
				pv_dict[index] = [count, 0, 0]

		return pv_dict

	@classmethod
	def merge_consume(cls, index, consume_dict, price):
		if index in consume_dict.keys():
			consume_dict[index] += price
		else:
			consume_dict[index] = price

		return consume_dict


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
	def ws_rpm(cls, cdielog, wsielog):
		city_code_map = None
		#is_ad_qps_dict = {}
		qps_dict = {}
		city_code_map = cls.fetch_city_map()
		rpm = 0
		machine_pv = {}
		province_pv = {}
		region_pv = {}
		all_pv = {}
		machine_consume = {}
		province_consume = {}
		region_consume = {}
		all_consume = {}

		#print wsielog[1:10]
		try:
			
			for line in wsielog:

				#province_code = int(line[3])/100*100
				#ip = str(line[8])
				#is_ad = int(line[7])
				#ad_num = int(line[6])
				#region = cls.map_region(ip)
				
				#all_pv = cls.merge_pv('all', all_pv, is_ad, ad_num)
				#machine_pv = cls.merge_pv(ip, machine_pv, is_ad, ad_num)
				#region_pv = cls.merge_pv(region, region_pv, is_ad, ad_num)
				##province_pv_a = cls.merge_pv(province, province_pv, is_ad)



				count = line[0]
				ad_num = line[5]
				ip = str(line[6])
				region = cls.map_region(ip)
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0
				all_pv = cls.merge_pv('all', all_pv, is_ad, ad_num, count)
				machine_pv = cls.merge_pv(ip, machine_pv, is_ad, ad_num, count)
				region_pv = cls.merge_pv(region, region_pv, is_ad, ad_num, count)

		except IndexError as err:
			logging.error(err)
	


		for line in cdielog:
			try:
				price = int(line[0])
				ip = line[3]
				province_code = int(line[2])/100*100
				region = cls.map_region(ip)
				if region == 'unkown':
					continue
				all_consume = cls.merge_consume('all', all_consume, price)
				machine_consume = cls.merge_consume(ip, machine_consume, price)
				region_consume = cls.merge_consume(region, region_consume, price)

			except IndexError as err:
				logging.error(err)


		#print region_consume
		#print all_pv
		try:
			all_rpm1 = cls.calculation_rpm(all_consume['all'], all_pv['all'], 1)
			all_rpm2 = cls.calculation_rpm(all_consume['all'], all_pv['all'], 2)
			all_rpm3 = cls.calculation_rpm(all_consume['all'], all_pv['all'], 3)
		except KeyError as err:
			all_rpm1 = 0
			all_rpm2 = 0
			all_rpm3 = 0
			logging.error("all pv is zero[%s]"%(err,))

		ws_server_rpm.labels('all', 'all', 'all', '1').set(all_rpm1)
		ws_server_rpm.labels('all', 'all', 'all', '2').set(all_rpm2)
		ws_server_rpm.labels('all', 'all', 'all', '3').set(all_rpm3)


		for h in machine_pv.keys():
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_rpm1 = cls.calculation_rpm(machine_consume[h], machine_pv[h], 1)
				machine_rpm2 = cls.calculation_rpm(machine_consume[h], machine_pv[h], 2)
				machine_rpm3 = cls.calculation_rpm(machine_consume[h], machine_pv[h], 3)
			#print "[hh]region: %s, ip: %s m_rpm1: %s".format(region, ip, machine_rpm1)
			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				machine_rpm1 = 0
				machine_rpm2 = 0
				machine_rpm3 = 0


			ws_server_rpm.labels(region, province, ip, '1').set(machine_rpm1)
			ws_server_rpm.labels(region, province, ip, '2').set(machine_rpm2)
			ws_server_rpm.labels(region, province, ip, '3').set(machine_rpm3)


		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_rpm1 = cls.calculation_rpm(region_consume[r], region_pv[r], 1)
				region_rpm2 = cls.calculation_rpm(region_consume[r], region_pv[r], 2)
				region_rpm3 = cls.calculation_rpm(region_consume[r], region_pv[r], 3)
			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_rpm1 = 0
				region_rpm2 = 0
				region_rpm3 = 0

			#print "[rr]region: %s, ip: %s m_rpm1: %s".format(region, ip, machine_rpm1)
			ws_server_rpm.labels(region, province, ip, '1').set(region_rpm1)
			ws_server_rpm.labels(region, province, ip, '2').set(region_rpm2)
			ws_server_rpm.labels(region, province, ip, '3').set(region_rpm3)







		#for p in province_pv:
		#	region = 'unkown'
		#	ip = 'unkown'
		#	province = p
		#	province_rpm = cls.calculation_rpm(province_pv[p])
		#	ws_server_rpm.labels(region, province, ip).set(province_rpm)
		#	



	@classmethod
	def ws_channel_rpm(cls, cdielog, wsielog):

		channel_pv = {}
		channel_consume = {}
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
				if ad_num > 0:
					is_ad = 1
				else:
					is_ad = 0
				if ch_index in channel_map.keys():
					channel_pv = cls.merge_pv(ch_index, channel_pv, is_ad, ad_num, count)


		except IndexError as err:
			logging.error(err)
	


		for line in cdielog:
			try:
				price = int(line[0])
				ch_code = line[8]
				if ch_code[0:3] in channel_map.keys():
					channel_consume = cls.merge_consume(ch_code[0:3], channel_consume, price)
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
				channel_rpm1 = cls.calculation_rpm(channel_consume[ch], channel_pv[ch], 1)
				channel_rpm2 = cls.calculation_rpm(channel_consume[ch], channel_pv[ch], 2)
				channel_rpm3 = cls.calculation_rpm(channel_consume[ch], channel_pv[ch], 3)
			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				channel_rpm1 = 0
				channel_rpm2 = 0
				channel_rpm3 = 0


			ws_channel_rpm.labels(channel1, channel2, '1', industry).set(channel_rpm1)
			ws_channel_rpm.labels(channel1, channel2, '2', industry).set(channel_rpm2)
			ws_channel_rpm.labels(channel1, channel2, '3', industry).set(channel_rpm3)





