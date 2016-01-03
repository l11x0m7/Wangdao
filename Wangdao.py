# -*- coding: utf-8 -*-
import re,sys,os
import urllib, urllib2
from docx import Document

class PhotoSpider:
    def __init__(self, page_from, page_to):
        self.start = page_from
        self.to = page_to
        self.url = 'http://m.byr.cn/board/Friends'
        self.head = 'http://m.byr.cn'
        self.dirname = 'photos'
        if not os.path.exists('photos'):
            os.mkdir('photos')

    def PagePhoto(self, page):
        real_url = self.url + '?p=' + str(page)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(real_url, headers = headers)
        try:
            myResponse = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print '[PagePhoto]:', e.code
        html = myResponse.read()
        match = re.findall(r'<li.*?<div><a href="(.*?)".*?>(.*?)</a>', html, re.S)
        for each in match:
            if '王道' in each[1].decode():
                now_url = self.head + each[0]
                self.SaveImg(now_url, each[1])

    def RangePhoto(self):
        start = self.start
        to = self.to
        count = 1
        for i in range(start, to+1):
            self.PagePhoto(i)
            print "Status:%.2f%%" % (float(count*100)/(to-start+1))
            count += 1
        print "Finish!"

    def SaveImg(self, url, tiezi):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url, headers = headers)
        try:
            myResponse = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print '[SaveImg]:', e
        html = myResponse.read()
        match = re.findall(r'a target="_blank" href="(/att.*?)">单击此查看原图', html, re.S)
        for each in match:
            name = each.strip().split('/')
            name = tiezi.decode() + name[-2] + name[-1]
            imgurl = self.head + each
            try:
                urllib.urlretrieve(imgurl, self.dirname + '/' + name + '.jpg')
            except IOError, e:
                try:
                    urllib.urlretrieve(imgurl, self.dirname + '/' + name[-2] + name[-1] + '.jpg')
                except IOError, e:
                    print '[SaveImg]:', e


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print """
    ---------------------------------------
       程序：BYR论坛照片爬取程序
       版本：0.1
       作者：lxm
       日期：2016-01-02
       语言：Python 2.7
       功能：爬取北邮人论坛上的照片
       使用：输入要爬取的网页范围（一页30个帖子）
    ---------------------------------------
    """
    start = input("where to start? ")
    to = input("where to end? ")
    spider = PhotoSpider(start, to)
    spider.RangePhoto()

