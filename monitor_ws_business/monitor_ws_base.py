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
	def fetch_ws_ie_log(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT count(), \
   							 if(multiMatchAny(pid, ['__free']),0,1) AS pid_flag, \
	   						 sum(toUInt32OrZero(cost)), \
	   						 if(toUInt32OrZero(cost)>400000,1,0) AS timeout, \
	   						 if(multiMatchAny(keyword_industry,['^203','^204','^208','^216'])==1,substr(keyword_industry,1,3),'0') AS indus, \
	   						 ad_number, \
	   						 gen_log_ip, \
	   						 substr(business,1,3) AS busi, \
	   						 reserved \
					  FROM realtime.ws_ie_log_all"

   		GROUP = "GROUP BY (ad_number, gen_log_ip, timeout, indus, busi, pid_flag, reserved)"
		SQL_WHERE = "WHERE time >= '{}' AND time < '{}' {}".format(start_time_sec, end_time_sec, GROUP)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
		
		return cls.query_clickhouse(SQL, 'cluster')	


	@classmethod
	def fetch_ws_ie_logG(cls, start_time_sec, end_time_sec):
    	##if(multiMatchAny(pid, [u'__free']),0,1) as pid_flag, \
   		SQL_SELECT = "SELECT 1, \
   							 pid, \
	   						 cost, \
	   						 business, \
	   						 keyword_industry, \
	   						 ad_number, \
	   						 gen_log_ip \
					  FROM realtime.ws_ie_log_all"

   		GROUP = "GROUP BY (ad_number, gen_log_ip, timeout, indus, busi, pid_flag)"
		SQL_WHERE = "WHERE time >= '{}' AND time < '{}'".format(start_time_sec, end_time_sec)
		SQL = "{} {}".format(" ".join(SQL_SELECT.split()), SQL_WHERE)
	
		
		return cls.query_clickhouse(SQL, 'cluster')	





	@classmethod
	def fetch_cd_ie_log(cls, start_time_sec, end_time_sec):
    
		#interval = sec
		#now_sec = int(time.time())
		#end_time_sec = now_sec - now_sec % interval
		#start_time_sec = end_time_sec - interval
	
		SQL_SELECT = "SELECT price, \
   			                 pid, \
   			                 city_code, \
   			                 ip, \
   			                 max_price, \
   			                 planid, \
   			                 kid_indus, \
   			                 eesf, \
   			                 service_type, \
   			                 upos_asid, \
   			                 accountid, \
   			                 business_level1, \
   			                 business_level2, \
   			                 business_level3 \
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
		    now_offset_sec = int(time.time())
		    
		    if now_offset_sec % interval == 0:
		    	
		    	if interval == offset_sec:
		    		end_sec = now_offset_sec - offset_sec
		    		start_sec = end_sec - interval
		    	else:
		    		time.sleep(offset_sec)
		    		end_sec = now_offset_sec
		    		start_sec = end_sec - interval

		    	ws_ie_log_data = cls.fetch_ws_ie_log(start_sec, end_sec)
		    	cd_ie_log_data = cls.fetch_cd_ie_log(start_sec, end_sec)
		    	func(interval, cd_ie_log_data, ws_ie_log_data)
		    	#func(interval, start_sec, end_sec)

		    time.sleep(1)



	@classmethod
	def run(cls):
		pass



        