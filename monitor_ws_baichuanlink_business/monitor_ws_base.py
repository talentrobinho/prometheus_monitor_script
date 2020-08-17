#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:00
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import start_http_server
from monitor_ws_conndb import Base
from threading import Thread
import logging
import time
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)


def async(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()
	return wrapper


class MonitorWSBase(Base):

	@classmethod
	def fetch_ws_bc_ie_log(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT count(), \
   							 if(multiMatchAny(pid, ['__free']),0,1) AS pid_flag, \
	   						 front_query_type, \
	   						 ad_number, \
	   						 gen_log_ip \
					  FROM realtime.ws_bc_ie_log_all"

   		GROUP = "GROUP BY (ad_number, gen_log_ip, front_query_type, pid_flag)"
		SQL_WHERE = "WHERE time >= '{}' AND time < '{}' {}".format(start_time_sec, end_time_sec, GROUP)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
		
		return cls.query_clickhouse(SQL, 'cluster')	

	@classmethod
	def fetch_ws_lk_ie_log(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT count(), \
   							 if(multiMatchAny(pid, ['__free']),0,1) AS pid_flag, \
	   						 front_query_type, \
	   						 ad_number, \
	   						 gen_log_ip \
					  FROM realtime.ws_lk_ie_log_all"

   		GROUP = "GROUP BY (ad_number, gen_log_ip, front_query_type, pid_flag)"
		SQL_WHERE = "WHERE time >= '{}' AND time < '{}' {}".format(start_time_sec, end_time_sec, GROUP)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
		
		return cls.query_clickhouse(SQL, 'cluster')	

	@classmethod
	def start_server(cls, interval, port, offset_sec, func):
		try:
			start_http_server(port)
		except Exception as err:
			logging.error(err)
			sys.exit(1)


		while True: 
		    now_offset_sec = int(time.time())
		    
		    if now_offset_sec % interval == 0:
		    	
		    	if interval == offset_sec:
		    		end_sec = now_offset_sec - offset_sec
		    		start_sec = end_sec - interval
		    	else:
		    		time.sleep(offset_sec)
		    		end_sec = now_offset_sec
		    		start_sec = end_sec - interval

		    	#ws_bc_ie_log_data = []
		    	ws_bc_ie_log_data = cls.fetch_ws_bc_ie_log(start_sec, end_sec)
		    	ws_lk_ie_log_data = cls.fetch_ws_lk_ie_log(start_sec, end_sec)
		    	
		    	func(interval, ws_bc_ie_log_data, ws_lk_ie_log_data)
		    	#func(interval, start_sec, end_sec)

		    time.sleep(1)



	@classmethod
	def run(cls):
		pass



        