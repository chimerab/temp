#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import paramiko
import subprocess
import urllib
import re
import time

def timeit(func):
    def wrapper():
        start = time.clock()
        func()
        end = time.clock()

        print "time been used :%s" % str(end - start)

    return wrapper()


def ssh_command(ip,user,passwd,command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/root/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip,port=22,username=user,password=passwd)
    except Exception,e:
        print "The error is:" + str(e)
        return

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)

    return

#ssh_command("123.56.xxx","root","xxxx","id")


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImage(html):
    reg = r'http://img.+?\.jpg'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)

    x = 0
    for pic in imglist:
        #urllib.urlretrieve(pic,"%s.jpg"%x)
        x = x + 1
    return imglist

@timeit
def foo():
    print "This is foo"



#html = getHtml("http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=2&fmq=1480332039000_R_D&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%BE%AE%E8%B7%9D%E6%91%84%E5%BD%B1")

#print getImage(html)




















