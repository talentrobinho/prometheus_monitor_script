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



class MonitorUPSQPS(object):

	@classmethod
	def update_qps(cls, data, interval):
		'''
		flag_list = {'service': 'update',
					 'region': 'bj',
					 'message': 'UNKOWN',
					 'msg_type': 'UNKOWN',
					 'cluster': 'UNKOWN',
					 'ip': 'UNKOWN',
					 'business': 'UNKOWN',
					 'is_pass': 'UNKOWN',
					 'level': 'UNKOWN',
					 'error_type': 'UNKOWN'}
		'''
		flag_list = {
						'service': 'update',
					 	'region': 'bj',
					 	'message': 'UNKOWN',
					 	'msg_type': 'UNKOWN',
					 	'cluster': 'UNKOWN',
					 	'message_status': 'UNKOWN',
					 	'ip': 'UNKOWN'
					 }
		message = {}
		msg_type = {}
		cluster = {}
		server = {}
		logging.info('######'*20)
		logging.info(data)
		#city_code_map = None
		#city_code_map = cls.fetch_city_map()
		try:
			for line in data:
				flag_list['message'] = line[1]
				flag_list['msg_type'] = line[2]
				flag_list['cluster'] = line[3]
				flag_list['message_status'] = line[4]
				flag_list['ip'] = line[5]
				#qps = round(int(line[0])*1.0/interval, 2)
				qps = int(line[0])
				#print flag_list
				update_server_qps.labels(flag_list['service'],
										 flag_list['region'],
										 flag_list['ip'],
										 flag_list['message'],
										 flag_list['msg_type'],
										 flag_list['message_status'],
										 flag_list['cluster']).set(qps)

		except IndexError as err:
			logging.error(err)

		#['service', 'region', 'ip', 'business', 'is_pass', 'level', 'error_type']




