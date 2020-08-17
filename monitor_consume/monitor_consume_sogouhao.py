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



class MonitorWSSogouHaoConsume(object):

	@classmethod
	def sogouhao_channel_search(cls, data):
		'''搜狗号详情页消耗'''
		sogouhao_search_consume = 0
		try:
			for line in data:
				item = line[7].split(',')
				if len(item) >= 5:
					if item[5] == "108":
						sogouhao_search_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			sogouhao_search_consume = 0
		sogouhao_channel_consume.labels('sogouhao_channel_search', '0.0.0.0').set(sogouhao_search_consume/100.0)

	@classmethod
	def sogouhao_channel_back(cls, data):
		'''搜狗号回流消耗'''
		sogouhao_back_consume = 0
		sogouhao_pid = ['sogou-waps-3f0c067fa4cac361',
						'sogou-waps-86654aa91382ffa2',
						'sogou-waps-3f2e2a6fcb760125',
						'sogou-waps-185afe2ab60395b0',
						'sogou-waps-a7ba7390e92513e1',
						'sogou-waps-d5542ec466d3f344',
						'sogou-waps-e4017fc196bfb479',
						'sogou-waps-c05c903e3d997add',
						'sogou-waps-03ea906731be85e3',
						'sogou-waps-0b9cc53336c8d4b6',
						'sogou-waps-a412963e013751a9',
						'sogou-waps-0e3e75d3095f3746']
		try:
			for line in data:
				if line[1] in sogouhao_pid:
					sogouhao_back_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			sogouhao_back_consume = 0
		sogouhao_channel_consume.labels('sogouhao_channel_back', '0.0.0.0').set(sogouhao_back_consume/100.0)

