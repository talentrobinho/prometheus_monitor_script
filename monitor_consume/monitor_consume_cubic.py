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



class MonitorWSCubicConsume(object):

	@classmethod
	def cubic_channel_cubic(cls, data):
		cubic_consume = 0
		try:
			for line in data:
				item = line[7].split(',')
				if len(item) >= 5:
					if item[5] == "103":
						cubic_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			cubic_consume = 0
		cubic_channel_consume.labels('cubic_channel_cubic', '0.0.0.0').set(cubic_consume/100.0)

