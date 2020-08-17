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



class MonitorWUConsume(object):

	@classmethod
	def wu_channel_content(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		wu_content_consume = 0
		try:
			for line in data:
				if (not line[1] in pid_list) and (line[10] in ['WapImageText', 'APPImageText']):
					wu_content_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			wu_content_consume = 0
		wu_channel_consume.labels('wu_channel_content', '0.0.0.0').set(wu_content_consume/100.0)


	@classmethod
	def wu_channel_searchkey(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		wu_sk_consume = 0
		try:
			for line in data:
				if (not line[1] in pid_list) and (line[10] in ['SearchKey', 'APPSearchKey']):
					wu_sk_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			wu_sk_consume = 0
		wu_channel_consume.labels('wu_channel_searchkey', '0.0.0.0').set(wu_sk_consume/100.0)


	@classmethod
	def wu_channel_zhitou(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		wu_zhitou_consume = 0
		try:
			for line in data:
				if (not line[1] in pid_list) and (line[10] in ['DirectInvest', 'DirectInvestAPP']):
					wu_zhitou_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			wu_zhitou_consume = 0
		wu_channel_consume.labels('wu_channel_zhitou', '0.0.0.0').set(wu_zhitou_consume/100.0)

