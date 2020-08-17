#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from prometheus_client import Gauge


ws_business_qps 	= Gauge('ws_business_qps', 'ws_business_qps', ['channel','ip'])
ws_business_rpm 	= Gauge('ws_business_rpm', 'ws_business_rpm', ['channel','ip'])
ws_business_ctr 	= Gauge('ws_business_ctr', 'ws_business_ctr', ['channel','ip'])


ws_server_qps 	= Gauge('ws_server_qps', 'ws_server_qps', ['channel','ip'])
ws_server_rpm 	= Gauge('ws_server_rpm', 'ws_server_rpm', ['channel','ip'])
ws_server_ctr 	= Gauge('ws_server_ctr', 'ws_server_ctr', ['channel','ip'])