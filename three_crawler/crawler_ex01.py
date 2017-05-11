#!/usr/bin/python
# coding:utf-8
##
# Filename: crawler_ex01.py
# Author  : aiapple
# Date    : 2017-05-10
# Describe:
##
#############################################
import requests
from bs4 import BeautifulSoup
url='http://www.heibanke.com/lesson/crawler_ex01/'
number=22


while True:
	parm={'username':'zane','password':number}
	r = requests.post(url,data=parm)

	if r.text.find(u'密码错误') > 0 and number < 50 :
		number=number+1
		print "输入密码:",number,"错误"
	else:
		html=r.text
		#print html
		bs=BeautifulSoup(html,"html.parser")
		print bs.h3.string
		print "正确密码:",number
		break

#f=urllib2.urlopen(req)

