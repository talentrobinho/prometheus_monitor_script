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



class MonitorPopUpUnskinConsume(object):

	code_site = ['2174', '2175', '2190']
	pid_list = ['sogou_pcsrf_app_a', 'sogou_pcsrf_app_b', 'sogou_pcsrf_app_adp', 'sogou_pcsrf_app_bdp']

	@classmethod
	def popupunskin_channel_content(cls, data):
		
		unskin_content_consume = 0
		try:
			for line in data:
				if (not line[13] in cls.code_site) and (line[10] == 'APPImageText'):
					if line[1] in cls.pid_list:
						unskin_content_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			unskin_content_consume = 0
		unskin_channel_consume.labels('unskin_channel_content', '0.0.0.0').set(unskin_content_consume/100.0)


	@classmethod
	def popupunskin_channel_zhitou(cls, data):

		unskin_zhitou_consume = 0
		try:
			for line in data:
				if (line[10] == 'DirectInvest') and (line[9] == 'APPImageText'):
					if (line[1] in cls.pid_list) and (not line[13] in cls.code_site):
						unskin_zhitou_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			unskin_zhitou_consume = 0
		unskin_channel_consume.labels('unskin_channel_zhitou', '0.0.0.0').set(unskin_zhitou_consume/100.0)

