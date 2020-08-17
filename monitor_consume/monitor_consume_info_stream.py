#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_consume_conndb import ConnRedis
from monitor_consume_conf import *
import logging


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorInfoStreamConsume(object):

	@classmethod
	def infostream_channel_content(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		info_content_consume = 0
		try:
			for line in data:
				if (line[1] in pid_list) and (line[10] in ['WapImageText', 'APPImageText']):
					info_content_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			info_content_consume = 0
		info_channel_consume.labels('info_channel_content', '0.0.0.0').set(info_content_consume/100.0)


	@classmethod
	def infostream_channel_searchkey(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		info_sk_consume = 0
		try:
			for line in data:
				if (line[1] in pid_list) and (line[10] in ['SearchKey', 'APPSearchKey']):
					info_sk_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			info_sk_consume = 0
		info_channel_consume.labels('info_channel_searchkey', '0.0.0.0').set(info_sk_consume/100.0)


	@classmethod
	def infostream_channel_zhitou(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		info_zhitou_consume = 0
		try:
			for line in data:
				if (line[1] in pid_list) and (line[10] in ['DirectInvest', 'DirectInvestAPP']):
					info_zhitou_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			info_zhitou_consume = 0
		info_channel_consume.labels('info_channel_zhitou', '0.0.0.0').set(info_zhitou_consume/100.0)

