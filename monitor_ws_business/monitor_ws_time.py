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
		avgtime = 0
		cost_time = 0
		pv = 0
		try:
			cost_time = pv_list[0]
			pv = pv_list[1]
		except IndexError as err:
			avgtime = 0
			#print pv_list
			logging.error("index error.[%s]"%(err,))

		if pv == 0:
			avgtime = 0
		else:
			try:
				avgtime = round(cost_time/pv)
			except ZeroDivisionError as err:
				avgtime = 0
				#print pv_list
				logging.error("avgtime is zero.[%s]"%(err,))
		return avgtime



	@classmethod
	def merge_data(cls, index, data_dict, micsencod, timeout, count):
		#mics = int(micsencod)
		
		if index in data_dict.keys():
			data_dict[index]['time'][0] += micsencod
			data_dict[index]['time'][1] += count
			#if mics > timeout:
			if timeout == 1:
				data_dict[index]['timeout'][0] += micsencod
				data_dict[index]['timeout'][1] += count
				#print mics
					
		else:
			#if mics > timeout:
			if timeout == 1:
				#data_dict[index] = {'time':[0, 0],'timeout':[micsencod, count]}
				data_dict[index] = {'time':[micsencod, count],'timeout':[micsencod, count]}
			else:
				data_dict[index] = {'time':[micsencod, count],'timeout':[0, 0]}

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
		#timeout = 400000
		
		province_pv = {}
		
		all_cost_time = {}
		machine_cost_time = {}
		region_cost_time = {}

		all_timeout = {}
		machine_timeout = {}
		region_timeout = {}

		free_count = 0

		try:
			
			for line in data:
				#if line[2] == u'' or not str(line[2]).isalnum():
				#	continue
				#province_code = int(line[3])/100*100
				#ip = str(line[8])
				#cost_time = line[1]
				#region = cls.map_region(ip)

				count = line[0]
				pid = line[1]
				cost_time = line[2]
				timeout = line[3]
				ip = str(line[6])
				region = cls.map_region(ip)


				#if pid != u'__free' and cost_time < u'100000000':
				#print pid
				#if pid != u'__free':
				if pid == 1:
				#if pid == 1 and cost_time < u'100000000':
					all_cost_time = cls.merge_data('all', all_cost_time, cost_time, timeout, count)
					machine_cost_time = cls.merge_data(ip, machine_cost_time, cost_time, timeout, count)
					region_cost_time = cls.merge_data(region, region_cost_time, cost_time, timeout, count)
				else:
					free_count += 1
			#logging.info("free_count: %d"%(free_count,))
		except IndexError as err:
			logging.error(err)
	

		'''总平均响应时间、总超时的平均时间、总超时率、总超时数量'''

		#logging.info(all_cost_time['all'])
		try:
			all_avgtime = cls.calculation_avgtime(all_cost_time['all']['time'])
		except KeyError as err:
			logging.error("all time is zero[%s]"%(err,))
			all_avgtime = 0

		ws_server_time.labels('all', 'all', 'all', 'avgtime').set(all_avgtime)

		try:
			all_avg_timeout = cls.calculation_avgtime(all_cost_time['all']['timeout'])
		except KeyError as err:
			logging.error("all timeout is zero[%s]"%(err,))
			all_avg_timeout = 0

		ws_server_time.labels('all', 'all', 'all', 'avg_timeout').set(all_avg_timeout)

		#print all_cost_time
		all_timeout_count = all_cost_time['all']['timeout'][1]
		ws_server_time.labels('all', 'all', 'all', 'timeout_count').set(all_timeout_count)

		#all_timeout_rate = round(all_timeout_count/(all_timeout_count+all_cost_time['all']['time'][1])*100, 2)
		all_timeout_rate = round(all_timeout_count*1.0/(all_cost_time['all']['time'][1]), 6)*100
		ws_server_time.labels('all', 'all', 'all', 'timeout_rate').set(all_timeout_rate)


		'''分机器平均响应时间、分机器超时的平均时间、分机器超时率、分机器超时数量'''
		for h in machine_cost_time.keys():
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_avgtime = cls.calculation_avgtime(machine_cost_time[h]['time'])
			except KeyError as err:
				logging.error("machine time is zero[%s]"%(err,))
				machine_avgtime = 0

			ws_server_time.labels(region, province, ip, 'avgtime').set(machine_avgtime)


			try:
				machine_avg_timeout = cls.calculation_avgtime(machine_cost_time[h]['timeout'])
			except KeyError as err:
				logging.error("machine timeout is zero[%s]"%(err,))
				machine_avg_timeout = 0
			ws_server_time.labels(region, province, ip, 'avg_timeout').set(machine_avg_timeout)

			machine_timeout_count = machine_cost_time[h]['timeout'][1]
			ws_server_time.labels(region, province, ip, 'timeout_count').set(machine_timeout_count)
		
			machine_timeout_rate = round(machine_timeout_count*1.0/(machine_timeout_count+machine_cost_time[h]['time'][1])*100, 2)
			ws_server_time.labels(region, province, ip, 'timeout_rate').set(machine_timeout_rate)

		'''分机房平均响应时间、分机房超时的平均时间、分机房超时率、分机房超时数量'''
		for r in region_cost_time.keys():
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_avgtime = cls.calculation_avgtime(region_cost_time[r]['time'])
			except KeyError as err:
				logging.error("region time is zero[%s]"%(err,))
				region_avgtime = 0

			ws_server_time.labels(region, province, ip, 'avgtime').set(region_avgtime)


			try:
				region_avg_timeout = cls.calculation_avgtime(region_cost_time[r]['timeout'])
			except KeyError as err:
				logging.error("region timeout is zero[%s]"%(err,))
				region_avg_timeout = 0
			ws_server_time.labels(region, province, ip, 'avg_timeout').set(region_avg_timeout)

			region_timeout_count = region_cost_time[r]['timeout'][1]
			ws_server_time.labels(region, province, ip, 'timeout_count').set(region_timeout_count)
		
			region_timeout_rate = round(region_timeout_count*1.0/(region_cost_time[r]['time'][1]+region_timeout_count)*100, 2)
			ws_server_time.labels(region, province, ip, 'timeout_rate').set(region_timeout_rate)



		#for p in province_pv:
		#	region = 'unkown'
		#	ip = 'unkown'
		#	province = p
		#	province_cov = cls.calculation_cov(province_pv[p])
		#	ws_server_cov.labels(region, province, ip).set(province_cov)
		#	






	@classmethod
	def ws_channel_time(cls, data):
		cov = 0
		channel_cost_time = {}
		industry_cost_time = {}
		free_count = 0
		channel1 = 'unkown'
		channel2 = 'unkown'
		industry = 'unkown'

		channel_map = {
						'302': 'qq',
					   	'303': 'sogou',
					   	'304': 'waigou'
					  }
		industry_map={
						'203':'merchants',
						'204':'it',
						'208':'medical',
						'216':'ecommerce'
		}

		try:
			
			for line in data:
				count = line[0]
				pid = line[1]
				cost_time = line[2]
				timeout = line[3]
				ch_index = line[7]
				indus_index = line[4]

				if pid == 1:
					if ch_index in channel_map.keys():
						channel_cost_time = cls.merge_data(ch_index, channel_cost_time, cost_time, timeout, count)
					if indus_index in industry_map.keys():
						industry_cost_time = cls.merge_data(indus_index, industry_cost_time, cost_time, timeout, count)
				else:
					free_count += 1
		except IndexError as err:
			logging.error(err)
	


		'''分渠道平均响应时间、分渠道超时的平均时间、分渠道超时率、分渠道超时数量'''
		for ch in channel_cost_time.keys():
			
			try:
				channel1 = channel_map[ch]
			except IndexError as err:
				logging.error('[IndexError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'
			except KeyError as err:
				logging.error('[KeyError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'


			try:
				channel_avgtime = cls.calculation_avgtime(channel_cost_time[ch]['time'])
			except KeyError as err:
				logging.error("channel time is zero[%s]"%(err,))
				channel_avgtime = 0

			ws_channel_time.labels(channel1, channel2, 'avgtime', industry).set(channel_avgtime)


			try:
				channel_avg_timeout = cls.calculation_avgtime(channel_cost_time[ch]['timeout'])
			except KeyError as err:
				logging.error("channel timeout is zero[%s]"%(err,))
				channel_avg_timeout = 0
			ws_channel_time.labels(channel1, channel2, 'avg_timeout', industry).set(channel_avg_timeout)

			channel_timeout_count = channel_cost_time[ch]['timeout'][1]
			ws_channel_time.labels(channel1, channel2, 'timeout_count', industry).set(channel_timeout_count)
		
			channel_timeout_rate = round(channel_timeout_count*1.0/(channel_timeout_count+channel_cost_time[ch]['time'][1])*100, 2)
			ws_channel_time.labels(channel1, channel2, 'timeout_rate', industry).set(channel_timeout_rate)




		'''分行业平均响应时间、分行业超时的平均时间、分行业超时率、分行业超时数量'''
		channel1 = 'unkown'
		channel2 = 'unkown'
		for indus in industry_cost_time.keys():
			
			try:
				industry = industry_map[indus]
			except IndexError as err:
				logging.error('[IndexError] industry is not exist.[{}]'.format(err))
				industry = 'unkown'
			except KeyError as err:
				logging.error('[KeyError] industry is not exist.[{}]'.format(err))
				industry = 'unkown'


			try:
				industry_avgtime = cls.calculation_avgtime(industry_cost_time[indus]['time'])
			except KeyError as err:
				logging.error("industry time is zero[%s]"%(err,))
				industry_avgtime = 0

			ws_channel_time.labels(channel1, channel2, 'avgtime', industry).set(industry_avgtime)


			try:
				industry_avg_timeout = cls.calculation_avgtime(industry_cost_time[indus]['timeout'])
			except KeyError as err:
				logging.error("industry timeout is zero[%s]"%(err,))
				industry_avg_timeout = 0
			ws_channel_time.labels(channel1, channel2, 'avg_timeout', industry).set(industry_avg_timeout)

			industry_timeout_count = industry_cost_time[indus]['timeout'][1]
			ws_channel_time.labels(channel1, channel2, 'timeout_count', industry).set(industry_timeout_count)
		
			industry_timeout_rate = round(industry_timeout_count*1.0/(industry_timeout_count+industry_cost_time[indus]['time'][1])*100, 2)
			ws_channel_time.labels(channel1, channel2, 'timeout_rate', industry).set(industry_timeout_rate)
