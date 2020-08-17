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



class MonitorWSTime(object):


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
	def calculation_avgtime(cls, pv_list):
		avgtime = 0.0
		cost_time = 0
		pv = 0.0
		try:
			cost_time = pv_list[0]
			pv = pv_list[1]
		except IndexError as err:
			avgtime = 0
			#print pv_list
			logging.error("avgtime is zero.[%s]"%(err,))

		try:
			avgtime = round(cost_time/pv,2)
		except ZeroDivisionError as err:
			avgtime = 0
			#print pv_list
			logging.error("avgtime is zero.[%s]"%(err,))
		return avgtime



	@classmethod
	def merge_data(cls, index, data_dict, mics):

		if index in data_dict.keys():
			data_dict[index][0] += mics
			data_dict[index][1] += 1
		else:
			data_dict[index] = [mics,1]

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
	def ws_time(cls, data):
		city_code_map = None
		#is_ad_qps_dict = {}
		qps_dict = {}
		city_code_map = cls.fetch_city_map()
		cov = 0
		timeout = 100000
		
		province_pv = {}
		
		all_cost_time = {}
		machine_cost_time = {}
		region_cost_time = {}

		all_timeout {}
		machine_timeout = {}
		region_timeout = {}



		try:
			
			for line in data:
				if str(line[1]) == '' or str(line[1].isalnum()):
					continue
				province_code = int(line[3])/100*100
				ip = str(line[8])
				cost_time = int(line[1])
				region = cls.map_region(ip)
				if str(line[0]) == '__free' and cost_time > 100000000:
					all_cost_time = cls.merge_data('all', all_cost_time, cost_time)
					machine_cost_time = cls.merge_data(ip, machine_cost_time, cost_time)
					region_cost_time = cls.merge_data(region, region_cost_time, cost_time)


					if cost_time > timeout:
						all_timeout = cls.merge_data('all', all_timeout, cost_time)
						machine_timeout = cls.merge_data(ip, machine_timeout, cost_time)
						region_timeout = cls.merge_data(region, region_timeout, cost_time)

		except IndexError as err:
			logging.error(err)
	

		'''总平均响应时间、总超时的平均时间、总超时率、总超时数量'''
		try:
			all_avgtime = cls.calculation_avgtime(all_cost_time['all'])
		except KeyError as err:
			logging.error("all pv is zero[%s]"%(err,))
			all_avgtime = 0

		ws_server_time.labels('all', 'all', 'all', 'avgtime').set(all_avgtime)

		try:
			all_avg_timeout = cls.calculation_avgtime(all_timeout['all'])
		except KeyError as err:
			logging.error("all pv is zero[%s]"%(err,))
			all_avg_timeout = 0

		ws_server_time.labels('all', 'all', 'all', 'avg_timeout').set(all_avg_timeout)

		all_timeout_count = all_timeout['all'][1]
		ws_server_time.labels('all', 'all', 'all', 'timeout_count').set(all_timeout_count)

		all_timeout_rate = all_timeout_count*100/all_cost_time['all'][1]
		ws_server_time.labels('all', 'all', 'all', 'timeout_rate').set(all_timeout_rate)


		'''分机器平均响应时间、分机器超时的平均时间、分机器超时率、分机器超时数量'''
		for h in machine_cost_time:
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_cost_time = cls.calculation_avgtime(machine_cost_time[h])
			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				machine_avgtime = 0

			ws_server_time.labels(region, province, ip, 'avgtime').set(machine_avgtime)


			try:
				machine_avg_timeout = cls.calculation_avgtime(machine_timeout[h])
			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				machine_avg_timeout = 0
			ws_server_time.labels(region, province, ip, 'avg_timeout').set(machine_avg_timeout)

			machine_timeout_count = machine_timeout[h][1]
			ws_server_time.labels(region, province, ip, 'timeout_count').set(machine_timeout_count)
		
			machine_timeout_rate = machine_timeout_count*100/machine_cost_time[h][1]
			ws_server_time.labels(region, province, ip, 'timeout_rate').set(machine_timeout_rate)

		'''分机房平均响应时间、分机房超时的平均时间、分机房超时率、分机房超时数量'''
		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_cost_time = cls.calculation_avgtime(region_cost_time[h])
			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_avgtime = 0

			ws_server_time.labels(region, province, ip, 'avgtime').set(region_avgtime)


			try:
				region_avg_timeout = cls.calculation_avgtime(region_timeout[h])
			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_avg_timeout = 0
			ws_server_time.labels(region, province, ip, 'avg_timeout').set(region_avg_timeout)

			region_timeout_count = region_timeout[h][1]
			ws_server_time.labels(region, province, ip, 'timeout_count').set(region_timeout_count)
		
			region_timeout_rate = region_timeout_count*100/region_cost_time[h][1]
			ws_server_time.labels(region, province, ip, 'timeout_rate').set(region_timeout_rate)



		#for p in province_pv:
		#	region = 'unkown'
		#	ip = 'unkown'
		#	province = p
		#	province_cov = cls.calculation_cov(province_pv[p])
		#	ws_server_cov.labels(region, province, ip).set(province_cov)
		#	
