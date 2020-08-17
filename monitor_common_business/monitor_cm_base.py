#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:00
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import start_http_server
from monitor_cm_conndb import Base
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


class MonitorCMBase(Base):
	#select count(),message,cluster,type from ws_update_update_log where time >= '1579155574' and time < '1579155575' group by (message, cluster, type);
	@classmethod
	def fetch_ups_update_log(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT count(), \
   							 message, \
	   						 type, \
	   						 cluster, \
	   						 message_status, \
	   						 gen_log_ip \
					  FROM realtime.ws_update_update_log_all"

   		GROUP = "GROUP BY (message, type, cluster, message_status, gen_log_ip)"
		SQL_WHERE = "WHERE time >= '{}' AND time < '{}' {}".format(start_time_sec, end_time_sec, GROUP)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
		
		return cls.query_clickhouse(SQL, 'cluster')	

	@classmethod
	def fetch_bill_ie_log(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT count(), \
   							 pid, \
   							 ret, \
   							 service_type, \
	   						 gen_log_ip \
					  FROM realtime.bill_ie_log_all"

   		GROUP = "GROUP BY (pid, ret, service_type, gen_log_ip)"
		SQL_WHERE = "WHERE time >= '{}' AND time < '{}' {}".format(start_time_sec, end_time_sec, GROUP)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
		
		return cls.query_clickhouse(SQL, 'cluster')	

	@classmethod
	def fetch_cd_ie_log(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT pid, \
   							 reserved, \
   							 ret, \
   							 eesf, \
   							 kid_indus, \
   							 account_type, \
   							 upos_asid, \
   			                 accountid, \
   							 keyword, \
   							 service_type, \
	   						 gen_log_ip \
					  FROM realtime.cd_ie_log"

		SQL_WHERE = "WHERE server_time >= '{}' AND server_time < '{}'".format(start_time_sec, end_time_sec)
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
		    now_offset_sec = int(time.time())
		    
		    if now_offset_sec % interval == 0:
		    	
		    	if interval == offset_sec:
		    		end_sec = now_offset_sec - offset_sec
		    		start_sec = end_sec - interval
		    	else:
		    		time.sleep(offset_sec)
		    		end_sec = now_offset_sec
		    		start_sec = end_sec - interval

		    	ups_update_log_data = cls.fetch_ups_update_log(start_sec, end_sec)
		    	bill_ie_log_data = cls.fetch_bill_ie_log(start_sec, end_sec)
		    	cd_ie_log_data = cls.fetch_cd_ie_log(start_sec, end_sec)

		    	func(interval, ups_update_log_data, bill_ie_log_data, cd_ie_log_data)
		    time.sleep(1)



	@classmethod
	def run(cls):
		pass



        