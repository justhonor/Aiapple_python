#!/usr/bin/python
# coding:utf-8
##
# Filename: crawler_ex02-1.py
# Author  : aiapple
# Date    : 2017-05-11
# Describe:
##
#############################################

# 隐藏表达 input type=hidden 也需要post
# name=csrfmiddlewaretoken ,值与cookies中csrftoken对应
from bs4 import BeautifulSoup
import requests
import pdb

# login 
url_login = "http://www.heibanke.com/accounts/login/"
url_form = "http://www.heibanke.com/lesson/crawler_ex02/"

parm={'username':'test','password':'test123'}

session = requests.Session()
f = session.get(url_login)

parm_cookies={'csrfmiddlewaretoken':f.cookies.get('csrftoken')}
parm.update(parm_cookies)
print parm

r=session.post(url_login,data=parm)
print 'login status:',r.status_code


# logical process
s = session.get(url_form)
parm1={'csrfmiddlewaretoken':s.cookies.get('csrftoken')}
for number in range(30):
	#pdb.set_trace()
	d = {'username':'test','password':str(number)}
	parm1.update(d)
	rr=session.post(url_form,data=parm1)
	if rr.text.find(u"密码错误") >0:
		print number,"not correct"
		number = number+1
	else:
		print number,"is correct"
		print BeautifulSoup(rr.text,"html.parser").h3.string
		break	
