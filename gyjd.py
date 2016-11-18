# -*- coding:utf-8 -*-
import time 
import urllib
import urllib2
import cookielib
import re
import webbrowser
import random

class SDU:

    def initProxylist(self):
        self.proxylist = (
            '211.167.112.14:80',
            '210.32.34.115:8080',
            '115.47.8.39:80',
            '211.151.181.41:80',
            '219.239.26.23:80',
        )

    def __init__(self):
        self.loginUrl = 'http://jiaoda.zhushou.la/Vote_do.asp'
        self.maxUserNum = 11
        self.id = 0
        self.initProxylist()
        self.initIP()

        self.loginHeaders =  {
            'Connection' : 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host':'jiaoda.zhushou.la',
            'Referer' : 'http://jiaoda.zhushou.la/vote.asp',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
        }

    def initIP(self):
        self.proxyURL = random.choice(self.proxylist)    
        print u"正在使用的代理IP为：",self.proxyURL
        # self.cookie = cookielib.CookieJar()
        self.cookie = cookielib.CookieJar()
        self.proxy = urllib2.ProxyHandler({'':self.proxyURL})
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)

        #普通方式访问（使用本机IP）
        #self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        #代理服务器访问
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)
        

    def initLoginData(self):
        self.post = {
            'ValidCode': '1',
            'pro1': '',
            'pid1': self.id,
            'Submitok2': ''
        } 
        self.postData = urllib.urlencode(self.post)
        
    def getPageUrl(self):
        request  = urllib2.Request(self.loginUrl,self.postData,self.loginHeaders)
        response = self.opener.open(request)
        page = response.read().decode('gb2312')
        pattern = re.compile('bgcolor="#FFFFFF" style="line-height:30px;"><p>(.*?)</p>',re.S)
        result = re.search(pattern,page)
        if not result:
            print u"失败"
            return False
        status = result.group(1)
        print u"服务器反馈：",status
        return True

    def workItOut(self):
        self.getPageUrl()
    
    def start(self):
        for num in range(0,self.maxUserNum):
            self.initIP()
            self.initLoginData()
            self.workItOut()
            time.sleep(random.randint(1,2))
        print u"任务完成！"            

sdu = SDU()
sdu.id = raw_input('请输入ID:')
sdu.start()
