#!/usr/bin/python
#-*-coding:utf-8-*-
#coding:utf-8
import re
f = open("re.file","r")
html = f.read()
#html = f.readlines()
print  "html len:",len(html)
print  "html type", type(html)
re_qb = re.compile(r'class="content">.*?<!--\d',re.DOTALL)
#re_qb = re.compile(r'class="content".*?<!--\d',re.DOTALL)
my_qiubai = re_qb.findall(html)
print "my_qiubai type",type(my_qiubai)
print "my_qiubai len",len(my_qiubai)


for line in my_qiubai:
        head = "--------------------这是第%s条----------------------"
        tail = "--------------------请按J继续-----------------------"
  
        #除去正则多余元素       \
	lextra = "class=\"content\">"
	rextra = "<!--1"
        line = line.lstrip(lextra)
	line = line.rstrip(rextra)
	print line
	line = "    " + line
        #计算除头尾的行数
        Line = len(line)/len(tail) + 2    
          

#print my_qiubai[0]

#my = my.qiubai[0].pop('<')
#print my
#r = re.compile(r'>.*?<',re.DOTALL)
#my = r.findall(str(my_qiubai))
#print "my type",type(my_qiubai)
#print "my len",len(my_qiubai)
#print my[0]
#print my_qiubai
#for line in my_qiubai:
        #line = line.rstrip()
#	print type(line)
#	print len(line)
#	print line
	
#print my_qiubai
#<class="content">
#
#记得小时候一周岁生日要“抓周”，过年那会儿，正好有一亲戚生孩子，我爸说突然说起我小时候当时一手抓了支铅笔一手抓了支毛笔，大家都说我以后肯定是个>读书的料，可把我爹妈乐坏了。直到很多年后，我才明白，那是二笔的意思。
#<!--1456393445-->

