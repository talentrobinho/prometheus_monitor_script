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



class MonitorWSCTR(object):


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
	def calculation_ctr(cls, click_pv, pv_list, num):
		ctr = 0
		try:
			pv = pv_list[num-1]

		except IndexError as err:
			ctr = 0
			logging.error("ctr is zero.[%s]"%(err,))
			return ctr


		try:
			ctr = round(click_pv*10000/pv,2)/100
		except ZeroDivisionError as err:
			ctr = 0
			#print pv_list
			logging.error("ctr is zero.[%s]"%(err,))
			return ctr
		return ctr

	@classmethod
	def merge_pv(cls, index, pv_dict, is_ad, ad_num, count):

		if index in pv_dict.keys():
			if is_ad == 1:
				pv_dict[index][2] += count
				pv_dict[index][1] += ad_num*count
			pv_dict[index][0] += count
		else:
			if is_ad == 1:
				pv_dict[index] = [count, ad_num*count, count]
			else:
				pv_dict[index] = [count, 0, 0]

		return pv_dict

	@classmethod
	def merge_click_pv(cls, index, click_pv_dict, click_pv):
		if index in click_pv_dict.keys():
			click_pv_dict[index] += click_pv
		else:
			click_pv_dict[index] = click_pv

		return click_pv_dict


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
	def ws_ctr(cls, cdielog, wsielog):
		city_code_map = None
		#is_ad_qps_dict = {}
		qps_dict = {}
		city_code_map = cls.fetch_city_map()
		ctr = 0
		machine_pv = {}
		province_pv = {}
		region_pv = {}
		all_pv = {}
		machine_click_pv = {}
		province_click_pv = {}
		region_click_pv = {}
		all_click_pv = {}

		#print wsielog[1:10]
		try:
			
			for line in wsielog:

				#province_code = int(line[3])/100*100
				#ip = str(line[8])
				#is_ad = int(line[7])
				#ad_num = int(line[6])
				#region = cls.map_region(ip)
				#
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
				click_pv = 1
				ip = line[3]
				province_code = int(line[2])/100*100
				region = cls.map_region(ip)
				if region == 'unkown':
					continue
				all_click_pv = cls.merge_click_pv('all', all_click_pv, click_pv)
				machine_click_pv = cls.merge_click_pv(ip, machine_click_pv, click_pv)
				region_click_pv = cls.merge_click_pv(region, region_click_pv, click_pv)

			except IndexError as err:
				logging.error(err)


		#print region_consume
		#print all_pv
		#print all_click_pv
		try:
			all_ctr1 = cls.calculation_ctr(all_click_pv['all'], all_pv['all'], 1)
			all_ctr2 = cls.calculation_ctr(all_click_pv['all'], all_pv['all'], 2)
			all_ctr3 = cls.calculation_ctr(all_click_pv['all'], all_pv['all'], 3)
		except KeyError as err:
			all_ctr1 = 0
			all_ctr2 = 0
			all_ctr3 = 0
			logging.error("all pv is zero[%s]"%(err,))

		ws_server_ctr.labels('all', 'all', 'all', '1').set(all_ctr1)
		ws_server_ctr.labels('all', 'all', 'all', '2').set(all_ctr2)
		ws_server_ctr.labels('all', 'all', 'all', '3').set(all_ctr3)


		for h in machine_pv.keys():
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_ctr1 = cls.calculation_ctr(machine_click_pv[h], machine_pv[h], 1)
				machine_ctr2 = cls.calculation_ctr(machine_click_pv[h], machine_pv[h], 2)
				machine_ctr3 = cls.calculation_ctr(machine_click_pv[h], machine_pv[h], 3)
			#print "[hh]region: %s, ip: %s m_ctr1: %s".format(region, ip, machine_ctr1)
			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				machine_ctr1 = 0
				machine_ctr2 = 0
				machine_ctr3 = 0


			ws_server_ctr.labels(region, province, ip, '1').set(machine_ctr1)
			ws_server_ctr.labels(region, province, ip, '2').set(machine_ctr2)
			ws_server_ctr.labels(region, province, ip, '3').set(machine_ctr3)


		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_ctr1 = cls.calculation_ctr(region_click_pv[r], region_pv[r], 1)
				region_ctr2 = cls.calculation_ctr(region_click_pv[r], region_pv[r], 2)
				region_ctr3 = cls.calculation_ctr(region_click_pv[r], region_pv[r], 3)
			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_ctr1 = 0
				region_ctr2 = 0
				region_ctr3 = 0

			#print "[rr]region: %s, ip: %s m_ctr1: %s".format(region, ip, machine_ctr1)
			ws_server_ctr.labels(region, province, ip, '1').set(region_ctr1)
			ws_server_ctr.labels(region, province, ip, '2').set(region_ctr2)
			ws_server_ctr.labels(region, province, ip, '3').set(region_ctr3)







		#for p in province_pv:
		#	region = 'unkown'
		#	ip = 'unkown'
		#	province = p
		#	province_ctr = cls.calculation_ctr(province_pv[p])
		#	ws_server_ctr.labels(region, province, ip).set(province_ctr)
		#	




	@classmethod
	def ws_channel_ctr(cls, cdielog, wsielog):

		ctr = 0
		channel_pv = {}
		channel_click_pv = {}
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
				click_pv = 1
				ch_code = line[8]
				if ch_code[0:3] in channel_map.keys(): 
					channel_click_pv = cls.merge_click_pv(ch_code[0:3], channel_click_pv, click_pv)

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
				channel_ctr1 = cls.calculation_ctr(channel_click_pv[ch], channel_pv[ch], 1)
				channel_ctr2 = cls.calculation_ctr(channel_click_pv[ch], channel_pv[ch], 2)
				channel_ctr3 = cls.calculation_ctr(channel_click_pv[ch], channel_pv[ch], 3)
			except KeyError as err:
				logging.error("channel pv is zero[%s]"%(err,))
				channel_ctr1 = 0
				channel_ctr2 = 0
				channel_ctr3 = 0


			ws_channel_ctr.labels(channel1, channel2, '1', industry).set(channel_ctr1)
			ws_channel_ctr.labels(channel1, channel2, '2', industry).set(channel_ctr2)
			ws_channel_ctr.labels(channel1, channel2, '3', industry).set(channel_ctr3)







