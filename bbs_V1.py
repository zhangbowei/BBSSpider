# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re

class SDU:

    def __init__(self):
        self.loginUrl = 'http://bbs.xjtu.edu.cn/BMY/bbslogin'
        self.upsideUrlHeader = 'http://bbs.xjtu.edu.cn/'
        self.upsideUrlTail = raw_input('请输入 帖子 尾部链接:')
        self.upsideUrl = ''
        self.secretKey = ''
        self.proxyURL = ''
        self.cookie = cookielib.CookieJar()
        self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        #普通方式访问
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        #代理服务器访问
        #self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)

        self.loginHeaders =  {
            'Connection' : 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host':'bbs.xjtu.edu.cn',
            'Referer' : 'http://bbs.xjtu.edu.cn/',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
        }

    def login(self, username, password):
        self.username = username
        self.password = password
        self.post = {
            'id':self.username,
            'pw':self.password,
            'login_btn.x':'2',
            'login_btn.y':'1'
        }
        self.postData = urllib.urlencode(self.post)


    def getPageUrl(self):
        request  = urllib2.Request(self.loginUrl,self.postData,self.loginHeaders)
        response = self.opener.open(request)
        page = response.read().decode('gbk')
        pattern = re.compile('<meta http-equiv=\'Refresh\' content=\'0; url=/(.*?)\'>',re.S)
        secretKey = re.search(pattern,page)
        self.secretKey = secretKey.group(1)
        print u"链接加密串：",secretKey.group(1)
        self.upsideUrl = self.upsideUrlHeader +self.secretKey+ self.upsideUrlTail
        print self.upsideUrl


    def upsidePage(self):
        request  = urllib2.Request(
            url = self.upsideUrl,
            data = self.postData,
            headers = self.loginHeaders)
        response = self.opener.open(request)
        page = response.read().decode('gbk')
        print page

sdu = SDU()
sdu.login('?????','?????')
sdu.getPageUrl()
sdu.upsidePage()
# time.sleep(20)
