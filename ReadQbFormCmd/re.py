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
head = "-------------------这是第3条-----------------------"
#head = "------这是第%s条-----"
tail = "--------------------请按J继续-----------------------"
#test = "‘“？，。！：周：岁；" 
test = "记得小时候一周岁生日要“抓周”，过年那会儿，正好有一亲戚生孩子，我爸说突然说起我小时候当时一手抓了支铅笔一手抓了支毛笔，大家都说我肯定是个读书的料，可把我爹妈乐坏了。直到很多年后，我才明白，那是二笔的意思。" 

test = "      " + test
print "this is test len",len(test)
num = (len(head)/2-7)*3
print "this is num",num
print head
for n in range(num,len(test),num):
	#print "this is n",n
	if n >= num and n+num <= len(test):
		print "*     "+test[n-num:n]
	elif n+60 > len(test):
		print "*     "+test[n:len(test)]
print tail 
#20个字符为一行
'''
for n in range(60,len(test),60):
	#print "this is n",n
	if n >= 60 and n+60 <= len(test):
		print "*     "+test[n-60:n]
	elif n+60 > len(test):
		print "*     "+test[n:len(test)]
'''		






'''
print "this is test[:21]",test[:21]
print "this is test[:22]",test[:22]
print "this is test[:23]",test[:23]
print test[21:24]
print test[27:30]
'''
'''


d ="。"
print "this is . len",len(d)
a ="，"
print "this is , len",len(a)
c ="？"
print "this is ? len",len(c)
b ="’" 
print "this is ' len",len(b)
e ="”" 
print "this is \" len",len(e)
f ="/" 
print "this is / len",len(f)
g ="；" 
print "this is ; len",len(g)
h ="：" 
print "this is : len",len(h)
m ="！" 
print "this is ! len",len(m)
'''
'''
#除去所有标点符号
biaodian = " \’\“，。：；"
print "6 test len is",len(test)
te = test.strip(biaodian)
print te
#utf-8 每一个汉字占三个字节
'''
'''
tt = "’”/？。》；：！"
print tt
print "this is tt len",len(tt)

print "this is tt[:1]",tt[:1]
print "this is tt[:2]",tt[:2]
print "this is tt[:3]",tt[:3]
print "this is tt[:4]",tt[:4]
print "this is tt[:5]",tt[:5]
print "this is tt[:6]",tt[:6]
print "this is tt[:7]",tt[:7]
print "this is tt[:8]",tt[:8]
print "this is tt[:9]",tt[:9]
print "this is tt[:10]",tt[:10]
print "this is tt[:11]",tt[:11]
print "this is tt[:12]",tt[:12]
print "this is tt[:13]",tt[:13]
print "this is tt[:14]",tt[:14]
print "this is tt[:15]",tt[:15]
'''
'''
print "this is test[:4]",test[:4]
print "this is test[:3]",test[:3]
print "this is test[:2]",test[:2]
print "this is test[:1]",test[:1]
print "this is test[:5]",test[:5]
print "this is test[:6]",test[:6]
print "this is test[:7]",test[:7]
print "this is test[:8]",test[:8]
'''
'''
for line in my_qiubai:
        head = "-------------------这是第3条-----------------------"
        #head = "------这是第%s条-----"
        tail = "--------------------请按J继续-----------------------"
  
        #除去正则多余元素       \
	lextra = "class=\"content\">"
	rextra = "<!--1"
        line = line.lstrip(lextra)
	line = line.rstrip(rextra)
	#print line
	line = "      " + line
	#print "this is line len ",len(line)
	#20个字符为一行
	num = (len(head)/2-2)*3
	print  "this is len num ",num
	print  "this is len line ",len(line)
	
	print head
	n = num
	for n in range(num,len(line),num):
		print "this is n ",n
	        if n >= num and n+num <= len(line):
			print "this is nnn ",n
        	        print "*     "+line[n-num:n]
       		elif n+num > len(line):
                	print "*     "+line[n:len(line)]

	print tail 
	#总字数
	word_num = len(line)/3
	#没行应该显示的字数
	line_num = len(head)/2
	#第一行标识数
	line_index1 = line_num*3+1
	#第二行标识数
	line_index2 = line_num*2*3+1
	#打印第一行第二行
	#print "this is first line:",line[:line_index1]
	#print "this is second line:",line[line_index1:line_index2]
	print "this is line_index1",line_index1
	print "this is line_index2",line_index2
	
	print line[:line_index1]
	print '\t'
	print line[line_index1:line_index2]
	
        #计算除头尾的行数,显示的首尾行也算
        #Line = (len(line)/3*2)/len(tail) + 2    
        #print "行数是 ",Line
'''
  
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

