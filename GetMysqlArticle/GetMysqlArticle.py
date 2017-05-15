#!/usr/bin/python
# encoding:utf-8
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
import os

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import socket
socket.setdefaulttimeout(30)

def get_bs_obj(url):
	open_correct=0
	# process timeout using sleep(2)
	while open_correct==0:
		try:
			fd = urllib.urlopen(url)
			error = fd.getcode()
			open_correct=1
		except socket.timeout:
			print 'timeout: \n',url
			time.sleep(2)
			print "open_correct:%s"%open_correct
		except Exception,e:
			print "%s error:%s"%(url,e)
			print "wait 2 seconds"
			time.sleep(2)
			
	if error != 200:
		print "error:%s",error
	else:
		print 'url: %s open correct'%url
	html = fd.read()
	bs = BeautifulSoup(html,"html.parser")
	#html=''
	#bs = BeautifulSoup(fd,"html.parser")
	return	fd,bs,html

def Schedule(a,b,c):
	# a:已经下载的数据块
	# b:数据块的大小
	# c:远程文件的大小
	per = 100.0*a*b/c
	if per > 100 :
		per = 100
	#print '%.2f%%' % per

def Download(url,location,filename):
	local = os.path.join(location,filename)
	#urllib.urlretrieve(url,local,Schedule)
	error = 1
	try:
		print "%s "%filename
		print url
		print "Downloading..."
		urllib.urlretrieve(url,local)
	except socket.timeout:
		print 'timeout: \n',url
	except Exception,e:
		print 'error:%s \n'%e
	else:
		print "Download correct!\n"
		error = 0
	print "Downloading error:%s"%error	
	return error
	

# 数据库内核月报
def Get_DatabaseReport(bs,fd,html):
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
    			global numbers
    			numbers=numbers+1
    			write_string='<h2><a href=%s>%s. %s</a></h2>\n'%(arti_url,numbers,aa.string.strip().replace("·","--"))
    			#print write_string
    			article.write(write_string)
	print 

def Get_DatabaseStudy(bs,fd,html):
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
	global numbers 
    	numbers=numbers+1
    	print name
    	print 	
    	write_string='<h2><a href=%s>%s. %s</a></h2>\n'%(t_url,numbers,name)
    	#print write_string
    	article.write(write_string)
   

def DownloadTOLoal():
	# Download the html to local
	location='/home/aiapple/git/Aiapple_python/GetMysqlArticle'
	try:
        	f = open('articles.html','r+')
       		html =  f.read()
       		#print html
	finally:
        	f.close()


	rest_a={}
	bs=BeautifulSoup(html,"html.parser")
	
	pattern=re.compile(r'.*?/')	
	for a in bs.find_all(name='a'):
		#pdb.set_trace()
		href =  a.attrs.get('href')
		name = a.string

		if pattern.findall(name) != []:
			# replace \ to space
			name=name.replace('/',' ')
			#print name

		if len(name) > 100:
			name=name[0:100]+"........."
			
		#print "%s "%name
		#print href
		if Download(href,location,name):
			#pdb.set_trace()
			rest_a[href]=name

	# Handle timeout 
	a_rest={}
	while len(rest_a):
		print  "Do the rest of html that report  timeout  before\n"
		print  "the rest number:%s\n %s"%(len(rest_a),rest_a)
		for href,name in rest_a.items():
		    if Download(href,location,name):
		        a_rest[href]=name
		    time.sleep(0.1)
		rest_a.clear()
		rest_a=a_rest.copy()
		a_rest.clear()


if __name__=='__main__':
	
	start_time=time.time()
	global numbers
	numbers=0
	main_url = 'http://mysql.taobao.org/monthly/'

	article=open('articles.html','wr+')
	start_time = time.time()
	fd,bs,html = get_bs_obj(main_url)

	Get_DatabaseReport(bs,fd,html)
	Get_DatabaseStudy(bs,fd,html)
	article.close()

	DownloadTOLoal()
	print
	print "The program costs %ss"%(time.time()-start_time)
	

