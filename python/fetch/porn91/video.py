#!/usr/bin python
# -*- coding: utf-8 -*-
from baseparse import *
from urlparse import urlparse


class VideoParse(BaseParse):

    def __init__(self):
        pass

    def run(self):
        for i in range(2, maxPage):
            self.videoParse(channel, videoUrl % (i))

    def videoParse(self, channel, url):
        dataList = []
        soup = self.fetchUrl(url)
        divs = soup.findAll("div", {"class": "imagechannelhd"})
        for div in divs:
            ahref = div.first('a')
            if ahref != None:
                img = ahref.first('img')
                if img != None:
                    picUrl = img.get('src')
                    name = img.get('title')
                    obj = {}
                    obj['name'] = name
                    mp4Url = self.parseDomVideo(ahref.get("href"))
                    if mp4Url == None:
                        print '没有mp4 文件:', ahref.get("href")
                        continue
                    obj['url'] = mp4Url
                    videourl = urlparse(obj['url'])
                    obj['path'] = videourl.path
                    obj['updateTime'] = datetime.datetime.now()
                    obj['pic'] = picUrl
                    obj['channel'] = channel
                    dataList.append(obj)
        dbVPN = db.DbVPN()
        ops = db_ops.DbOps(dbVPN)
        for obj in dataList:
            ops.inertVideo(obj)

        print '91pron video --解析完毕 ; channel =', channel, '; len=', len(dataList), url
        dbVPN.commit()
        dbVPN.close()

    def parseDomVideo(self, url):
        soup = self.fetchUrl(url)
        source = soup.first("source", {"type": "video/mp4"})
        if source != None:
            return source.get("src")
        return None


def videoParse(queue):
    queue.put(VideoParse())
