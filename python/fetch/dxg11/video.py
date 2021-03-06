#!/usr/bin python
# -*- coding: utf-8 -*-
from baseparse import *
from urlparse import urlparse
from common import common
from urllib import unquote
import time
from fetch.profile import *
from urllib import unquote

class VideoParse(BaseParse):

    def __init__(self):
        pass

    def run(self):
        dbVPN = db.DbVPN()
        ops = db_ops.DbOps(dbVPN)
        chs = self.videoChannel()
        for item in chs:
            ops.inertVideoChannel(item)
        print 'dxg11 video -- channel ok;,len=',len(chs)
        dbVPN.commit()
        dbVPN.close()
        for item in chs:
            for i in range(1, maxVideoPage):
                url= item['url']
                if i!=1:
                    url= "%s%s%s"%(item['url'].replace('1.html',''),i,".html")
                self.videoParse(item['channel'], url)
                print '解析完成 ', item['channel'], ' ---', i, '页'
    def videoChannel(self):
        channelList=[]
        for item in channelMap:
            obj={}
            obj['name']=item.get("name")
            obj['url']=item.get("url")
            obj['baseurl']=baseurl
            obj['updateTime']=datetime.datetime.now()
            obj['pic']=''
            obj['rate']=0.7
            obj['channel']="dxg11"+item.get("url")
            obj['showType']=1
            obj['channelType']='normal'
            channelList.append(obj)
        return channelList
    def videoParse(self, channel, url):
        dataList = []
        soup = self.fetchUrl(url)
        ul = soup.first("ul",{"id":"waterfall"})
        if ul!=None:
            lis = ul.findAll("div",{"class":"c cl"})
            for li in lis:
                ahref = li.first("a")
                if ahref != None:
                    obj = {}
                    mp4Url = self.parseDomVideo(ahref.get("href"))
                    if mp4Url == None:
                        print '没有mp4 文件:', ahref.get("href")
                        continue
                    obj['url'] = mp4Url
                    img = ahref.first("img")
                    if img!=None:
                        obj['pic'] = baseurl+img.get("src")
                    else:
                        obj['pic']=""
                    obj['name'] = ahref.get("title")
                    videourl = urlparse(obj['url'])
                    obj['path'] = videourl.path
                    obj['updateTime'] = datetime.datetime.now()
                    if mp4Url.count("m3u8")==0 or mp4Url.count("url=")!=0:
                        obj['videoType'] = "webview"
                    else:
                        obj['videoType'] = "normal"
                    obj['channel'] = channel
                    obj['baseurl'] = baseurl
                    print obj['videoType'],obj['name'],obj['url'],obj['pic']
                    dataList.append(obj)
        dbVPN = db.DbVPN()
        ops = db_ops.DbOps(dbVPN)
        for obj in dataList:
            ops.inertVideo(obj,obj['videoType'],baseurl)

        print 'zanquye video --解析完毕 ; channel =', channel, '; len=', len(dataList), url
        dbVPN.commit()
        dbVPN.close()

    def parseDomVideo(self, url):
      
        try:
            soup = self.fetchUrl(url)
            iframe = soup.first("iframe")
            if iframe!=None:
                ahref = iframe.get("src")
                if ahref!=None:
                    soup = self.fetchUrl(ahref)
                    scripts = soup.findAll("script")
                    for script in scripts:
                        if script.text!=None:
                            content = unquote(str(script.text))
                            match = regVideo.search(content)
                            if match!=None: 
                                return "http"+match.group(1)+'index.m3u8'
            print '没找到mp4'
            return None
        except Exception as e:
            print common.format_exception(e)
            return None

def videoParse(queue):
    queue.put(VideoParse())
