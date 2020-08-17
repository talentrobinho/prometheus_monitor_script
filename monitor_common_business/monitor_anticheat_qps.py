#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-01-16 14:46:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_cm_conf import *
from monitor_cm_conndb import ConnRedis
import logging
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorAnticheatQPS(object):

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
	def anticheat_qps(cls, data, interval):
		#city_code_map = None
		#city_code_map = cls.fetch_city_map()
		total_cd_click = 0
		pass_cd_click = 0
		total_qps = 0
		total_pass_qps = 0
		cd_click = {}
		region = 'UNKOWN'
		business_list = {'1':'PS',
						 '2':'PU',
						 '3':'WS',
						 '5':'WU',
						 '6':'PG',
						 '7':'WG',
						 '8':'IP'}
		try:
			for line in data:
				
				subnet = ".".join(line[10].split(".")[0:2])
				try:
					region = region_list[subnet]
				except IndexError as err:
					logging.error(err)
					region = 'UNKOWN'
				#line[2]=ret
				#line[9]=service
				info_key = "{}_{}_{}_{}".format(region,line[10],line[2],business_list[line[9][0]])
				if info_key in cd_click.keys():
					cd_click[info_key] += 1
				else:
					cd_click[info_key] = 1
		except IndexError as err:
			logging.error(err)
		#['service', 'region', 'ip', 'business', 'is_pass', 'level', 'error_type']	
		for info in cd_click.keys():
			info_list = info.split("_")
			#logging.info(cd_click[info])
			cd_qps = cd_click[info]/interval
			
			region = info_list[0]
			ip = info_list[1]
			ret = info_list[2]
			business = info_list[3]

			total_cd_click += cd_click[info]
			if int(ret) == 0:
				pass_cd_click += cd_click[info]
			cm_server_qps.labels('anticheat', region, ip, business, ret, 'UNKOWN', 'UNKOWN' ).set(cd_qps)
		
		total_qps = total_cd_click/interval
		total_pass_qps = pass_cd_click/interval
		cm_server_qps.labels('anticheat', region, ip, 'total', 'UNKOWN', 'UNKOWN', 'UNKOWN' ).set(total_qps)
		cm_server_qps.labels('anticheat', region, ip, 'total_pass', 'UNKOWN', 'UNKOWN', 'UNKOWN' ).set(total_pass_qps)

