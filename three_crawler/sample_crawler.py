#!/usr/bin/python
# coding:utf-8
##
# Filename: sample_crawler.py
# Author  : aiapple
# Date    : 2017-05-10
# Describe:
##
#############################################

import urllib
from bs4 import BeautifulSoup
import re
import pdb

number=''
url='http://www.heibanke.com/lesson/crawler_ex00/'
URL=url+number
i=0

html = urllib.urlopen(URL)
bs_obj = BeautifulSoup(html,"html.parser")
str1 = bs_obj.h3.string

pattern = re.compile(r"\d")
while True:
	number=pattern.findall(str1)
	if number == [] or i > 100:
		break
	URL=url+''.join(number)
	#pdb.set_trace()
	i=i+1
	print URL,number,i
	html = urllib.urlopen(URL)
	bs_obj = BeautifulSoup(html,"html.parser")
	str1 = bs_obj.h3.string

print str1,
