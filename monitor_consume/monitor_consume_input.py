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



class MonitorInputConsume(object):


	@classmethod
	def input_channel_tongtou(cls, data):

		tongtou_consume = 0
		try:
			for line in data:
				if line[1] == 'sogou-apps-c64e7fcb17df2cd4':
					if line[8] == 'INMethod' and line[9] == 'InputStream':
						tongtou_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			tongtou_consume = 0
		input_channel_consume.labels('input_channel_tongtou', '0.0.0.0').set(tongtou_consume/100.0)


	@classmethod
	def input_channel_inputstream(cls, data):

		inputstream_consume = 0
		try:
			for line in data:
				if line[8] == 'INMethod' and line[9] == 'InputStream':
					inputstream_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			inputstream_consume = 0
		input_channel_consume.labels('input_channel_inputstream', '0.0.0.0').set(inputstream_consume/100.0)

	

	@classmethod
	def input_channel_direct(cls, data):

		direct_consume = 0
		try:
			for line in data:
				if line[8] == 'INMethod' and line[9] == 'DIRECT':
					direct_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			direct_consume = 0
		input_channel_consume.labels('input_channel_direct', '0.0.0.0').set(direct_consume/100.0)


	@classmethod
	def input_channel_recomm(cls, data):

		recomm_consume = 0
		try:
			for line in data:
				if line[8] == 'INMethod' and line[9] == 'PreSearchRecomm':
					recomm_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			recomm_consume = 0
		input_channel_consume.labels('input_channel_recomm', '0.0.0.0').set(recomm_consume/100.0)



	@classmethod
	def input_channel_guang(cls, data):

		guang_consume = 0
		try:
			for line in data:
				if line[8] == 'INMethod' and line[9] == 'ChatAndGuang':
					guang_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			guang_consume = 0
		input_channel_consume.labels('input_channel_guang', '0.0.0.0').set(guang_consume/100.0)


