#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)


import logging
from monitor_consume_conf import *

logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSConsume(object):

	'''==============================================================='''
	'''========================== 按渠道统计 ==========================='''
	'''==============================================================='''

	@classmethod
	def ws_channel_consume_filter(cls, line, flag):
		consume = 0
		try:
			if flag == 'Total' and line[8] == u'WSSearch':
				consume = int(line[0])
			elif line[9] == flag:
				consume = int(line[0])
		except IndexError as err:
			logging.error(err)
			consume = 0
		return consume


	@classmethod
	def ws_channel(cls, data):
		qq_consume = 0
		waigou_consume = 0
		sogou_consume = 0
		total_consume = 0
		other_consume = 0

		for line in data:
			qq_consume += cls.ws_channel_consume_filter(line, 'QQ')
			waigou_consume += cls.ws_channel_consume_filter(line, 'WaiGou')
			sogou_consume += cls.ws_channel_consume_filter(line, 'ZiYou')
			total_consume += cls.ws_channel_consume_filter(line, 'Total')
			total_consume_s += cls.ws_channel_consume_total(line)

		other_consume = total_consume - qq_consume - waigou_consume - sogou_consume
		ws_channel_consume.labels('ws_channel_sogou', '0.0.0.0').set(sogou_consume/100.0)
		ws_channel_consume.labels('ws_channel_qq', '0.0.0.0').set(qq_consume/100.0)
		ws_channel_consume.labels('ws_channel_waigou', '0.0.0.0').set(waigou_consume/100.0)
		ws_channel_consume.labels('ws_channel_other', '0.0.0.0').set(other_consume/100.0)
		ws_channel_consume.labels('ws_channel_total', '0.0.0.0').set(total_consume/100.0)

			
	'''==============================================================='''
	'''========================== 按账户统计 ==========================='''
	'''==============================================================='''

	@classmethod
	def ws_acccount_consume_filter(cls, line, flag):
		consume = 0
		try:
			if line[12] == flag and line[9] in ['QQ', 'WaiGou', 'ZiYou']:
				consume = int(line[0])
		except IndexError as err:
			logging.error(err)
			consume = 0
		return consume

	@classmethod
	def ws_account(cls, data):
		local_account_consume = 0
		other_account_consume = 0

		for line in data:
			local_account_consume += cls.ws_acccount_consume_filter(line, 'LOCAL')
			other_account_consume += cls.ws_acccount_consume_filter(line, 'CHANNEL')


		ws_account_consume.labels('ws_account_local', '0.0.0.0').set(local_account_consume/100.0)
		ws_account_consume.labels('ws_account_other', '0.0.0.0').set(other_account_consume/100.0)
	
		
	'''==============================================================='''
	'''=========================== 按行业统计 =========================='''
	'''==============================================================='''
	@classmethod
	def ws_industry_consume_filter(cls, line, flag):
		consume = 0
		try:
			if line[6].startswith(flag):
				consume = int(line[0])
		except IndexError as err:
			logging.error(err)
			consume = 0
		return consume



	@classmethod
	def ws_industry(cls, data):
		merchants_consume = 0
		it_consume = 0
		medical_consume = 0
		ecommerce_consume = 0
		for line in data:
			'''招商'''
			merchants_consume += cls.ws_industry_consume_filter(line, '203')

			'''IT'''
			it_consume += cls.ws_industry_consume_filter(line, '204')

			'''医疗'''
			medical_consume += cls.ws_industry_consume_filter(line, '208')

			'''电子商务'''
			ecommerce_consume += cls.ws_industry_consume_filter(line, '216')


		ws_industry_consume.labels('ws_industry_merchants', '0.0.0.0').set(merchants_consume/100.0)
		ws_industry_consume.labels('ws_industry_it', '0.0.0.0').set(it_consume/100.0)
		ws_industry_consume.labels('ws_industry_medical', '0.0.0.0').set(medical_consume/100.0)
		ws_industry_consume.labels('ws_industry_ecommerce', '0.0.0.0').set(ecommerce_consume/100.0)




	'''==============================================================='''
	'''======================== 按机器和机房统计 ========================'''
	'''==============================================================='''


	@classmethod
	def ws_server_consume_merge(cls, data):
		server_consume = {}
		for line in data:
			ip = str(line[3])
			try:
				if str(line[8]) == 'WSSearch':
					if ip in server_consume.keys():
						server_consume[ip] += int(line[0])
					else:
						server_consume[ip] = int(line[0])
			except IndexError as err:
				logging.error(err)
		return server_consume


	@classmethod
	def ws_server_consume_submit(cls, server_list, consume_list, flag):
		for ip in server_list:
			if ip in consume_list.keys():
				ws_server_consume.labels(flag, ip).set(consume_list[ip]/100.0)

	@classmethod
	def ws_server(cls, data):
		server_consume_list = cls.ws_server_consume_merge(data)
		cls.ws_server_consume_submit(ws_server_bj_sk, server_consume_list, 'ws_server_bj_sk')
		cls.ws_server_consume_submit(ws_server_bj, server_consume_list, 'ws_server_bj')
		cls.ws_server_consume_submit(ws_server_gd, server_consume_list, 'ws_server_gd')
		cls.ws_server_consume_submit(ws_server_js, server_consume_list, 'ws_server_js')
		cls.ws_server_consume_submit(ws_server_bc_bj, server_consume_list, 'ws_server_bc_bj')
		cls.ws_server_consume_submit(ws_server_lk_bj, server_consume_list, 'ws_server_lk_bj')


	'''==============================================================='''
	'''========================== 按位置统计 ==========================='''
	'''==============================================================='''



	@classmethod
	def ws_adpos_consume_filter(cls, line, pos_list):
		consume = 0
		reserved = line[15]
		if str(line[8]) == 'WSSearch':
			for id_pos in reserved.split(','):
				pos = (int(id_pos) >> 1 & 15)
				if pos in pos_list:
					consume += int(line[0])
				else:
					consume = 0

		return consume

	@classmethod
	def ws_adpos(cls, data):
		midad_consume = 0
		midad_pos_list = {8, 9}

		for line in data:
			midad_consume += cls.ws_adpos_consume_filter(line, midad_pos_list)


		ws_adpos_consume.labels('ws_adpos_midad', '0.0.0.0').set(midad_consume/100.0)

