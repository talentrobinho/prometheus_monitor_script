#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)


'''系统类'''
from prometheus_client import start_http_server
import threading
import logging
import os
import time
import sys

'''自定义监控指标类'''
from monitor_ws_conf import *
from monitor_ws_base import MonitorWSBase
from monitor_ws_bc_qps import *
from monitor_ws_bc_cov import *
from monitor_ws_bc_asn import *
from monitor_ws_lk_qps import *
from monitor_ws_lk_cov import *
from monitor_ws_lk_asn import *



'''日志配置'''
logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorWSBusiness(MonitorWSBCQPS,
						MonitorWSBCCOV,
						MonitorWSBCASN,
						MonitorWSLKQPS,
						MonitorWSLKCOV,
						MonitorWSLKASN,
					 	MonitorWSBase):


	@classmethod
	def ws_business(cls, interval, wsbc_ielog, wslk_ielog):
	#def ws_business(cls, interval, start_sec, end_sec):
		#wsielog = MonitorWSBase.fetch_ws_ie_log(start_sec, end_sec)
		#cdielog = MonitorWSBase.fetch_cd_ie_log(start_sec, end_sec)
		if wsbc_ielog is None:
			logging.error("wsielog data set is Null")
			return False
		elif wslk_ielog is None:
			logging.error("wsielog data set is Null")
			return False
		'''============================ MonitorWSBusiness ==============================='''
		#if interval == 10:
		threading.Thread(target=MonitorWSBCQPS.wsbc_qps, args=(wsbc_ielog,interval)).start()
		threading.Thread(target=MonitorWSBCCOV.wsbc_cov, args=(wsbc_ielog,)).start()
		threading.Thread(target=MonitorWSBCASN.wsbc_asn, args=(wsbc_ielog,)).start()

		threading.Thread(target=MonitorWSLKQPS.wslk_qps, args=(wslk_ielog,interval)).start()
		threading.Thread(target=MonitorWSLKCOV.wslk_cov, args=(wslk_ielog,)).start()
		threading.Thread(target=MonitorWSLKASN.wslk_asn, args=(wslk_ielog,)).start()

	@staticmethod
	def run(interval, port, offset_sec):
		MonitorWSBase.start_server(interval, port, offset_sec, MonitorWSBusiness.ws_business)



import socket
def IsOpen(port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect(('0.0.0.0',int(port)))
		s.shutdown(2)
		#利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
		#该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
		logging.error('%d is open' % port)
		return True
	except:
		return False



if __name__ == '__main__':

	offset_sec = 30
	if len(sys.argv) > 1:
		try:
			interval = int(sys.argv[1])
			port = int(sys.argv[2])

			if interval < 10:
				logging.error("interval is err[10s, 60s, 300s, ...].")
				sys.exit(1)
			elif interval < offset_sec:
				logging.error("interval is smaller than offset_sec.[offset_sec: {}; interval: {}]".format(offset_sec, interval))
				sys.exit(1)
		except IndexError:
			logging.error("args is error.[as: %s <interval> <port>]"%(sys.argv[0],))
			sys.exit(1)
		except ValueError:
			logging.error("args type is error.[as: %s 10 9000]"%(sys.argv[0],))
			sys.exit(1)
		
		if not interval in [10, 60, 300]:
			logging.error("interval is err[10s, 60s, 300s, ...].")
			sys.exit(1)
		if port is None or port < 9000:
			logging.error("http port is error[9000+].")
			sys.exit(1)
	else:
		interval = 300
		port = 9000


	'''check port is using'''
	if IsOpen(port):
		sys.exit(1)

	
	#sec = int(time.time())
	#sec_diff = sec % interval
	

	#if sec_diff >= offset_sec:
	#    delay = interval - sec_diff + offset_sec
	#else:
	#    delay = offset_sec - sec_diff	
	#time.sleep(delay)
	#time.sleep(sec_diff)

	pid=os.fork()
	pidfile="{}_{}_{}.pid".format(sys.argv[0].split('.')[0], sys.argv[1], sys.argv[2])
	if pid != 0:
		#logging.info("father pid: {}".format(pid))
		with open(pidfile, 'w') as f:
			f.write("{}".format(pid))
		os._exit(0)
	else:
		#logging.info("daemon pid: {}".format(realpid))
		MonitorWSBusiness.run(interval, port, offset_sec)