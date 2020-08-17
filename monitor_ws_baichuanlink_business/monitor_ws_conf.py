#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import Gauge

ws_bc_server_qps 	= Gauge('ws_bc_server_qps', 'ws_bc_server_qps', ['region', 'province', 'ip', 'flag'])
ws_bc_server_cov   = Gauge('ws_bc_server_cov', 'ws_bc_server_cov', ['region', 'province', 'ip', 'flag'])
ws_bc_server_asn   = Gauge('ws_bc_server_asn', 'ws_bc_server_asn', ['region', 'province', 'ip', 'flag'])


ws_lk_server_qps 	= Gauge('ws_lk_server_qps', 'ws_lk_server_qps', ['region', 'province', 'ip', 'flag'])
ws_lk_server_cov   = Gauge('ws_lk_server_cov', 'ws_lk_server_cov', ['region', 'province', 'ip', 'flag'])
ws_lk_server_asn   = Gauge('ws_lk_server_asn', 'ws_lk_server_asn', ['region', 'province', 'ip', 'flag'])

'''
ws_server_bc_bj			= ['10.134.52.64',
						   '10.134.79.98',
						   '10.134.80.116',
						   '10.139.17.94']

ws_server_bc_hb			= ['10.160.44.49',
						   '10.160.54.69']

ws_server_lk_bj			= ['10.134.65.77',
						   '10.134.65.78',
						   '10.139.50.51',
						   '10.139.50.52']

'''
ws_server_bc = {'10.160.68.101':'ws_server_bc_hb',
				'10.160.51.114':'ws_server_bc_hb',
				'10.160.17.95':'ws_server_bc_hb',
				'10.160.17.94':'ws_server_bc_hb'
				}

ws_server_lk = {'10.134.65.77':'ws_server_lk_bj',
				'10.134.65.78':'ws_server_lk_bj',
				'10.160.74.126':'ws_server_lk_hb',
				'10.160.69.52':'ws_server_lk_hb',
				'10.160.61.100':'ws_server_lk_hb',
				'10.160.19.77':'ws_server_lk_hb'
				}
region_list = {'10.160':'hebei',
			   '10.134':'beijing',
			   '10.144':'beijing',
			   '10.139':'beijing',
			   '10.149':'beijing',
			   '10.140':'jiangsu',
			   '10.150':'jiangsu',
			   '10.135':'guangdong',
			   '10.145':'guangdong'
			   }
