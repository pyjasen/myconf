#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import zlib
import urllib2
import threading
from common.envmod import *
from common import db_ops
from common import common
import threading
from BeautifulSoup import BeautifulSoup
import re
import os
baseurl = "https://7mm.tv"
header = {'Cookie':'__cfduid=d1d15c2d498733cada4b78811f4114c2e1548612262; PHPSESSID=c85vtnldn8mrmu7faiva3lkm50; UM_distinctid=168907bea2921b-0b38597540b9cc-47e1039-1fa400-168907bea2d352; HstCfa3415871=1548612268811; HstCmu3415871=1548612268811; c_ref_3415871=https%3A%2F%2Fwww.google.com%2F; splash_i=false; SC_unique_550883=0; SC_unique_553058=0; CNZZDATA1273421816=777958336-1548610618-%7C1548610618; SC_unique_563786=1; _ga=GA1.2.1331595716.1548614082; _gid=GA1.2.117258503.1548614082; CNZZDATA1273377176=2093245763-1548609279-https%253A%252F%252Fwww.google.com%252F%7C1548649570; HstCla3415871=1548654658528; HstPn3415871=1; HstPt3415871=29; HstCnv3415871=2; HstCns3415871=3','User-Agent':
          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', "Referer": baseurl}
maxCount = 3
regVideo = re.compile(r"http(.*?)m3u8")
regVideo2 = re.compile(r'src="(https://hhvid.com|https://www.rapidvideo.com|https://www.thisav.com|https://avgle.com|https://www.bitporno.com)/(.*?)">')

class BaseParse(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def fetchUrl(self, url, aheader=header):
        count = 0
        while count < maxCount:
            try:
                req = urllib2.Request( url, headers={'Cookie':"td_cookie=18446744069599001696; UM_distinctid=16267a77486203-0a34f7eb9f837-454c092b-1fa400-16267a7748726f; CNZZDATA4033785=cnzz_eid%3D1967344694-1522153663-null%26ntime%3D1522153663; CNZZDATA1263493226=2025093065-1522155903-null%7C1522155903; PHPSESSID=cqppj1tg9v8tf27j95ogqogjs1; td_cookie=18446744069599206493; WSKY=6c172; jiathis_rdc=%7B%22http%3A//www.zxdy.cc/vod/22266.html%22%3A1739039602%2C%22http%3A//www.zxdy.cc/play/22266-0-1.html%22%3A1739044927%2C%22http%3A//www.zxdy.cc/Uploads/https%3A//tupian.tupianzy.com/pic/upload/vod/2018-03-03/201803031520062617.jpg%22%3A1739118415%2C%22http%3A//www.zxdy.cc/list/1-p-3-0.html%22%3A1739129605%2C%22http%3A//www.zxdy.cc/list/1-p-1-0.html%22%3A1739216767%2C%22http%3A//www.zxdy.cc/list/9-p-1-0.html%22%3A1739358031%2C%22http%3A//www.zxdy.cc/list/9-p-2-0.html%22%3A1739371664%2C%22http%3A//www.zxdy.cc/Uploads/https%3A//wx3.sinaimg.cn/mw690/005w5c6ogy1fjuo496v5uj30tu15ok3k.jpg%22%3A1739577535%2C%22http%3A//www.zxdy.cc/Uploads/https%3A//img.alicdn.com/imgextra/i4/2264228004/TB2UynHnQqvpuFjSZFhXXaOgXXa_%21%212264228004.jpg%22%3A1739585958%2C%22http%3A//www.zxdy.cc/%22%3A1739586271%2C%22http%3A//www.zxdy.cc/vod/5128.html%22%3A1739763188%2C%22http%3A//www.zxdy.cc/vod/1.html%22%3A1739772004%2C%22http%3A//www.zxdy.cc/play/1-0-1.html%22%3A1739777508%2C%22http%3A//www.zxdy.cc/vod/4063.html%22%3A1739811363%2C%22http%3A//www.zxdy.cc/play/4063-0-2.html%22%3A1739820736%2C%22http%3A//www.zxdy.cc/list/11-p-1-0.html%22%3A1739855919%2C%22http%3A//www.zxdy.cc/vod/22236.html%22%3A0%7C1522158279843%2C%22http%3A//www.zxdy.cc/play/22236-0-1.html%22%3A%220%7C1522158307282%22%7D"
                    ,'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html, Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13', "Referer":baseurl})
                req.encoding = 'utf-8'
                response = urllib2.urlopen(req, timeout=300)
                gzipped = response.headers.get(
                    'Content-Encoding')  # 查看是否服务器是否支持gzip
                content = response.read().decode('utf8', errors='replace')
                if gzipped:
                    content = zlib.decompress(
                        content, -zlib.MAX_WBITS)  # 解压缩，得到网页源码
                soup = BeautifulSoup(content)
                return soup
            except Exception as e:
                print common.format_exception(e)
                print '打开页面错误,重试', url, '次数', count
                count = count + 1

        print '打开页面错误,重试3次还是错误', url
        return BeautifulSoup('')
    def header(self,name):
#         content = self.fetchContentUrl(headerUrl, header)
        content=''
        print "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__)) 
        with open("mm7/"+name) as f:
            for line in f.readlines():
                content = "%s%s"%(content,line)
        soup= BeautifulSoup(content)
        alist = soup.findAll('a')
        return alist
    def fetchUrlWithBase(self, url, aheader=header):
        count = 0
        while count < maxCount:
            try:
                req = urllib2.Request(url, headers=aheader)
                content = urllib2.urlopen(req, timeout=300).read()
                soup = BeautifulSoup(content)
                return soup
            except Exception as e:
                print common.format_exception(e)
                print '打开页面错误,重试', url, '次数', count
                count = count + 1

        print '打开页面错误,重试3次还是错误', url
        return BeautifulSoup('')

    def fetchContentUrl(self, url, aheader=header):
        count = 0
        while count < maxCount:
            try:
                req = urllib2.Request(url, headers=aheader)
                content = urllib2.urlopen(req, timeout=300).read()
                return content
            except Exception as e:
                print common.format_exception(e)
                print '打开页面错误,重试', url, '次数', count
                count = count + 1

        print '打开页面错误,重试3次还是错误', url
        return ''

    