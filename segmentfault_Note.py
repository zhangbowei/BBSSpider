# -*- coding:utf-8 -*-
import urllib2
import re

# 处理页面标签类


class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

# 百度贴吧爬虫类


class BDTB:

    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl):
        # base链接地址
        self.baseURL = baseUrl
        # 是否只看楼主
        self.seeLZ = '/notes?page='
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 全局file变量，文件写入操作对象
        self.file = None

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            # 构建URL
            url = self.baseURL + self.seeLZ + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # 返回UTF-8格式编码内容
            return response.read().decode('utf-8')
        # 无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败,错误原因", e.reason
                return None

    def isPageExist(self, page):
        # 获取帖子页数的正则表达式
        pattern = re.compile(
            '(\D)</a></li></ul></div></div></div></div></div>', re.S)
        result = re.search(pattern, page)
        if result:
            return True
        else:
            return False

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        # 匹配所有楼层的内容
        pattern = re.compile(
            '<a class="profile-mine__content--title" href="(.*?)">(.*?)</a>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            # 将文本进行去除标签处理，同时在前后加入换行符
            content = "[" + item[1] + "]" + \
                "(https://segmentfault.com" + item[0] + ") "
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self, title):
        self.file = open(title + ".md", "w+")

    def writeData(self, contents):
        # 向文件写入每一楼的信息
        for item in contents:
            # 楼之间的分隔符
            floorLine = "\n---\n"
            self.file.write(floorLine)
            self.file.write(item)

    def start(self):
        self.setFileTitle('link')
        i = 1
        while(True):
            print "正在写入第" + str(i) + "页数据"
            page = self.getPage(i)
            contents = self.getContent(page)
            self.writeData(contents)
            if not (self.isPageExist(page)):
                break
            i = i + 1
        print "写入任务完成"

print u"请输入帖子代号"
# baseURL = 'https://segmentfault.com/u/' + str(raw_input('请输入账户名：'))
baseURL = 'https://segmentfault.com/u/' + 'zhangbowei'
bdtb = BDTB(baseURL)
bdtb.start()
