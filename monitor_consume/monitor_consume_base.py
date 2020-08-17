#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from multiprocessing import Process, Manager
#from clickhouse_driver import Client
from prometheus_client import Gauge,start_http_server
#from conf import Config
from monitor_consume_conndb import Base
import threading
import logging
import os
import time
import sys
import copy
#import schedule

logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorConsumeBase(Base):

	@classmethod
	def fetch_data(cls, sec):
    
		interval = sec
		now_sec = int(time.time())
		end_time_sec = now_sec - now_sec % interval
		start_time_sec = end_time_sec - interval
	
		SQL_SELECT = "SELECT price, \
   			                 pid, \
   			                 city_code, \
   			                 ip, \
   			                 max_price, \
   			                 planid, \
   			                 kid_indus, \
   			                 eesf, \
   			                 business_level1, \
   			                 business_level2, \
   			                 business_level3, \
   			                 pc_business, \
   			                 account_type, \
   			                 upos_asid, \
   			                 accountid, \
   			                 reserved, \
   			                 keyword, \
   			                 service_type \
   			                 FROM realtime.cd_ie_log"
		SQL_WHERE = "WHERE server_time >= '{}' AND server_time < '{}' AND is_consume_account = 1 AND ret = '0'".format(start_time_sec,end_time_sec)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
	
		return cls.query_clickhouse(SQL)

	@classmethod
	def start_server(cls, interval, port, offset_sec, func):
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



        