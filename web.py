#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re


class Spider:
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
            '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
            re.S)
        items = re.findall(pattern, page)
        i = 0;
        for item in items:
            print item[0], item[1], item[2], item[3], item[4]
            self.saveImage("http:"+item[1],i)
            i = i + 1


    def saveImage(self,imageurl,name):
        u = urllib.urlopen(imageurl)
        data = u.read()
        f = open("/root/workspace/"+str(name) + ".jpg","wb")
        f.write(data)
        f.close()



spider = Spider()
spider.getContents(2)



