#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import urllib2
import threading
from BeautifulSoup import BeautifulSoup
from common.envmod import *
from common import common
from common import typeutil
from common import db_ops
from common import MyQueue
from common import dateutil
from common import html_parse
import re
import os
import sys
import time
from urlparse import urlparse
reload(sys)
sys.setdefaultencoding('utf8')
queue = MyQueue.MyQueue(20000)
fileOrige = "/home/file/img_orige/"
fileCompress = "/home/file/img_compress/"
max_count = 10
idlist = []


def syncImgsObj():
    dbVPN = db.DbVPN()
    ops = db_ops.DbOps(dbVPN)
    objs = ops.getImgItems_itemUnSyncById(idlist)
    dbVPN.close()
    for obj in objs:
        ext = os.path.splitext(obj['picUrl'])[1]
        out = fileOrige + str(obj['id']) + ext
        os.system("wget -O %s %s " % (out, obj['picUrl']))
        os.system("mogrify  -resize 80%x80% " + out)
        print 'sync imgok url=', obj['picUrl']


def mv0K():
    os.system(
        "sudo ls -l %s -h | awk -F' ' '{print$5" "$9}' | awk -F' ' '$1==0{print$2}'  | xargs -t -i mv %s{} /mnt/file/test/{}" % (fileOrige, fileOrige))


def getImgs():
    dbVPN = db.DbVPN()
    ops = db_ops.DbOps(dbVPN)
    items = ops.getImgItems_itemId()
    dbVPN.close()
    return items


def listDir():
    lists = os.listdir(fileOrige)
    names = []
    for item in lists:
        names.append(
            item.replace(".jpg", '').replace(".png", '').replace(".jpeg", ''))
    return names


def fix1():
    lists = os.listdir(fileOrige)
    count = 0
    for item in lists:
        out = fileOrige + item
        path = fileCompress + item
        if os.path.exists(path) == False:
            os.system("convert  -resize 50%x50% " + out + ' ' + path)
            print item, count, (count % 50)
            count += 1
            if (count % 150) == 0:
                print 'sleep'
                time.sleep(5)


def fix2():
    fh = open('fix_img.txt')
    count = 0
    for line in fh.readlines():
        if line.count("http") > 0:
            urls = line.split(",")
            if len(urls) != 2:
                print 'error', line
                continue
            ext = os.path.splitext(urls[1])[1]
            out = fileOrige + \
                str(urls[0]) + ext.replace('\n', '').replace('\r', '')
            outjpg = fileOrige + str(urls[0]) + '.jpg'
            print "wget -O %s %s " % (out, urls[1])
            ret = os.system("wget -O %s %s " % (out, urls[1]))
            if ret != 0:
                print '没找到图片', urls[1], urls[0]
                continue
            os.system("mogrify  -resize 80%x80% " + out)
            if ext != 'jpg':
                os.system("convert  %s %s " % (out, outjpg))
                print 'convert to jpg'
#             outComjpg = fileCompress + str(urls[0]) + '.jpg'
#             commond = "convert  -resize 50%x50% " + outjpg + "  " + outComjpg
#             print commond
#             os.system(commond)
#             count += 1
#             if (count % 150) == 0:
#                 print 'sleep'
#                 time.sleep(5)


def fix3():
    dbVPN = db.DbVPN()
    ops = db_ops.DbOps(dbVPN)
    sortType = dateutil.y_m_d()
    items = ops.getImgItems_itemBySortType(sortType)
    dbVPN.close()
    for obj in items:
        ext = os.path.splitext(obj['picUrl'])[1]
        out = fileOrige + str(obj['id']) + ext
        path = fileCompress + str(obj['id']) + ext
        os.system("wget -O %s %s " % (out, obj['picUrl']))
        os.system("mogrify  -resize 80%x80% " + out)
        os.system("convert  -resize 50%x50% " + out + ' ' + path)
        print 'sync imgok url=', obj['picUrl']
if __name__ == '__main__':
    mv0K()
#     print 'mv ok'
#     imgIds = getImgs()
#     print 'imgIds ok'
#     names = listDir()
#     print 'listDir ok'
#     for imgId in imgIds:
#         if names.count(str(imgId)) == 0:
#             idlist.append(imgId)
#     print len(idlist), idlist
#     syncImgsObj()
#     fix1()
#     fix2()
    fix3()
