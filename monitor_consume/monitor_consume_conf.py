#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import Gauge

'''promethuse config'''
ws_channel_consume 		 = Gauge('ws_channel_consume', 'ws_channel_consume', ['channel','ip'])
ws_account_consume 		 = Gauge('ws_account_consume', 'ws_account_consume', ['account','ip'])
ws_industry_consume 	 = Gauge('ws_industry_consume', 'ws_industry_consume', ['industry','ip'])
ws_server_consume 		 = Gauge('ws_server_consume', 'ws_server_consume', ['region','ip'])
ws_bc_server_consume  	 = Gauge('ws_bc_server_consume', 'ws_bc_server_consume', ['region','ip'])
ws_adpos_consume 		 = Gauge('ws_adpos_consume', 'ws_adpos_consume', ['adpos','ip'])

sogouhao_channel_consume = Gauge('sogouhao_channel_consume', 'sogouhao_channel_consume', ['channel','ip'])
zhida_channel_consume 	 = Gauge('zhida_channel_consume', 'zhida_channel_consume', ['channel','ip'])
input_channel_consume 	 = Gauge('input_channel_consume', 'input_channel_consume', ['channel','ip'])
bigcustomer_channel_consume = Gauge('bigcustomer_channel_consume', 'bigcustomer_channel_consume', ['channel', 'industry', 'ip'])
huazhang_channel_consume = Gauge('huazhang_channel_consume', 'huazhang_channel_consume', ['channel','ip'])
baichuan_channel_consume = Gauge('baichuan_channel_consume', 'baichuan_channel_consume', ['channel','ip'])
zhisou_channel_consume = Gauge('zhisou_channel_consume', 'zhisou_channel_consume', ['channel','ip'])
cubic_channel_consume = Gauge('cubic_channel_consume', 'cubic_channel_consume', ['channel','ip'])

ps_channel_consume 		 = Gauge('ps_channel_consume', 'ps_channel_consume', ['channel','ip'])
ps_server_consume 		 = Gauge('ps_server_consume', 'ps_server_consume', ['region','ip'])


pu_channel_consume 		 = Gauge('pu_channel_consume', 'pu_channel_consume', ['channel','ip'])
pu_server_consume 		 = Gauge('pu_server_consume', 'pu_server_consume', ['region','ip'])


wu_channel_consume 		 = Gauge('wu_channel_consume', 'wu_channel_consume', ['channel','ip'])
wu_server_consume		 = Gauge('wu_server_consume', 'wu_server_consume', ['region','ip'])

skin_channel_consume	 = Gauge('skin_channel_consume', 'skin_channel_consume', ['channel','ip'])
unskin_channel_consume	 = Gauge('unskin_channel_consume', 'unskin_channel_consume', ['channel','ip'])
info_channel_consume	 = Gauge('info_channel_consume', 'info_channel_consume', ['channel','ip'])



galaxy_channel_consume 	 = Gauge('galaxy_channel_consume', 'galaxy_channel_consume', ['channel','ip'])
moon_channel_consume 	 = Gauge('moon_channel_consume', 'moon_channel_consume', ['channel','ip'])



'''machine list'''
ws_server_bj_sk 		= ['10.139.36.101',
			   			   '10.160.18.95',
			   			   '10.162.34.92']
ws_server_bj 			= ['10.139.20.71',
			    		   '10.139.35.58',
			    		   '10.162.34.82',
			    		   '10.160.13.71',
			    		   '10.160.13.73',
			    		   '10.160.13.76',
			    		   '10.160.73.104',
			    		   '10.160.81.121',
			    		   '10.162.34.82']
ws_server_gd 			= ['10.135.66.41',
						   '10.135.66.32',
						   '10.135.73.90',
						   '10.135.73.41']
ws_server_js 			= ['10.140.26.81',
						   '10.140.26.80',
						   '10.140.11.23']
ws_server_bc_bj			= ['10.134.52.64',
						   '10.160.44.49',
						   '10.160.54.69',
						   '10.139.17.94',
						   '10.160.17.94',
						   '10.160.17.95',
						   '10.160.51.114',
						   '10.160.68.101']
ws_server_lk_bj			= ['10.134.65.77',
						   '10.134.65.78',
						   '10.160.74.126',
						   '10.160.69.52',
						   '10.160.61.100',
						   '10.160.19.77']
