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



class MonitorWSQPS(object):

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
	def ws_qps(cls, data, interval):
		city_code_map = None
		qps_dict = {}
		city_code_map = cls.fetch_city_map()
		#print data
		try:
			for line in data:

				#province_code = int(line[3])/100*100
				#index="{}_{}_{}".format(line[8], province_code, line[3])
				#index="{}_{}".format(line[8], province_code)
				count = line[0]
				ad_num = line[5]
				index = line[6]
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
				#print line
			#print qps_dict
		except IndexError as err:
			logging.error(err)
		#sys.exit(1)
		#print qps_dict
		#logging.info(qps_dict)
		for ip in qps_dict.keys():
			province = 'unkown'
			#ip = k.split('_')[0]
			#try:
			#	#city = city_code_map[k.split('_')[2]]
			#	province = city_code_map[k.split('_')[1]]
			#except Exception as err:
			#	logging.error("Find city_code_map error[%s]"%(err,))

			qps = qps_dict[ip][0]/interval
			qps2 = qps_dict[ip][1]/interval
			qps3 = qps_dict[ip][2]/interval

			region = 'unkown'
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
			#ws_server_qps.labels(region, province, city, ip).set(qps)
			ws_server_qps.labels(region, province, ip).set(qps)
			ws_server_qps1.labels(region, province, ip, '1').set(qps)
			ws_server_qps1.labels(region, province, ip, '2').set(qps2)
			ws_server_qps1.labels(region, province, ip, '3').set(qps3)
			#print "region: {}   province: {}  ip: {}   qps: {}".format(region, province, ip, qps)




	@classmethod
	def ws_channel_qps(cls, data, interval):
		ch_qps_dict = {}
		channel1 = 'unkown'
		channel2 = 'unkown'
		industry = 'unkown'
		channel_map = {
						'302': 'qq',
					   	'303': 'sogou',
					   	'304': 'waigou'
					  }
		'''
		industry_map={
						'203':'merchants',
						'204':'it',
						'208':'medical',
						'216':'ecommerce'
		}
		'''
		for line in data:
			try:
				count = line[0]
				ad_num = line[5]
				ch_index = line[7]
				#logging.info("business: {}".format(index))
			except IndexError as err:
				logging.error(err)

			if ad_num > 0:
				is_ad = 1
			else:
				is_ad = 0
			'''按渠道统计QPS'''
			if ch_index in channel_map.keys():

				if ch_index in ch_qps_dict.keys():
					ch_qps_dict[ch_index][0] += count
					ch_qps_dict[ch_index][1] += ad_num
					ch_qps_dict[ch_index][2] += is_ad
				else:
					ch_qps_dict[ch_index] = [count, ad_num, is_ad]


		for ch in ch_qps_dict.keys():
			qps1 = ch_qps_dict[ch][0]/interval
			qps2 = ch_qps_dict[ch][1]/interval
			qps3 = ch_qps_dict[ch][2]/interval

			try:
				channel1 = channel_map[ch]
			except IndexError as err:
				logging.error('[IndexError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'
			except KeyError as err:
				logging.error('[KeyError] channel is not exist.[{}]'.format(err))
				channel1 = 'unkown'

			ws_channel_qps.labels(channel1, channel2, '1', industry).set(qps1)
			ws_channel_qps.labels(channel1, channel2, '2', industry).set(qps2)
			ws_channel_qps.labels(channel1, channel2, '3', industry).set(qps3)
