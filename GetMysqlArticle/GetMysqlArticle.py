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
import re
import pdb
import time

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

main_url = 'http://mysql.taobao.org/monthly/'
start_time = time.time()
def get_bs_obj(url):
	fd = urllib.urlopen(url)
	error = fd.getcode()
	if error != 200:
		print "error:%s",error
	else:
		print 
		print 'url: %s open correct'%url
	html = fd.read()
	bs = BeautifulSoup(html,"html.parser")
	#html=''
	#bs = BeautifulSoup(fd,"html.parser")
	
	return	fd,bs,html

fd,bs,html = get_bs_obj(main_url)
article=open('articles.html','wr')

numbers=0
# 数据库内核月报
for a in bs.find_all(name='a',attrs={'href':re.compile(r'monthly/[0-9]')}):
	# find second_url 	
	pattern = re.compile(r'[0-9].*?[0-9]$')
	s_url = pattern.findall(a.attrs.get('href'))
	second_url = main_url + ''.join(s_url)
	#print second_url

	#print yunsite(second_url)
	cf,cs,html = get_bs_obj(second_url)
	#print "cf status:",cf.getcode()
	#print html

	title=cs.title.string
	#print "title si:",title	

	# find  all article url
	for aa in cs.find_all(name='a',attrs={'href':re.compile(r'monthly/[0-9]')}):
		# find MySQL article url
		pattern2=re.compile(r'MySQL')
		if pattern2.findall(aa.string):
			patter = re.compile(r'[0-9].*?/')
			ss_url = patter.findall(aa.attrs.get('href'))
			arti_url = main_url + ''.join(ss_url)
		
			print aa.string.strip()
			numbers=numbers+1
			write_string='<h2><a href=%s>%s. %s</a></h2>\n'%(arti_url,numbers,aa.string.strip().replace("·","--"))
			#print write_string
			article.write(write_string)
# 淘宝数据库研发组	
for t_a in bs.find_all(name='a',attrs={'href':re.compile(r'^.*?php')}):
	t_url = t_a.attrs.get('href')
	#print t_url

	t_fd,t_bs,t_html = get_bs_obj(t_url)
	#print "t_fd status:",t_fd.getcode()

	name=''
	# structure the name which consist of ariticles' name
	for names in t_bs.find_all(name='span',attrs={'class':'toctext'}):
		#pdb.set_trace()
		name=name+names.string+"--"
		#print name.strip()
	name=name[:-2]
	numbers=numbers+1
	print name
	write_string='<h2><a href=%s>%s. %s</a></h2>\n'%(t_url,numbers,name)
	#print write_string
	article.write(write_string)

article.close()
#print start_time,time.time()
print
print "The program costs %ss"%(time.time()-start_time)
