# -*- coding:utf-8 -*-
import time 
import urllib
import urllib2
import cookielib
import re
import webbrowser
import random

class Tool:
    removeExtraUrl = re.compile('&amp') 
    removeSemicolon = re.compile(';')
    def replace(self,x):
        x = re.sub(self.removeExtraUrl,"",x)
        x = re.sub(self.removeSemicolon,"&",x)
        return x.strip()

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
            u'已阅，顶下',
            u'看看，顶你',
            u'多谢分享',
            u'说的不错，支持',
            u'我是来灌水的，哈 ',
            u'666!'
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
        self.tool = Tool()
        self.loginUrl = 'http://bbs.xjtu.edu.cn/BMY/bbslogin'
        self.upsideUrlHeader = 'http://bbs.xjtu.edu.cn/'
        self.upsideUrlTail = '' 
        self.upsideUrl = ''
        self.maxUserNum = 15
        self.initUserInfor()
        self.initProxylist()
        self.initReplyTextCore()
        self.initIP()

        self.loginHeaders =  {
            'Connection' : 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host':'bbs.xjtu.edu.cn',
            'Referer' : 'http://bbs.xjtu.edu.cn/',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
        }
        self.upsideHeaders = {}

    def initIP(self):
        self.proxyURL = random.choice(self.proxylist)    
        print u"正在使用的代理IP为：",self.proxyURL
        self.cookie = cookielib.CookieJar()
        self.proxy = urllib2.ProxyHandler({'':self.proxyURL})
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)

        #普通方式访问（使用本机IP）
        #self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        #代理服务器访问
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)
        

    def initLoginData(self, username, password):
        self.username = username
        self.password = password
        self.post = {
            'id':self.username,
            'pw':self.password,
            'login_btn.x':'2',
            'login_btn.y':'1'
        } 
        self.postData = urllib.urlencode(self.post)
        
    def getUpsideUrlTail(self):
        sourceUrl = raw_input('请输入原帖地址：')
        request = urllib2.Request(sourceUrl)
        response = urllib2.urlopen(request)
        page = response.read()
        pattern = re.compile('class=btnfunc.*?</tr></table></td>.*?<a href=\'(.*?)\'',re.S)
        result = re.search(pattern,page)
        if not result:
            print u"系统无法获得回复链接"        
            return False
        self.upsideUrlTail = self.tool.replace(result.group(1))
        print u"系统获取的回复链接：",self.upsideUrlTail
        return True
        

    def getPageUrl(self):
        request  = urllib2.Request(self.loginUrl,self.postData,self.loginHeaders)
        response = self.opener.open(request)
        page = response.read().decode('gb2312')
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
        print u"系统生成的回复链接：",self.upsideUrl
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
    
    def contentTranscoding(self):
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
        self.contentTranscoding()
                    
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
        self.initLoginData(username,password)
        del self.userinfor[username]
        
    def start(self):
        for num in range(0,self.maxUserNum):
            if not self.userinfor:
                break           
            self.initIP()
            self.chooseUser()
            self.workItOut()
            if not self.upsideUrl:
                break
            time.sleep(random.randint(3,5))
        print u"任务完成！"            

sdu = SDU()
if sdu.getUpsideUrlTail():
    sdu.start()
else:
    print u"任务失败！"
