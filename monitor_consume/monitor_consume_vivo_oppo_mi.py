#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_consume_conf import *
import logging


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)



class MonitorCustomerConsume(object):



        self.redis_node_list = ParseConf.redis['nodes']
        self.conn = None
        self.consumer = None

    def conn_redis(self):
        nodes_index = randint(0,len(self.redis_node_list)-1)
        self.logger.info("********* connecting redis_node_list %d ************"%(nodes_index,))
        try:
            #return StrictRedisCluster(startup_nodes=self.redis_node_list, socket_keepalive=True)
            return StrictRedisCluster(startup_nodes=[self.redis_node_list[nodes_index]], max_connections=500)
            #return StrictRedisCluster(startup_nodes=self.redis_node_list, max_connections=500)
        except Exception,e:
            self.logger.error("Filter Error connecting to database of redis cluster.")
            sys.exit(1)

	@classmethod
	def bigcustomer_channel_vivo(cls, data):
		'''搜狗号回流消耗'''
		sogouhao_back_consume = 0
		try:
			for line in data:
				item = line[7].split(',')
				if len(item) >= 5:
					if item[5] == "108":
						sogouhao_back_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			sogouhao_back_consume = 0
		sogouhao_channel_consume.labels('sogouhao_channel_back', '0.0.0.0').set(sogouhao_back_consume/100.0)


