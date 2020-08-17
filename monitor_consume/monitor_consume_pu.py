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



class MonitorPUConsume(object):

	@classmethod
	def pu_channel_content(cls, data):
		union_content_consume = 0
		try:
			for line in data:
				if line[9] == 'THEME':
					union_content_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			union_content_consume = 0
		pu_channel_consume.labels('pu_channel_content', '0.0.0.0').set(union_content_consume/100.0)

	@classmethod
	def pu_channel_searchkey(cls, data):
		union_sk_consume = 0
		try:
			for line in data:
				if line[9] == 'SearchKey':
					union_sk_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			union_sk_consume = 0
		pu_channel_consume.labels('pu_channel_searchkey', '0.0.0.0').set(union_sk_consume/100.0)

