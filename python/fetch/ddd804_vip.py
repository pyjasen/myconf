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
from ddd804 import *
import re
import sys
from fetch.ddd804 import *
reload(sys)
sys.setdefaultencoding('utf8')

def parsejiqingyazhouImg():
    imgop = imgjiqingyazhou.ImgParse()
    imgop.run()
def parse39vqImg():
    imgop = img39vq.ImgParse()
    imgop.run()
def parse3wujiImg():
    imgop = img3wuji.ImgParse()
    imgop.run()
def parse58589sImg():
    imgop = img58589s.ImgParse()
    imgop.run()
def parse52cjgImg():
    imgop = img52cjg.ImgParse()
    imgop.run()
def parsejjj382Img():
    imgop = imgjjj382.ImgParse()
    imgop.run()
def parse65aeaeImg():
    imgop = img65aeae.ImgParse()
    imgop.run()
def parseasy1000Img():
    imgop = img65aeae.ImgParse()
    imgop.run()
def parsAll():
#     parsejiqingyazhouImg()
#     parse39vqImg()
#     parse3wujiImg()
#     parse58589sImg()
#     parse52cjgImg()
    parsejjj382Img()
    parse65aeaeImg()
    parseasy1000Img()
if __name__ == '__main__':
    parseasy1000Img()
#     parse39vqImg()
# #      
#     parsedddImg()
#     parsejiqingyazhouImg()
