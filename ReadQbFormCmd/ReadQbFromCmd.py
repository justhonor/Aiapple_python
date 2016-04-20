#!/usr/bin/python
#coding:utf-8
#autor:jack
#date :2014-4-22
#file :ReadQbFromCmd.py
import urllib2
import re
import time
class qiubai:
        def __init__(self,page=1):
                self.page=page

        def search(self,page):
#               re_qb = re.compile(r'detail.*?<a.*?>(.*?)<.*?title="(.*?)">\s*(.*?)\s*?<',re.DOTALL)
                start = time.time()
                my_headers = {
                           'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                           "Accept": "text/plain"
                          }
		url  = "http://www.qiushibaike.com/8hr/page/%s" %page
                req = urllib2.Request(url,headers=my_headers)   #以my_headers这种浏览器形式去申请一个对象
                print "method:",req.get_method()                #使用get还是post呢？
                resp  = urllib2.urlopen(req)                    #open这个申请对象
                html  = resp.read()                             #得到html
                print "html len",len(html)                                 
                print "html type",type(html)                                 
		#print "eee type of html ",type(html)
                readDone = time.time()-start
                #html = str(html)                                #将html转换成string类型
               #f = open("html.txt","w+")                       #建立html.txt并将html写入
               #f.writelines(html)
		#f.close()
                #print "type of html  ",type(html)
                print "after read time%f"%(readDone)

		#建立re_qb这种规则
#               re_qb = re.compile(r'class="content".*?="(.*?)">.*?(\S.*?)\s*?<',re.DOTALL)
                re_qb = re.compile(r'class="content".*?<!--\d',re.DOTALL)

                #用re_qb这种规则去匹配html得到新得my_qiubai
		my_qiubai = re_qb.findall(html)
		for line in my_qiubai:
			print line
                reDone = time.time()-readDone
                #print "after re time %f"%(reDone)
                #lenth = len(my_qiubai)
                #ff = open("my_qiubai.txt","w+")                       #建立html.txt并将html写入
                #ff.writelines(my_qiubai)
	        #ff.close()
		#print "my_qiubai is ",my_qiubai
                #for i in range(0,lenth):
                #        for k in range(2):
                #                print my_qiubai[i][k]
                print "after show time %f"%(time.time()-reDone)
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
        qb=qiubai()
        qb.query()

