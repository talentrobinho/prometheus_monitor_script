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
from monitor_consume_conf import *
from monitor_consume_base import MonitorConsumeBase
from monitor_consume_sogouhao import *
from monitor_consume_huazhang import *
from monitor_consume_zhisou import *
from monitor_consume_baichuan import *
from monitor_consume_ws import *
from monitor_consume_ps import *
from monitor_consume_zhida import *
from monitor_consume_customer import *
from monitor_consume_input import *
from monitor_consume_pu import *
from monitor_consume_wu import *
from monitor_consume_info_stream import *
from monitor_consume_popup_skin import *
from monitor_consume_popup_unskin import *
from monitor_consume_galaxy import *
from monitor_consume_cubic import *


'''日志配置'''
logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorConsume(MonitorWSSogouHaoConsume, 
					 MonitorWSHuaZhangConsume,
					 MonitorWSConsume,
					 MonitorPSConsume, 
					 MonitorZhiDaConsume,
					 MonitorCustomerConsume,
					 MonitorWSBaiChuanConsume,
					 MonitorInputConsume,
					 MonitorPUConsume,
					 MonitorWUConsume,
					 MonitorInfoStreamConsume,
					 MonitorPopUpSkinConsume,
					 MonitorPopUpUnskinConsume,
					 MonitorGalaxyConsume,
					 MonitorWSZHiSouConsume,
					 MonitorWSCubicConsume,
					 MonitorConsumeBase):


	@classmethod
	def consume(cls, data):

		'''============================ MonitorWSConsume ==============================='''
		threading.Thread(target=MonitorWSConsume.ws_channel, args=(data,)).start()
		threading.Thread(target=MonitorWSConsume.ws_server, args=(data,)).start()
		threading.Thread(target=MonitorWSConsume.ws_industry, args=(data,)).start()
		threading.Thread(target=MonitorWSConsume.ws_account, args=(data,)).start()
		threading.Thread(target=MonitorWSConsume.ws_adpos, args=(data,)).start()
		#
		'''============================ MonitorWSSogouHaoConsume ==============================='''
		threading.Thread(target=MonitorWSSogouHaoConsume.sogouhao_channel_back, args=(data,)).start()
		threading.Thread(target=MonitorWSSogouHaoConsume.sogouhao_channel_search, args=(data,)).start()
		threading.Thread(target=MonitorWSHuaZhangConsume.huazhang_channel_huazhang, args=(data,)).start()
		threading.Thread(target=MonitorWSZHiSouConsume.ws_zhisou, args=(data,)).start()
		#
		#
		'''============================ MonitorZhiDaConsume ==============================='''
		threading.Thread(target=MonitorZhiDaConsume.zhida_channel, args=(data,)).start()
		#
		'''============================ MonitorCubicConsume ==============================='''
		threading.Thread(target=MonitorWSCubicConsume.cubic_channel_cubic, args=(data,)).start()
		#
		'''============================ MonitorCustomerConsume ==============================='''
		threading.Thread(target=MonitorCustomerConsume.customer_channel_vivo, args=(data,)).start()
		threading.Thread(target=MonitorCustomerConsume.customer_channel_oppo, args=(data,)).start()
		threading.Thread(target=MonitorCustomerConsume.customer_channel_mi, args=(data,)).start()
		threading.Thread(target=MonitorCustomerConsume.customer_channel_taobao, args=(data,)).start()
		threading.Thread(target=MonitorCustomerConsume.customer_channel_taobaolowquality, args=(data,)).start()
		#
		#				
		'''============================ MonitorBaiChuanConsume ==============================='''
		threading.Thread(target=MonitorWSBaiChuanConsume.baichuan_channel_recomm_below, args=(data,)).start()
		threading.Thread(target=MonitorWSBaiChuanConsume.baichuan_channel_secondary_page, args=(data,)).start()
		#threading.Thread(target=MonitorWSBaiChuanConsume.ws_bc_server, args=(data,)).start()
		#
		#
		#
		'''============================ MonitorInputConsume ==============================='''
		threading.Thread(target=MonitorInputConsume.input_channel_tongtou, args=(data,)).start()
		threading.Thread(target=MonitorInputConsume.input_channel_inputstream, args=(data,)).start()
		threading.Thread(target=MonitorInputConsume.input_channel_direct, args=(data,)).start()
		threading.Thread(target=MonitorInputConsume.input_channel_recomm, args=(data,)).start()
		threading.Thread(target=MonitorInputConsume.input_channel_guang, args=(data,)).start()
		#
		#
		#
		'''============================ MonitorPSConsume ==============================='''
		threading.Thread(target=MonitorPSConsume.ps_channel_bc, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_bd, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_brws, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_ime, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_123, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_sogou, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_sohu, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_channel_soso, args=(data,)).start()
		#
		threading.Thread(target=MonitorPSConsume.ps_server_bj, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_server_bj_sk, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_server_gd, args=(data,)).start()
		threading.Thread(target=MonitorPSConsume.ps_server_js, args=(data,)).start()
		#		
		#
		'''============================ MonitorPUConsume ==============================='''
		threading.Thread(target=MonitorPUConsume.pu_channel_content, args=(data,)).start()
		threading.Thread(target=MonitorPUConsume.pu_channel_searchkey, args=(data,)).start()
		#
		#
		'''============================ MonitorWUConsume ==============================='''
		threading.Thread(target=MonitorWUConsume.wu_channel_content, args=(data,)).start()
		threading.Thread(target=MonitorWUConsume.wu_channel_searchkey, args=(data,)).start()
		threading.Thread(target=MonitorWUConsume.wu_channel_zhitou, args=(data,)).start()
		#
		#
		'''============================ MonitorInfoStreamConsume ==============================='''
		threading.Thread(target=MonitorInfoStreamConsume.infostream_channel_content, args=(data,)).start()
		threading.Thread(target=MonitorInfoStreamConsume.infostream_channel_searchkey, args=(data,)).start()
		threading.Thread(target=MonitorInfoStreamConsume.infostream_channel_zhitou, args=(data,)).start()
		#
		#
		'''============================ MonitorPopUpSkinConsume ==============================='''
		threading.Thread(target=MonitorPopUpSkinConsume.popupskin_channel_content, args=(data,)).start()
		threading.Thread(target=MonitorPopUpSkinConsume.popupskin_channel_zhitou, args=(data,)).start()
		#
		#
		'''============================ MonitorPopUpUnskinConsume ==============================='''
		threading.Thread(target=MonitorPopUpUnskinConsume.popupunskin_channel_content, args=(data,)).start()
		threading.Thread(target=MonitorPopUpUnskinConsume.popupunskin_channel_zhitou, args=(data,)).start()
		#
		#
		'''============================ MonitorGalaxyConsume ==============================='''
		threading.Thread(target=MonitorGalaxyConsume.wgalaxy_channel_ec, args=(data,)).start()
		threading.Thread(target=MonitorGalaxyConsume.wgalaxy_channel_finance, args=(data,)).start()
		threading.Thread(target=MonitorGalaxyConsume.wgalaxy_channel_other, args=(data,)).start()
		threading.Thread(target=MonitorGalaxyConsume.moon_channel_ec, args=(data,)).start()






	@staticmethod
	def run(interval, port, offset_sec):
		MonitorConsumeBase.start_server(interval, port, offset_sec, MonitorConsume.consume)

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

	if len(sys.argv) > 1:
		try:
			interval = int(sys.argv[1])
			port = int(sys.argv[2])

			if interval < 10:
				logging.error("interval is err[10s, 60s, 300s, ...].")
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

	offset_sec = 8
	sec = int(time.time())
	sec_diff = sec % interval
	if sec_diff >= offset_sec:
	    delay = interval - sec_diff + offset_sec
	else:
	    delay = offset_sec - sec_diff

	time.sleep(delay)

	pid=os.fork()
	pidfile="{}_{}_{}.pid".format(sys.argv[0].split('.')[0], sys.argv[1], sys.argv[2])
	if pid != 0:
		#logging.info("father pid: {}".format(pid))
		with open(pidfile, 'w') as f:
			f.write("{}".format(pid))
		os._exit(0)
	else:
		#logging.info("daemon pid: {}".format(realpid))
		MonitorConsume.run(interval, port, offset_sec)