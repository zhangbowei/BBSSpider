# -*- coding:utf-8 -*-
import time 
import urllib
import urllib2
import cookielib
import re
import webbrowser
import random
 
class SDU:
    #用户名禁止重复！
    def initUserInfor(self):
        self.userinfor =  {
            '?????': '?????',
            '?????': '?????'
        }
    
    def initReplyTextCore(self):
        self.replylist = [
            u'不错，支持一下',
            u'已阅，顶一下',
            u'看看，顶你',
            u'多谢分享',
            u'说的不错，支持',
            u'提着水桶到处转，哪里缺水哪里灌！ ',
            u'太6了!'
        ]

    def initProxylist(self):
        self.proxylist = (
            '211.167.112.14:80',
            '210.32.34.115:8080',
            '115.47.8.39:80',
            '211.151.181.41:80',
            '219.239.26.23:80',
        )

    def __init__(self):
        self.loginUrl = 'http://bbs.xjtu.edu.cn/BMY/bbslogin'
        self.upsideUrlHeader = 'http://bbs.xjtu.edu.cn/'
        self.upsideUrlTail = raw_input('请输入 帖子 尾部链接:')
        self.upsideUrl = ''
        self.maxUserNum = 15
        self.initUserInfor()
        self.initProxylist()
        self.initReplyTextCore()

        self.loginHeaders =  {
            'Connection' : 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host':'bbs.xjtu.edu.cn',
            'Referer' : 'http://bbs.xjtu.edu.cn/',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
        }
        self.upsideHeaders = {}

    def chooseIP(self):
        self.proxyURL = random.choice(self.proxylist)    
        print u"正在使用的代理IP为：",self.proxyURL
        self.cookie = cookielib.CookieJar()
        self.proxy = urllib2.ProxyHandler({'':self.proxyURL})
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)

        #普通方式访问（使用本机IP）
        #self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        #代理服务器访问
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)
        

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
        self.chooseIP()
        request  = urllib2.Request(self.loginUrl,self.postData,self.loginHeaders)
        response = self.opener.open(request)
        page = response.read().decode('gb2312')
        print page
        pattern = re.compile('<meta http-equiv=\'Refresh\' content=\'0; url=/(.*?)\'>',re.S)
        result = re.search(pattern,page)
        if not result:
            print u"该用户名或密码错误：",self.username,"  ",self.password
            return False
        else:
            print u"正在使用该用户名与密码：",self.username,"  ",self.password
        secretKey = result.group(1)
        self.secretKey = secretKey        
        print u"链接加密串：",secretKey
        self.upsideUrl = self.upsideUrlHeader +self.secretKey+ self.upsideUrlTail
        return True
    
    def getReplyItems(self):
        request  = urllib2.Request(self.upsideUrl,self.postData,self.loginHeaders)
        response = self.opener.open(request)
        if not response:
            print u"用户链接输入错误!"
            self.upsideUrl = ''
            return
        page = response.read().decode('gb2312')
        pattern = re.compile('<TR><TD class=bor.*?method=post action=(.*?)>',re.S)
        replyUrlTail = re.search(pattern,page).group(1)
        replyUrlHeader = self.upsideUrlHeader
        self.replyUrl = replyUrlHeader + self.secretKey + replyUrlTail

        pattern = re.compile('<td><input name=title.*?value=\'(.*?)\'',re.S)
        self.replyTitle = re.search(pattern,page).group(1)
        pattern = re.compile('<td><textarea id=textedit.*?class=f2 >(.*?)</textarea>',re.S)
        replyTextTail = re.search(pattern,page).group(1)
        self.replyTextCore = random.choice(self.replylist)
        self.replyText = self.replyTextCore + replyTextTail
    
    def convertCode(self):
        self.replyTitle = self.replyTitle.encode('gb2312')
        self.replyText = self.replyText.encode('gb2312')
        submit = u'发表'
        self.submit = submit.encode('gb2312')
    
    def replyPage(self):
        self.upsideHeaders =  {
            'Connection' : 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host':'bbs.xjtu.edu.cn',
            'Referer' : self.upsideUrl,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
        }
        #转码
        self.convertCode()
                    
        self.content = {
            'title':self.replyTitle,
            'signature':'0',
            'text':self.replyText,
            'Submit2':self.submit
        } 

        self.contentData = urllib.urlencode(self.content)
        request  = urllib2.Request(self.replyUrl,self.contentData,self.upsideHeaders)
        response = self.opener.open(request)
        page = response.read().decode('gb2312')
        print u"回复：",self.replyTextCore,u" \n成功"

    def workItOut(self):
        if self.getPageUrl():
            self.getReplyItems()
            self.replyPage()
    
    def chooseUser(self):
        username = random.choice(self.userinfor.keys())   
        password = self.userinfor[username]
        print username,password
        self.login(username,password)
        del self.userinfor[username]
        
    def start(self):
        for num in range(0,self.maxUserNum):
            if not self.userinfor:
                break           
            self.chooseUser()
            self.workItOut()
            if not self.upsideUrl:
                break
            time.sleep(5)
        print u"程序执行完成"            

sdu = SDU()
sdu.start()
