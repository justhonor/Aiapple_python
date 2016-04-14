#!/usr/bin/python
#-*-coding:utf-8-*-
#coding:utf-8
import re
f = open("re.file","r")
html = f.readlines()
print len(html)
html = str(html)
#re_qb = re.compile(r'class="content">',re.DOTALL)
#re_qb = re.compile(r'<!--\d',re.DOTALL)
re_qb = re.compile(r'class="content">[\u4e00-\u9fa5]*<!--\d',re.DOTALL)
my_qiubai = re_qb.findall(html)
print len(my_qiubai)
#print my_qiubai
