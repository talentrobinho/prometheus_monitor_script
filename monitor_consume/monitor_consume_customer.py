#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)


from monitor_consume_conndb import ConnRedis
from monitor_consume_conf import *
import logging
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorCustomerConsume(object):


	@classmethod
	def customer_channel_vivo(cls, data):

		vivo_consume = 0
		vivo_local_account_consume = 0
		vivo_other_account_consume = 0
		vivo_indus_consume = {
								'merchants': 0,
								'it': 0,
								'medical': 0,
								'ecommerce': 0,
								'other': 0
							 }
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_vivo')
		try:
			for line in data:
				if line[1] in pid_list:
					vivo_consume += int(line[0])
					if line[6].startswith('203'):
						vivo_indus_consume['merchants']+= int(line[0])
					elif line[6].startswith('204'):
						vivo_indus_consume['it']+= int(line[0])
					elif line[6].startswith('208'):
						vivo_indus_consume['medical']+= int(line[0])
					elif line[6].startswith('216'):
						vivo_indus_consume['ecommerce']+= int(line[0])
					else:
						vivo_indus_consume['other']+= int(line[0])

					if line[12] == 'LOCAL':
						vivo_local_account_consume += int(line[0])
					else:
						vivo_other_account_consume += int(line[0])
					
		except IndexError as err:
			logging.error(err)
			vivo_consume = 0
		bigcustomer_channel_consume.labels('bigcustomer_channel_vivo', 'unknow', '0.0.0.0').set(vivo_consume/100.0)
		bigcustomer_channel_consume.labels('bigcustomer_indus_vivo', 'merchants', '0.0.0.0').set(vivo_indus_consume['merchants']/100.0)
		bigcustomer_channel_consume.labels('bigcustomer_indus_vivo', 'it', '0.0.0.0').set(vivo_indus_consume['it']/100.0)
		bigcustomer_channel_consume.labels('bigcustomer_indus_vivo', 'medical', '0.0.0.0').set(vivo_indus_consume['medical']/100.0)
		bigcustomer_channel_consume.labels('bigcustomer_indus_vivo', 'ecommerce', '0.0.0.0').set(vivo_indus_consume['ecommerce']/100.0)
		bigcustomer_channel_consume.labels('bigcustomer_indus_vivo', 'other', '0.0.0.0').set(vivo_indus_consume['other']/100.0)

		bigcustomer_channel_consume.labels('bigcustomer_account_vivo', 'local_account', '0.0.0.0').set(vivo_local_account_consume/100.0)
		bigcustomer_channel_consume.labels('bigcustomer_account_vivo', 'other_account', '0.0.0.0').set(vivo_other_account_consume/100.0)


	@classmethod
	def customer_channel_oppo(cls, data):

		oppo_consume = 0
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_oppo')
		try:
			for line in data:
				if line[1] in pid_list:
					oppo_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			oppo_consume = 0
		bigcustomer_channel_consume.labels('bigcustomer_channel_oppo', 'unknow', '0.0.0.0').set(oppo_consume/100.0)


	@classmethod
	def customer_channel_mi(cls, data):

		mi_consume = 0
		redis = ConnRedis.conn_redis()
		pid_list = redis.smembers('pid_mi')
		try:
			for line in data:
				if line[1] in pid_list:
					mi_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			mi_consume = 0
		bigcustomer_channel_consume.labels('bigcustomer_channel_mi', 'unknow', '0.0.0.0').set(mi_consume/100.0)


	@classmethod
	def customer_channel_taobao(cls, data):

		taobao_consume = 0
		#low_quality_channel_list = {'30304', '30408', '30409'}
		low_quality_channel_list = {'SogouOther', 'BDS', 'OTHER'}
		redis = ConnRedis.conn_redis()
		account_list = set(redis.smembers('taobao_total'))
		try:
			for line in data:
				if line[14] in account_list:
					taobao_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			taobao_consume = 0
		bigcustomer_channel_consume.labels('bigcustomer_channel_taobao', 'unknow', '0.0.0.0').set(taobao_consume/100.0)


	@classmethod
	def customer_channel_taobaolowquality(cls, data):

		taobao_low_consume = 0
		#low_quality_channel_list = {'30304', '30408', '30409'}
		low_quality_channel_list = {'SogouOther', 'BDS', 'OTHER'}
		redis = ConnRedis.conn_redis()
		account_list = set(redis.smembers('taobao_total'))
		try:
			for line in data:
				if line[14] in account_list and line[10] in low_quality_channel_list:
					taobao_low_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			taobao_low_consume = 0
		bigcustomer_channel_consume.labels('bigcustomer_channel_taobaolowquality', 'unknow', '0.0.0.0').set(taobao_low_consume/100.0)
