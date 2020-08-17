#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)


import logging
from monitor_consume_conf import *

logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorPSConsume(object):

	'''==============================================================='''
	'''========================== 按渠道统计 ==========================='''
	'''==============================================================='''
	@classmethod
	def ps_channel_bc(cls, data):
		bc_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_bc":
					bc_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			bc_consume = 0
		ps_channel_consume.labels('ps_channel_bc', '0.0.0.0').set(bc_consume/100.0)



	@classmethod
	def ps_channel_bd(cls, data):
		bd_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_bd":
					bd_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			bd_consume = 0
		ps_channel_consume.labels('ps_channel_bd', '0.0.0.0').set(bd_consume/100.0)

	@classmethod
	def ps_channel_brws(cls, data):
		brws_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_brws":
					brws_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			brws_consume = 0
		ps_channel_consume.labels('ps_channel_brws', '0.0.0.0').set(brws_consume/100.0)


	@classmethod
	def ps_channel_ime(cls, data):
		ime_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_ime":
					ime_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			ime_consume = 0
		ps_channel_consume.labels('ps_channel_ime', '0.0.0.0').set(ime_consume/100.0)


	@classmethod
	def ps_channel_123(cls, data):
		onetwothree_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_123":
					onetwothree_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			onetwothree_consume = 0
		ps_channel_consume.labels('ps_channel_123', '0.0.0.0').set(onetwothree_consume/100.0)


	@classmethod
	def ps_channel_sogou(cls, data):
		sogou_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_sogou":
					sogou_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			sogou_consume = 0
		ps_channel_consume.labels('ps_channel_sogou', '0.0.0.0').set(sogou_consume/100.0)


	@classmethod
	def ps_channel_sohu(cls, data):
		sohu_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_sohu":
					sohu_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			sohu_consume = 0
		ps_channel_consume.labels('ps_channel_sohu', '0.0.0.0').set(sohu_consume/100.0)



	@classmethod
	def ps_channel_soso(cls, data):
		soso_consume = 0
		try:
			for line in data:
				if line[11] == "pc_channel_soso":
					soso_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			soso_consume = 0
		ps_channel_consume.labels('ps_channel_soso', '0.0.0.0').set(soso_consume/100.0)




	'''==============================================================='''
	'''======================== 按机器和机房统计 ========================'''
	'''==============================================================='''
	@classmethod
	def ps_server_bj_sk(cls, data):

		server_list = ['10.139.21.59',
					   '10.160.64.120']


		for ip in server_list:
			bj_sk_consume = 0
			for line in data:

				try:
					if line[3] == ip and line[8] == 'PCSearch':
						#logging.info("{}-->{}".format(ip, line[3]))
						#logging.info("{}: {}".format('ps_bj', line[3]))
						bj_sk_consume += int(line[0])
				except IndexError as err:
					logging.error(err)
					bj_sk_consume = 0
			ps_server_consume.labels('ps_server_bj_sk', ip).set(bj_sk_consume/100.0)





	@classmethod
	def ps_server_bj(cls, data):

		server_list = ['10.139.20.72',
					   '10.139.20.59',
					   '10.139.36.56',
					   '10.160.64.117',
					   '10.160.64.118',
					   '10.160.64.119']	

		for ip in server_list:
			bj_consume = 0
			for line in data:

				try:
					if line[3] == ip and line[8] == 'PCSearch':
						#logging.info("{}-->{}".format(ip, line[3]))
						#logging.info("{}: {}".format('ps_bj', line[3]))
						bj_consume += int(line[0])
				except IndexError as err:
					logging.error(err)
					bj_consume = 0
			ps_server_consume.labels('ps_server_bj', ip).set(bj_consume/100.0)


	@classmethod
	def ps_server_gd(cls, data):
		
		server_list = ['10.135.73.91',
					   '10.135.73.92',
					   '10.135.73.93']

		for ip in server_list:

			gd_consume = 0
			for line in data:
				
				try:
					if line[3] == ip and line[8] == 'PCSearch':
						#logging.info("{}-->{}".format(ip, line[3]))
						gd_consume += int(line[0])
				except IndexError as err:
					logging.error(err)
					gd_consume = 0
			ps_server_consume.labels('ps_server_gd', ip).set(gd_consume/100.0)


	@classmethod
	def ps_server_js(cls, data):
		
		server_list = ['10.140.11.22',
					   '10.140.11.39',
					   '10.140.19.67']
		
		for ip in server_list:
			js_consume = 0
			for line in data:

				try:
					if line[3] == ip and line[8] == 'PCSearch':
						#logging.info("{}-->{}".format(ip, line[3]))
						js_consume += int(line[0])
				except IndexError as err:
					logging.error(err)
					js_consume = 0
			ps_server_consume.labels('ps_server_js', ip).set(js_consume/100.0)


