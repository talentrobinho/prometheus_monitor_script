#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-16 16:16:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from rediscluster import StrictRedisCluster
import random
from clickhouse_driver import Client
import logging
import sys


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)




class Base(object):

    clickhouse_host     = '10.134.49.49'
    #clickhouse_cluster  = ['10.134.76.125', '10.134.113.118', '10.134.92.25', '10.139.36.103']
    clickhouse_cluster  = ['10.139.18.31', '10.139.36.107', '10.139.36.122', '10.139.36.67']
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
    def __conn_clickhouse_cluster(cls):
        err = 0
        ip = random.choice(cls.clickhouse_cluster)
        #for ip in cls.clickhouse_cluster:
        logging.info('clickhouse_cluster: {}'.format(ip))
        try:
            client = Client(ip,
                            user=cls.clickhouse_user,
                            password=cls.clickhouse_passwd,
                            database=cls.clickhouse_db)
            #return client
        except Exception as err:
            err += 1
        
        #if err == len(cls.clickhouse_cluster):
        if err == 1:
            logging.error("Filter Error connecting to database of clickhouse cluster.")
            sys.exit(1)
        
        return client


    @classmethod
    def query_clickhouse(cls, sql, flag='alone'):
        if flag == 'alone':
            cli = cls.__conn_clickhouse()
        elif flag == 'cluster':
            cli = cls.__conn_clickhouse_cluster()
        try:
            data_list = cli.execute(sql)
        except Exception as err:
            logging.error("query error[%s]:%s"%(sql,err))
            sys.exit(1)
        #logging.info('Base {}'.format(len(data_list)))
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
        
        nodes_index = random.randint(0,len(redis_node_list)-1)
        #logging.info("********* connecting redis_node_list %d ************"%(nodes_index,))
        try:
            return StrictRedisCluster(startup_nodes=[redis_node_list[nodes_index]], max_connections=500)
        except Exception,e:
            logging.error("Filter Error connecting to database of redis cluster.")
            sys.exit(1)

