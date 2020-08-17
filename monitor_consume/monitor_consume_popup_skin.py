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



class MonitorPopUpSkinConsume(object):

	code_site = ['2174', '2175', '2190']

	@classmethod
	def popupskin_channel_content(cls, data):
		
		skin_content_consume = 0
		try:
			for line in data:
				#logging.info("{} {}".format(line[13], line[10]))
				if (line[13] in cls.code_site) and (line[10] == 'APPImageText'):
					skin_content_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			skin_content_consume = 0
		skin_channel_consume.labels('skin_channel_content', '0.0.0.0').set(skin_content_consume/100.0)


	@classmethod
	def popupskin_channel_zhitou(cls, data):
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_info_stream')
		skin_zhitou_consume = 0
		try:
			for line in data:
				if (line[10] == 'DirectInvest') and (line[9] == 'APPImageText'):
					if line[13] in cls.code_site:
						skin_zhitou_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			skin_zhitou_consume = 0
		skin_channel_consume.labels('skin_channel_zhitou', '0.0.0.0').set(skin_zhitou_consume/100.0)

