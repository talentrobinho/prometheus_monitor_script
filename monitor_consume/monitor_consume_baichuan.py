#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_consume_conf import *
import logging


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSBaiChuanConsume(object):


	@classmethod
	def baichuan_channel_recomm_below(cls, data):
		'''华章详情页消耗'''
		baichuan_recomm_below_consume = 0
		click_source = {'101'}
		try:
			for line in data:
				item = line[7].split(',')
				if len(item) >= 5:
					if item[5] in click_source:
						baichuan_recomm_below_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			baichuan_recomm_below_consume = 0
		baichuan_channel_consume.labels('baichuan_channel_recomm_below', '0.0.0.0').set(baichuan_recomm_below_consume/100.0)



	@classmethod
	def baichuan_channel_secondary_page(cls, data):
		'''华章详情页消耗'''
		baichuan_secondary_page_consume = 0
		click_source = {'102'}
		try:
			for line in data:
				item = line[7].split(',')
				if len(item) >= 5:
					if item[5] in click_source:
						baichuan_secondary_page_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			baichuan_secondary_page_consume = 0
		baichuan_channel_consume.labels('baichuan_channel_secondary_page', '0.0.0.0').set(baichuan_secondary_page_consume/100.0)


	'''==============================================================='''
	'''======================== 按机器和机房统计 ========================'''
	'''==============================================================='''


	@classmethod
	def ws_bc_server_consume_merge(cls, data):
		server_consume = {}
		for line in data:
			ip = str(line[3])
			try:
				if ip in server_consume.keys():
					server_consume[ip] += int(line[0])
				else:
					server_consume[ip] = int(line[0])
			except IndexError as err:
				logging.error(err)
		return server_consume


	@classmethod
	def ws_bc_server_consume_submit(cls, server_list, consume_list, flag):
		for ip in server_list:
			if ip in consume_list.keys():
				ws_bc_server_consume.labels(flag, ip).set(consume_list[ip]/100.0)

	@classmethod
	def ws_bc_server(cls, data):
		server_consume_list = cls.ws_bc_server_consume_merge(data)
		cls.ws_bc_server_consume_submit(ws_bc_server_bj, server_consume_list, 'ws_bc_server_bj')
