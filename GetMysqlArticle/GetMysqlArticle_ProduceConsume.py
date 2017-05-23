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
from Queue import Queue
from threading import Thread as thread
import threading

import logging 
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s [line:%(lineno)d] %(thread)d %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

#Define a StreamHandler object to print INFO level or higher log to screen
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(thread)d %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


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

def Producer(q,fd,lock):
	pattern_h=re.compile(r'http://.*?>')
	pattern_n=re.compile(r'[0-9]+. M.*?SQL.*?<')	
	pattern_r=re.compile(r'.*?/')
	
	L=lock
	#print threading.currentThread().getName(),"Producer starting"
	logging.debug("%s Producer starting"%threading.currentThread().getName())
	CurrentThreadName = "Producer "+ "%s"%threading.currentThread().getName()
	while True:
		if L.acquire():	
			# print CurrentThreadName,"Got lock!!!!"
			logging.debug("%s Got lock!!!!"%CurrentThreadName)
			temp={}
			if fd.closed:
				L.release()
				break
			line=fd.readline()
			# judge whether the file is end
			if not line : 
				#print "fd at the end of file. return"
				logging.debug("%s fd at the end of file. return"%CurrentThreadName)
				fd.close()
				L.release()
				break
			else:
				# find herf and name stored using dict
				href=pattern_h.findall(line)
				name=pattern_n.findall(line)

				url=''.join(href)[:-1]
				filename=''.join(name)[:-1]
			#	pdb.set_trace()
			#	print CurrentThreadName,url
				if pattern_r.findall(filename) != []:
					# replace \ to space
					filename=filename.replace('/',' ')

				# put the dict into queue
				#pdb.set_trace()
				temp[url]=filename
				logging.debug("url:%s name:%s"%(url,filename))
				logging.debug("line:%s "%(line))
				q.put(temp)
			L.release()
		else:
			#print CurrentThreadName,"Can not got lock!!!"
			logging.debug("%s Can not got lock!!!"%CurrentThreadName)
		#time.sleep(0.1)

	#print threading.currentThread().getName(),"Producer Ending"
	logging.debug("%s Producer ending"%threading.currentThread().getName())
		
def Consumer(q,fd,lock):
	# Download html to local with real name
	logging.debug("%s Consumer Starting"%threading.currentThread().getName())
	#print threading.currentThread().getName(),"Consumer Starting"
	location='/home/aiapple/git/Aiapple_python/GetMysqlArticle'

	CurrentThreadName = "Consumer "+"%s"%threading.currentThread().getName()	
	L=lock
	while True:
	#	if L.acquire(2):
			# The file is closed and queue is empty.return
			#pdb.set_trace()
	#		print CurrentThreadName,"Got lock!!!"
			if fd.closed and q.empty():
				logging.debug("%s The file is closed and queue is empty.return"%CurrentThreadName)
				#print CurrentThreadName," The file is closed and queue is empty.return"
				#L.release()
				break
			else:
				# Download 
				# print CurrentThreadName,"geting value from queue"
				if not q.empty():
					#pdb.set_trace()
					logging.debug("%s Consumer Download()"%CurrentThreadName)
					#print CurrentThreadName," Consumer Download()"
					Download(q.get(),location) 
			#L.release()
	#	else:
	#		print CurrentThreadName,"Can not got lock!!!"
			time.sleep(0.1)
		
	#print threading.currentThread().getName(),"Consumer Ending"
	logging.debug("%s Consumer Ending"%threading.currentThread().getName())

def Download(data,location):
	CurrentThreadName = "Consumer "+"%s"%threading.currentThread().getName()	
	temp=data
	url = ''.join(temp.keys())

	name = ''.join(temp[url])
	if len(name) > 100:
        	name=name[0:100]+"........."
	local = os.path.join(location,name)
	
	times=0
	error = 1
	while error and times < 5:
		try:
			#print CurrentThreadName,"Downloading :%s"%url
			#print "                              %s "%name
			logging.debug("%s Downloading :%s"%(CurrentThreadName,url))
			logging.debug("%s %s "%(CurrentThreadName,name))
			urllib.urlretrieve(url,local)
		except socket.timeout:
			times=times+1
			#print 'timeout: \n',url
			logging.debug('timeout: ',url)

		except Exception,e:
			times=times+1
			logging.error('%s error:%s url:%s name:%s local:%s data:%s'%(CurrentThreadName,e,url,name,local,data))
		else:
			logging.debug("%s Download correct!"%CurrentThreadName)
			error = 0
		#print "Downloading error:%s"%error	
		logging.debug("%s Downloading error:%s\n"%(CurrentThreadName,error))

if __name__=='__main__':
	
	start_time=time.time()
	global numbers
	numbers=0
	main_url = 'http://mysql.taobao.org/monthly/'

#	article=open('articles.html','wr+')
#	start_time = time.time()
#	fd,bs,html = get_bs_obj(main_url)
#	Get_DatabaseReport(bs,fd,html)
#	Get_DatabaseStudy(bs,fd,html)
#	article.close()
#	DownloadTOLoal()

	Threads_numbers=2
	# using Queue control the lock
	q = Queue(maxsize=200)

	# create two mutex for temp data
	P=threading.Lock()
	C=threading.Lock()

	# reopen the file 
	fd = open('articles.html','r+')

	# create thread object

	producers  = [thread(target=Producer,args=(q,fd,P)) for i in xrange(Threads_numbers)]
	for p in producers:
		#print "starting producer thread %s"%p.getName()
		logging.debug("starting producer thread %s"%p.getName())
		p.start()

	consumers  = [thread(target=Consumer,args=(q,fd,C)) for i in xrange(Threads_numbers+2)]
	for c in consumers:
		#print "starting consumer thread %s"%c.getName()
		logging.debug("starting consumer thread %s"%c.getName())
		c.start()

	for c in consumers:
		if c.isAlive():
			logging.debug(" consumer join() thread %s"%c.getName())
			#print "consumer join()"
			c.join()

	for p in producers:
		if p.isAlive():
			#print "procuder join()"
			logging.debug(" producer join() thread %s"%p.getName())
			p.join()

	#print
	#print "The program costs %ss"%(time.time()-start_time)
	logging.debug("The program costs %ss"%(time.time()-start_time))
	

