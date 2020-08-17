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



class MonitorWSHuaZhangConsume(object):


	@classmethod
	def huazhang_channel_huazhang(cls, data):
		'''华章详情页消耗'''
		huazhang_search_consume = 0
		click_source = ['109', '110']
		try:
			for line in data:
				item = line[7].split(',')
				if len(item) >= 5:
					if item[5] in click_source:
						huazhang_search_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			huazhang_search_consume = 0
		huazhang_channel_consume.labels('huazhang_channel_huazhang', '0.0.0.0').set(huazhang_search_consume/100.0)
