#!/usr/bin/python
# coding:utf-8
##
# Filename: GetMysqlArticle.py
# Author  : aiapple
# Date    : 2017-05-12
# Describe:
##
#############################################
from bs4 import BeautifulSoup
import urllib 
import requests
import re
import pdb
import time
import os

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

main_url = 'http://mysql.taobao.org/monthly/'

def get_bs_obj(url):
	fd = urllib.urlopen(url)
	error = fd.getcode()
	if error != 200:
		print "error:%s",error
	html = fd.read()
	bs = BeautifulSoup(html,"html.parser")
	return	fd,bs,html

#def yunsite(url):
#    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#               'Accept-Encoding': 'gzip, deflate, sdch, br',
#               'Accept-Language': 'zh-CN,zh;q=0.8',
#               'Connection': 'keep-alive',
#               'Host': 'http://mysql.taobao.org/monthly/',
#               'Upgrade-Insecure-Requests': '1',
#               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
#
#    html = requests.get(url, headers=headers, allow_redirects=False)
#    return html.headers['Location']

fd,bs,htmll = get_bs_obj(main_url)

article=open('article.html','wr')


for a in bs.find_all(name='a',attrs={'href':re.compile(r'monthly/[0-9]')}):
	# find second_url 	
	pattern = re.compile(r'[0-9].*?[0-9]$')
	s_url = pattern.findall(a.attrs.get('href'))
	second_url = main_url + ''.join(s_url)
	print second_url

	#print yunsite(second_url)
	cf,cs,html = get_bs_obj(second_url)
	print "cf status:",cf.getcode()
	#print html

	title=cs.title.string
	print "title si:",title	
	# 数据库内核月报
	pattern1=re.compile(r'数据库内核月报')
	if pattern1.findall(title) != [] and 1 == 2:
		# find  all article url
		for aa in cs.find_all(name='a',attrs={'href':re.compile(r'monthly/[0-9]')}):
			pdb.set_trace()
			# find MySQL article url
			pattern2=re.compile(r'MySQL')
			if pattern2.findall(aa.string):
				patter = re.compile(r'[0-9].*?/')
				ss_url = patter.findall(aa.attrs.get('href'))
				arti_url = main_url + ''.join(ss_url)
			
				print aa.string,arti_url
				write_string='<h2><a href=%s>%s</a></h2>\n'%(arti_url,aa.string.strip().replace("·","--"))
				print write_string
				article.write(write_string)
	# 淘宝数据库研发组	
	pattern3=re.compile(r'淘宝数据库研发组')
	if pattern3.findall(title) !=[]:
		pdb.set_trace()
		# structure the name which consist of ariticles' name
		print cs.table

article.close()
