# !/usr/bin/python
# -*- coding: utf-8 -*-
# import urllib
# import urllib2
# from bs4 import BeautifulSoup
# import re
import argparse
import datetime

import requests
from prettytable import PrettyTable
from requests.packages.urllib3.exceptions import \
	InsecureRequestWarning  # 感谢：—>—>->http://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

now = datetime.datetime.now()
tomorrow = now + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')
print tomorrow

argument = argparse.ArgumentParser()
argument.add_argument('--fromcity', '-f', default='xuzhou')
argument.add_argument('--tocity', '-t', default='huaibei')
argument.add_argument('--date', '-d', default=tomorrow)
# argument.add_argument('-d',action='store_true')
args = argument.parse_args()

from_station = args.fromcity
to_station = args.tocity
Date = args.date
# /​otn/​resources/​js/​framework/​favorite_name.js
stationlist_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js/?station_version=1.8979'
r = requests.get(stationlist_url, verify=False)

stationlist = r.content

ToStation = ''
FromStation = ''

placea = stationlist.find(from_station)
placeb = stationlist.find(to_station)

for i in range(-4, -1):
	FromStation += stationlist[placea + i]
for i in range(-4, -1):
	ToStation += stationlist[placeb + i]
# https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-11-22&from_station=TJP&to_station=GZQ
query_url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=' + Date + '&from_station=' + FromStation + '&to_station=' + ToStation
r = requests.get(query_url, verify=False)

with open('json.txt', 'w') as fp:
	fp.write(str(r.json()))

if 'datas' in r.json()["data"]:
	rj = r.json()["data"]["datas"]
	pt = PrettyTable()

	header = '车次 车站 到站时间 时长 一等座 二等座 软卧 硬卧 硬座 无座'.split()
	pt._set_field_names(header)

	for x in rj:
		ptrow = []
		ptrow.append(x["station_train_code"])
		ptrow.append('\n'.join([x["from_station_name"], x["to_station_name"]]))
		ptrow.append('\n'.join([x["start_time"], x["arrive_time"]]))
		ptrow.append(x["lishi"].replace(':', 'h') + 'm')
		ptrow.append(x['zy_num'])
		ptrow.append(x['ze_num'])
		ptrow.append(x['rw_num'])
		ptrow.append(x['yw_num'])
		ptrow.append(x['yz_num'])
		ptrow.append(x['wz_num'])
		pt.add_row(ptrow)
	print pt
else:
	print '这两个站点没有直达列车'
