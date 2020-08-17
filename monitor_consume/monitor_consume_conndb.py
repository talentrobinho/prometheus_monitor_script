#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 18:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from rediscluster import StrictRedisCluster
from random import randint
from multiprocessing import Process
from clickhouse_driver import Client
import threading
import logging
import os
import time
import sys
import copy
#import schedule

logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)




class Base(object):

    clickhouse_host     = '10.134.49.49'
    clickhouse_user     = 'storm'
    clickhouse_passwd   = ''
    clickhouse_db       = 'realtime'
    interval            = 10


    @classmethod
    def __conn_clickhouse(cls):
        try:
            client = Client(cls.clickhouse_host,
                            user=cls.clickhouse_user,
                            password=cls.clickhouse_passwd,
                            database=cls.clickhouse_db)
            #return client
        except Exception as err:
            logging.error("Filter Error connecting to database of clickhouse.")
            sys.exit(1)

        return client

    @classmethod
    def query_clickhouse(cls, sql):
        cli = cls.__conn_clickhouse()
        try:
            data_list = cli.execute(sql)
        except Exception as err:
            logging.error("query error[%s]:%s"%(sql,err))
            sys.exit(1)

        return data_list



    @classmethod
    def merge_data(cls, data_list):
        total_v = 0
        try:
            for v in data_list:
                total_v += int(v[0])
        except Exception as err:
            logging.error("merge data error:%s"%(err,))
            sys.exit(1)

        return total_v


    @classmethod
    def entrance(cls, sql):
        data_set = cls.query_clickhouse(sql)
        result = cls.merge_data(data_set)
        return result



class ConnRedis(object):

    @classmethod
    def conn_redis(cls):
        redis_node_list = [{'host': '10.162.129.38', 'port': '7001'},
                           {'host': '10.162.129.38', 'port': '7002'},
                           {'host': '10.162.133.41', 'port': '7001'},
                           {'host': '10.162.133.41', 'port': '7002'},
                           {'host': '10.162.133.42', 'port': '7001'},
                           {'host': '10.162.133.42', 'port': '7002'}]
        
        nodes_index = randint(0,len(redis_node_list)-1)
        #logging.info("********* connecting redis_node_list %d ************"%(nodes_index,))
        try:
            return StrictRedisCluster(startup_nodes=[redis_node_list[nodes_index]], max_connections=500)
        except Exception,e:
            logging.error("Filter Error connecting to database of redis cluster.")
            sys.exit(1)

