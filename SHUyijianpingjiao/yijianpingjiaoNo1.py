# -*- coding: UTF-8 -*- 
import urllib2
import urllib
import os,sys
import time
import cookielib
from BeautifulSoup import BeautifulSoup
import re
reload(sys)
sys.setdefaultencoding("utf-8")

class pinggu():
	def __init__(self):
		self.hosturl = 'http://cj.shu.edu.cn/'
		self.posturl = 'http://cj.shu.edu.cn/'
	def yijianpinggu(self):
		self.cookies(self.hosturl)
		self.getidentifyingcode()
		self.input_and_set_logindata(self.posturl)
	#设置cookies
	def cookies(self,hosturl):
		cj = cookielib.LWPCookieJar()  
		cookie_support = urllib2.HTTPCookieProcessor(cj)  
		opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
		urllib2.install_opener(opener)
		#访问一次网页获得cookie
		h = urllib2.urlopen(hosturl)
	#获取验证码图片
	def getidentifyingcode(self):
		p_url='http://cj.shu.edu.cn/User/GetValidateCode?%20%20+%20GetTimestamp()'
		pic = urllib2.urlopen(p_url)
		content = pic.read()
		f = open('jiaowuguanli2.jpg','wb')
		f.write(content)
		f.close()
	#输入学号姓名验证码,并制作value,header
	def input_and_set_logindata(self,posturl):
		txtUserNo = raw_input("input your StudentNumber: ")
		txtPassword = raw_input("input your PassWord: ")
		txtValiCode = raw_input("input Identifying Code: ")
		values = {'url':'',
		  'txtUserNo':txtUserNo, #输入学号
		  'txtPassword':txtPassword, #输入密码
		  'txtValidateCode':txtValiCode}
		data = urllib.urlencode(values)

		headers = { "Host":"cj.shu.edu.cn",
			"Origin":"http://cj.shu.edu.cn",
			"Referer":"http://cj.shu.edu.cn/",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
			}
		self.login_and_get(data,headers,self.posturl)


	def login_and_get(self,data,headers,posturl):
		req = urllib2.Request(posturl,data,headers)
		response = urllib2.urlopen(req)
		#获取教学评估
		htmlget=urllib2.urlopen('http://cj.shu.edu.cn/StudentPortal/Evaluate')
		classnumber=[]
		soup = BeautifulSoup(htmlget.read())
		self.set_coursedata(soup,classnumber)

	def set_coursedata(self,soup,classnumber):
		for tag in soup.findAll(id=re.compile('TEnrollIDORG$')):
			classnumber.append(tag['value'])

		post_url='http://cj.shu.edu.cn/StudentPortal/EvaluateSave'
		headers2 = { "Host":"cj.shu.edu.cn",
					"Origin":"http://cj.shu.edu.cn",
					"Referer":"http://cj.shu.edu.cn/StudentPortal/Evaluate",
					"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
					}
		values2 ={}
		print "You have %d courses in this term" % len(classnumber)
		for i in range(0,len(classnumber)):
   			values2['classlist[%d].TEnrollIDORG' % i]= classnumber[i]
			values2['classlist[%d].TEnrollIDORG' % i]= classnumber[i]
			values2['classlist[%d].ItemValue[0]' % i]='20'
			values2['classlist[%d].ItemValue[1]' % i]='25'
			values2['classlist[%d].ItemValue[2]' % i]='25'
			values2['classlist[%d].ItemValue[3]' % i]='25'

		data2 = urllib.urlencode(values2)
		self.get_result(headers2,data2,post_url)

	def get_result(self,headers2,data2,post_url):
		req2 = urllib2.Request(post_url,data2,headers2)
		response2 = urllib2.urlopen(req2)
		html2 = response2.read()
		print html2

if __name__ == '__main__':
	a = pinggu()
	a.yijianpinggu()