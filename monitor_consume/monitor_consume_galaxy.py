#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-18 16:03:08
# @Author  : lizhansheng (lizhansheng@sogou-inc.com)

from monitor_consume_conf import *
import logging


logging.basicConfig(
    format="[%(asctime)s] [file:%(filename)s] [line:%(lineno)s] [col:%(levelno)s], [%(message)s]"
)
logging.getLogger().setLevel(logging.INFO)
'''
		SQL_SELECT = "SELECT price, \
   			                 pid, \
   			                 city_code, \
   			                 ip, \
   			                 max_price, \
   			                 planid, \
   			                 kid_indus, \
   			                 eesf, \
   			                 business_level1, \
   			                 business_level2, \
   			                 business_level3, \
   			                 pc_business, \
   			                 union_business, \
   			                 upos_asid, \
   			                 accountid \
   			                 FROM realtime.consume"
'''
galaxy_ec = {
			"18882348":"jd",
			"18583511":"jd",
			"18872991":"jd",
			"18882202":"jd",
			"18741204":"jd",
			"20519945":"sn",
			"18901045":"sn",
			"20286338":"sn",
			"20286344":"sn",
			"20005085":"amazon",
			"20010897":"kaola",
			"20011219":"dangdang",
			"20010009":"vip",
			"20208035":"guomei",
			"18863843":"taobao",
			"20703760":"1688",
}
moon_ec = {
			"18883593":"111",
			"18733965":"jumei",
			"18729825":"mogujie",
			"18723394":"vipshop",
			"18618155":"vipshop",
			"18678216":"vipshop",
			"18716920":"vipshop",
			"18655549":"jd",
			"19982714":"jd",
			"19982713":"jd",
			"19987652":"jd",
			"18619570":"jd",
			"18619570":"jd",
			"18711766":"jd",
			"18618367":"suning",
			"19983291":"suning",
			"20286338":"suning",
			"18618443":"gome",
			"18618416":"lefeng",
			"18618412":"yhd",
			"18618839":"yhd",
			"18717232":"yhd",
			"18618539":"beibei",
			"18618832":"yougou",
			"18873277":"dangdang",
			"18873276":"dangdang",
			"19982805":"dangdang",
			"19982806":"dangdang",
			"19982804":"dangdang",
			"20002846":"dangdang",
			"20002872":"dangdang",
			"18618969":"dangdang",
			"18648133":"dangdang",
			"18648142":"dangdang",
			"18659465":"1zw",
			"18664847":"xiupin",
			"18665700":"feiniu",
			"18678661":"yohobuy",
			"18677919":"paipai",
			"18701352":"womai",
			"18706243":"yapingguo",
			"18926422":"windeln",
			"18933193":"kaola",
			"20005219":"amazon",
			"20703760":"1688",
}
class MonitorGalaxyConsume(object):


	@classmethod
	def wgalaxy_channel_ec(cls, data):
		'''
			30304
		   	sogou-apps-3501672ebc68a552
		'''
		wgalaxy_ec_consume = {}
		pid = 'sogou-apps-3501672ebc68a552'

		for line in data:
			if str(line[1]) == pid and str(line[10]).startswith('SogouOther'):
				try:
					if line[14] in galaxy_ec.keys():
						if galaxy_ec[line[14]] in wgalaxy_ec_consume.keys():
							wgalaxy_ec_consume[galaxy_ec[line[14]]] += int(line[0])
						else:
							wgalaxy_ec_consume[galaxy_ec[line[14]]] = int(line[0])
				except IndexError as err:
					logging.error("This is accountid is not galaxy_ec")
					wgalaxy_ec_consume[galaxy_ec[line[14]]] += 0
				#galaxy_ec_consume += int(line[0])

		for ec in wgalaxy_ec_consume.keys():
			galaxy_channel_consume.labels('wgalaxy_channel_ec_%s'%(ec,), '0.0.0.0').set(wgalaxy_ec_consume[ec]/100.0)



	@classmethod
	def wgalaxy_channel_finance(cls, data):
		'''
		   	30304
		   	sogou-apps-a35f4223bb8f6c86
		'''
		wgalaxy_finance_consume = 0
		pid = 'sogou-apps-a35f4223bb8f6c86'
		try:
			for line in data:
				if str(line[1]) == pid and str(line[10]).startswith('SogouOther'):
					wgalaxy_finance_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			wgalaxy_finance_consume = 0
		galaxy_channel_consume.labels('wgalaxy_channel_finance', '0.0.0.0').set(wgalaxy_finance_consume/100.0)
	



	@classmethod
	def wgalaxy_channel_other(cls, data):
		'''
		   	30304
		    sogou-waps-c0cccc24dd23ded6
            sogou-apps-9eb53b5052d534ea
            sogou-waps-3000311ca56a1cb9
            sogou-apps-3261769be720b0fe
            sogou-apps-47e51e9d11cf800f
		'''
		wgalaxy_other_consume = 0
		pid = {'sogou-waps-c0cccc24dd23ded6',
			   'sogou-apps-9eb53b5052d534ea',
			   'sogou-waps-3000311ca56a1cb9',
			   'sogou-apps-3261769be720b0fe',
			   'sogou-apps-47e51e9d11cf800f'}
		try:
			for line in data:
				if str(line[1]) in pid and str(line[10]).startswith('SogouOther'):
					wgalaxy_other_consume += int(line[0])
		except IndexError as err:
			logging.error(err)
			wgalaxy_other_consume = 0
		galaxy_channel_consume.labels('wgalaxy_channel_other', '0.0.0.0').set(wgalaxy_other_consume/100.0)



	@classmethod
	def moon_channel_ec(cls, data):
		'''
		20760:MoonPCShoppingSearch
		50760:MoonShoppingSearch
			self.loglist[7]).startswith('50760') or str(self.loglist[7]).startswith('20760')
		'''
		pmoon_ec_consume = {}
		wmoon_ec_consume = {}
		moon_ec_consume = 0
		for line in data:
			if str(line[10]).startswith('MoonPCShoppingSearch'):
				try:
					if line[14] in moon_ec.keys():
						if moon_ec[line[14]] in pmoon_ec_consume.keys():
							pmoon_ec_consume[moon_ec[line[14]]] += int(line[0])
						else:
							pmoon_ec_consume[moon_ec[line[14]]] = int(line[0])
				except IndexError as err:
					logging.error("This is accountid is not moon_ec")
					pmoon_ec_consume[moon_ec[line[14]]] += 0
				moon_ec_consume += int(line[0])
			elif str(line[10]).startswith('MoonShoppingSearch'):
				try:
					if line[14] in moon_ec.keys():
						if moon_ec[line[14]] in wmoon_ec_consume.keys():
							wmoon_ec_consume[moon_ec[line[14]]] += int(line[0])
						else:
							wmoon_ec_consume[moon_ec[line[14]]] = int(line[0])
				except IndexError as err:
					logging.error("This is accountid is not moon_ec")
					wmoon_ec_consume[moon_ec[line[14]]] += 0
				moon_ec_consume += int(line[0])

		for ec in pmoon_ec_consume.keys():	
			moon_channel_consume.labels('pmoon_channel_ec_%s'%(ec,), '0.0.0.0').set(pmoon_ec_consume[ec]/100.0)

		for ec in wmoon_ec_consume.keys():	
			moon_channel_consume.labels('wmoon_channel_ec_%s'%(ec,), '0.0.0.0').set(wmoon_ec_consume[ec]/100.0)





