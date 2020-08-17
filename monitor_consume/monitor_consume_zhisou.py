#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-06 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_consume_conf import *
import logging


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)


#split($66,its,",");if(its[4]~/30037|30038|30039/){print $0}
#accountid 20592426
class MonitorWSZHiSouConsume(object):


	@classmethod
	def ws_zhisou(cls, data):
		'''无线智叟消耗'''
		zhisou_consume = 0
		try:
			for line in data:
				#if line[8] != u'WSSearch':
				#	continue
				#item = line[7].split(',')
				#if len(item) >= 3:
				#	if item[3] in ['30037', '30038', '30039']:
				#		zhisou_consume += int(line[0])
				#print "{} {}".format(line[14], '20592426')
				if line[14] == '20592426' or line[16] == u'商品推广计费关键词-请勿删除':
					#logging.info(line[16])
					zhisou_consume += int(line[0])

		except IndexError as err:
			logging.error(err)
			zhisou_consume = 0
		zhisou_channel_consume.labels('zhisou_channel_zhisou', '0.0.0.0').set(zhisou_consume/100.0)
