#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import Gauge

ws_server_qps 	= Gauge('ws_server_qps', 'ws_server_qps', ['region', 'province', 'ip'])
ws_server_qps1 	= Gauge('ws_server_qps1', 'ws_server_qps1', ['region', 'province', 'ip', 'flag'])
ws_server_rpm 	= Gauge('ws_server_rpm', 'ws_server_rpm', ['region', 'province', 'ip', 'flag'])
ws_server_cov   = Gauge('ws_server_cov', 'ws_server_cov', ['region', 'province', 'ip', 'flag'])
ws_server_ctr 	= Gauge('ws_server_ctr', 'ws_server_ctr', ['region', 'province', 'ip', 'flag'])
ws_server_time  = Gauge('ws_server_time', 'ws_server_time', ['region', 'province', 'ip', 'flag'])
ws_server_asn   = Gauge('ws_server_asn', 'ws_server_asn', ['region', 'province', 'ip', 'flag'])


ws_channel_qps 		= Gauge('ws_channel_qps', 'ws_channel_qps', ['channel1', 'channel2', 'flag', 'industry'])
ws_channel_rpm 		= Gauge('ws_channel_rpm', 'ws_channel_rpm', ['channel1', 'channel2', 'flag', 'industry'])
ws_channel_cov 		= Gauge('ws_channel_cov', 'ws_channel_cov', ['channel1', 'channel2', 'flag', 'industry'])
ws_channel_ctr 		= Gauge('ws_channel_ctr', 'ws_channel_ctr', ['channel1', 'channel2', 'flag', 'industry'])
ws_channel_asn 		= Gauge('ws_channel_asn', 'ws_channel_asn', ['channel1', 'channel2', 'flag', 'industry'])
ws_channel_time 	= Gauge('ws_channel_time', 'ws_channel_time', ['channel1', 'channel2', 'flag', 'industry'])




sk_server_list = {'10.139.36.101',
			   	  '10.160.18.95',
			   	  '10.162.34.92'}

bj_server_list = {'10.139.20.71',
				  '10.139.35.58',
				  '10.139.20.52',
				  '10.160.13.71',
			      '10.160.13.73',
			      '10.160.13.76',
			      '10.160.73.104',
			      '10.160.81.121',
			      '10.162.34.82'}

gd_server_list = {'10.135.66.41',
				  '10.135.66.32',
				  '10.135.73.90',
				  '10.135.73.41'}

js_server_list = {'10.140.26.81',
				  '10.140.26.80',
				  '10.140.11.23'}

pweb_server_list = {'10.160.13.72',
				  	'10.160.13.74',
				  	'10.160.13.75'}

region_list = {'10.160':'hebei',
			   '10.162':'hebei',
			   '10.134':'beijing',
			   '10.144':'beijing',
			   '10.139':'beijing',
			   '10.149':'beijing',
			   '10.140':'jiangsu',
			   '10.150':'jiangsu',
			   '10.135':'guangdong',
			   '10.145':'guangdong'
			   }