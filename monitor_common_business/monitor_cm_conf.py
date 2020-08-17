#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import Gauge

update_server_qps 	= Gauge('update_server_qps', 'update_server_qps', ['service', 'region', 'ip', 'message', 'msg_type', 'message_status', 'cluster'])
cm_server_qps 	= Gauge('cm_server_qps', 'cm_server_qps', ['service', 'region', 'ip', 'business', 'is_pass', 'level', 'error_type'])




update_server_list = {'10.139.48.123'}
#bill_server_list = {'10.134.115.91',
#					'10.134.115.90',
#					'10.139.40.60',
#					'10.139.40.59'}
#cheating_server_list = {'10.139.35.57'}


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