#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:00
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import start_http_server
from monitor_conndb import Base
import logging
import time
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSBase(Base):

	@classmethod
	def fetch_data(cls, sec):
    
		interval = sec
		now_sec = int(time.time())
		end_time_sec = now_sec - now_sec % interval
		start_time_sec = end_time_sec - interval
	
		SQL_SELECT = "SELECT pid, \
							 cost, \
							 business, \
							 city_region, \
							 keyword_industry, \
							 idmap, \
							 ad_num, \
							 is_ad_display, \
							 gen_log_ip \
   			                 FROM ws_ie_log"
		SQL_WHERE = "WHERE server_time >= '{}' AND server_time < '{}'".format(start_time_sec,end_time_sec)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
	
		return cls.query_clickhouse(SQL)



	@classmethod
	def start_server(cls, interval, port, offset_sec, func, city_region=0):
		try:
			start_http_server(port)
		except Exception as err:
			logging.error(err)
			sys.exit(1)
		while True:

		    time_str = time.time()
		    now_offset_sec = int(time_str)
		    if now_offset_sec % interval == offset_sec:
		    	data = cls.fetch_data(interval)
				func(data)
		    time.sleep(1)


	@classmethod
	def run(cls):
		pass



        