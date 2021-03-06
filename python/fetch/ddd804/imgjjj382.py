#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import threading
from common import common
from baseparse import *
from common import db_ops
from common.envmod import *
from common import dateutil
from fetch.profile import *
from urllib import unquote
class ImgParse(BaseParse):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        channels = self.parseChannel()
        dbVPN = db.DbVPN()
        ops = db_ops.DbOps(dbVPN)
        for obj in channels:
            channel = obj['name']
            page_url = obj['url']
            obj['url']=obj['name']
            ops.inertImgChannel(obj)
            soup = self.fetchUrl(baseurl8, page_url)
            strong = soup. first("strong")
            max = 255
            if strong!=None:
                texts = strong.text.split("/")
                if len(texts)==2:
                    max = int(texts[1])
            print 'max=',max
            for i in range(0, maxImgPage):
                url = page_url
                if i!=1:
                    url = url.replace('index.html',"")
                    url = "%s%s%s%s"%(url,"list_",max-i,".html")
                print url
                count = self.update(url, ops, channel, i)
                dbVPN.commit()

    def parseChannel(self):
        objs = self.fetchjjj382(baseurl8,"图片")
        for obj in objs:
            print '需要解析的channel=', obj.get('url')
            obj['updateTime'] = datetime.datetime.now()
            obj['rate'] = 1.2
            obj['showType'] = 3
            obj['channel'] = 'porn_sex'
        return objs

    def update(self, url, ops, channel, i):
        objs = self.fetchImgItemsData(url, channel)
        print "解析 Img 图片ok----channl=", channel, '  页数=', i, " 数量=", len(objs)
        for obj in objs:
            try:
                ops.inertImgItems(obj)
                for picItem in obj['picList']:
                    item = {}
                    item['itemUrl'] = obj['url']
                    item['picUrl'] = picItem
                    ops.inertImgItems_item(item)
            except Exception as e:
                print common.format_exception(e)
        return len(objs)

    def fetchDataHead(self, url):
        try:
            soup = self.fetchUrl(url)
            div = soup.first("div", {"class": "piclist"})
            if div != None:
                return div.findAll('li')

        except Exception as e:
            print common.format_exception(e)
            return []

    def fetchImgItemsData(self, url, channel):
        soup = self.fetchUrl(baseurl8,url)
        div = soup.first("div",{"class":"typelist"})
        if div!=None:
            datalist = div.findAll("ul")
            objs = []
            sortType = dateutil.y_m_d()
            for item in datalist:
                ahref = item.first("a")
                if ahref!=None:
                    try:
                        obj = {}
                        obj['fileDate'] = item.first("font",{"color":"#3C3C3C"}).text
                        name = ahref.text
                        obj['name'] = name
                        obj['url'] = ahref.get('href')
                        obj['baseurl'] = baseurl8
                        obj['channel'] = channel
                        obj['updateTime'] = datetime.datetime.now()
                        
                        pics = self.fetchImgs(obj['url'])
                        if len(pics) == 0:
                            print '没有 图片文件--', obj['url'], '---', url
                            continue
                        obj['picList'] = pics
                        obj['showType'] = 3
                        obj['pics'] = len(pics)
                        obj['sortType'] = sortType
                        print name,pics[0],'  url=', obj['url'], '  图片数量=', len(pics)
                        objs.append(obj)
                    except Exception as e:
                        print common.format_exception(e)
        return objs

    def fetchImgs(self, url):
        pics = []
        soup = self.fetchUrl(baseurl8,url)
        data = soup.first("div", {"class": "mtop"})
        if data != None:
            try:
                imgs = data.findAll('img')
                for img in imgs:
                    pics.append(unquote(str(img.get('src'))))
            except Exception as e:
                print common.format_exception(e)
        return pics
