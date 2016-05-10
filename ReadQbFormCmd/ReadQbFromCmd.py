#!/usr/bin/python
#coding:utf-8
#autor:jack
#date :2014-4-22
#file :ReadQbFromCmd.py
import urllib2
import re
import time
import os
import sys
import termios


def InputKeyIs(msg):
    # 获取标准输入的描述符
    fd = sys.stdin.fileno()

    # 获取标准输入(终端)的设置
    old_ttyinfo = termios.tcgetattr(fd)

    # 配置终端
    new_ttyinfo = old_ttyinfo[:]

    # 使用非规范模式(索引3是c_lflag 也就是本地模式)
    new_ttyinfo[3] &= ~termios.ICANON
    # 关闭回显(输入不会被显示)
    new_ttyinfo[3] &= ~termios.ECHO

    # 输出信息
    sys.stdout.write(msg)
    sys.stdout.flush()
    # 使设置生效
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
    # 从终端读取
    a = os.read(fd, 7)
    # 还原终端设置
    termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)

    return a

def DisplayForm(st):
	head = "--------------------这是第%s条----------------------"%COUNTT
        tail = "--------------------请按J继续-----------------------"
        
        #增加两个开始的空格
	st ="    " + st

        num = (len(head)/2-2)*3
        for n in range(num,len(st),num):
                if n >= num and n+num <= len(st):
                        print "*     "+st[n-num:n]
                elif n+num > len(st):
                        print "*     "+st[n:len(st)]

        



class qiubai:
        def __init__(self,page=1):
                self.page=page

        def search(self,page):
		global COUNTT
                start = time.time()
                my_headers = {
                           'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                           "Accept": "text/plain"
                          }
		url  = "http://www.qiushibaike.com/8hr/page/%s" %page
                req = urllib2.Request(url,headers=my_headers)   #以my_headers这种浏览器形式去申请一个对象
                #print "method:",req.get_method()                #使用get还是post呢？
                resp  = urllib2.urlopen(req)                    #open这个申请对象
                html  = resp.read()                             #得到html
                #print "html len",len(html)                                 
                #print "html type",type(html)                                 
		#open('thefile.txt','w+').write(html)
                readDone = time.time()-start
                #print "after read time%f"%(readDone)

		#建立re_qb这种规则
                #re_qb = re.compile(r'class="content".*?<!--\d',re.DOTALL)#2016-4-25不能用了，官方改变了html
                re_qb = re.compile(r'class="content".*?</',re.DOTALL)
		
                #用re_qb这种规则去匹配html得到新得my_qiubai
		my_qiubai = re_qb.findall(html)
		print "this is my_qiubai len:",len(my_qiubai)
		#首先显示的条数控制
		count = 0 
		#按键显示控制
		jcrol = 1
		for line in my_qiubai:
			#每一页先显示一条，之后再要求按键继续
			
			#除去正则多余元素       \
          		lextra = "class=\"content\">"
          		rextra = "</"
          		line = line.lstrip(lextra)
          		line = line.rstrip(rextra)

			if count < 1:
				print '---------------------这是第%s条---------------------'%COUNTT
				#print line
				DisplayForm(line)
				#print "this is line type:",type(line)
			if (count >=1) and (count < len(my_qiubai)-1):
				while jcrol:
					if InputKeyIs("---------------------请按j继续---------------------\n")=='j':
						jcrol = 0
						print '\t\t\t\t\t\t\t\t\n\n\n\n'
						print '---------------------这是第%s条---------------------'%COUNTT
						#print line
						DisplayForm(line)
					
			COUNTT += 1
			count += 1	
			jcrol = 1
			
                reDone = time.time()-readDone
                #print "after show time %f"%(time.time()-reDone)
                s = raw_input("回车继续")
                if s == "q":
                        exit()
                else:
                        page=int(page)+1
                        print "-"*18 + "第" + str(page) + "页" + "-"*18
                        self.search(page)
                        print "-"*40

        def query(self):
                global p
                p = raw_input("输入要看的页数:")
                if p == "q":
                        exit()
                elif not p.isdigit() or p =="0":
                        self.query()
                else:
                        print "-"*18 + "第" + p + "页" + "-"*18
                        self.search(p)
if __name__ == "__main__":
        print "-"*40
        print "糗百命令行版"
        print '输入"q"退出程序'
        print "-"*40
        COUNTT = 1
        qb=qiubai()
        qb.query()

