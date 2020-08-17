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



class MonitorWSBCASN(object):


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
	def merge_pv(cls, index, pv_dict, ad_num, count):

		if index in pv_dict.keys():
			if ad_num > 0:
				pv_dict[index][0] += count*ad_num
			pv_dict[index][1] += count
				
		else:
			if ad_num > 0:
				pv_dict[index] = [count*ad_num, count]
			else:
				pv_dict[index] = [0, count]

		return pv_dict


	@classmethod
	def map_region(cls, ip):
		'''
		#region = 'unkown'
		if ip in ws_server_bc_bj:
			region = 'ws_server_bc_bj'
		else:
			region = 'unkown'
			#logging.info("unkown: %s" % (ip,))
		'''	
		
		#if ip in ws_server_bc.keys():
		#	region = ws_server_bc[ip]
		#else:
		#	region = 'unkown'
		#return region

 		ip_prefix=".".join(ip.split(".")[0:2])
 		try:
 			region = "ws_server_bc_{}".format(region_list[ip_prefix])
 		except IndexError as err:
 			logging.error(err)
 			region = 'unkown'

 		return region

	@classmethod
	def wsbc_asn(cls, wsielog):
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
				ad_num = line[3]
				ip = str(line[4])
				region = cls.map_region(ip)

				machine_pv = cls.merge_pv(ip, machine_pv, ad_num, count)
				region_pv = cls.merge_pv(region, region_pv, ad_num, count)

		except IndexError as err:
			logging.error(err)



		for h in machine_pv.keys():
			ip = h
			region = cls.map_region(ip)
			province = 'unkown'

			try:
				machine_asn = cls.calculation_asn(machine_pv[h])

			except KeyError as err:
				logging.error("machine pv is zero[%s]"%(err,))
				machine_asn = 0



			ws_bc_server_asn.labels(region, province, ip, 'unkown').set(machine_asn)



		for r in region_pv:
			region = r
			ip = 'unkown'
			province = 'unkown'
			try:
				region_asn = cls.calculation_asn(region_pv[r])

			except KeyError as err:
				logging.error("region pv is zero[%s]"%(err,))
				region_asn = 0

			ws_bc_server_asn.labels(region, province, ip, 'unkown').set(region_asn)



