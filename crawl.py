#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'vincentnewpro'

from pymongo import MongoClient
from bookListing import BookListing
import requests
import json
from robobrowser import RoboBrowser
import re, os
import time
import chardet
import sys
from mongo import writeToMongo
from timeConvertor import parse_datetime

class ShuzhaiCrawl:
    client = MongoClient()
    client = MongoClient('107.170.115.138', 27017)
    db = client['shuzhai']
    collection = db['shuzhai_lists']
    # Browse to Rap Genius
    browser = RoboBrowser(history=True,user_agent='Mozilla/5.0 ... Safari/537.36')

    def crawTengxun(self):
        start = 1
        end = 5
        urlStr = "http://cul.qq.com/c/shuzhaiList_%d.htm"
        for x in range(start,end):
            finalUrl = urlStr % (x)
            self.browser.open(finalUrl,method='get',headers={'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',"Content-Type":"text/html; charset=GB2312",
                                                                                                      'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.3'})
            if self.browser.response.status_code is not 200:
                break
            else:
                lists = self.browser.select('#listZone1 li')
                text = lists[0]
                text
                #print(self.browser.parsed)
                pass

    def convert_utf(self, body , text):
        content_type = chardet.detect(body)
        encoding = content_type['encoding']
        if encoding == 'GB2312':
            encoding = 'GBK'
        if encoding != 'UTF-8':
            reload(sys)
            sys.setdefaultencoding(encoding)
            text = text.decode(encoding, 'ignore')
        text = text.encode('utf-8')
        return text

    def crawlWeibo(self):
        start = 560
        end = 561
        urlStr = "http://feed.mix.sina.com.cn/api/roll/get?pageid=96&lid=%d&num=%d"
        for x in range(start,end):
            print("x=%d"%x)
            finalUrl = urlStr % (x,1)
            r = requests.get(finalUrl)
            jsonData = r.json()
            if jsonData['result']['status']['code']==0:
                totoalNumb = jsonData['result']['total']
                finalUrl = urlStr %(x,totoalNumb)
                print "found:"+finalUrl
                r = requests.get(finalUrl)
                thisJson = r.json()
                fileName = 'resources/'+"weibo_lid_"+str(thisJson['result']['lid'])+".json"
                with open(fileName, "w") as outfile:
                    json.dump(thisJson,outfile)

    def processWeibo(self,targetFile=None):
        listResource = os.listdir("resources") if targetFile==None else [targetFile]
        for file in listResource:
            if 'weibo_' in file:
                with open('resources/'+file,'r') as f:
                    jsondata = json.load(f)
                    i = 0
                    for bookListing in jsondata['result']['data']:
                        print(i)
                        aBook = self.readingWeiboBookListing(bookListing)
                        #json.dump(aBook.to_JSON().decode('utf-8'),targetFile)
                        #aBookDict = aBook.to_JSON()
                        if aBook is not None:
                            writeToMongo(aBook.__dict__)
                            i+=1


    def readingWeiboBookListing(self,bookListing):
        url = bookListing['wapurl']
        if  '?sa=' in url or  len(url)==0:
            url = bookListing["url"]

        bookListingObj = BookListing()
        bookListingObj.initTime = bookListing['intime']
        bookListingObj.createTime = int(time.time())
        bookListingObj.url = url
        #img
        imgs = bookListing['images']
        bookListingObj.imgs = imgs
        bookListingObj.docid = bookListing['oid']
        bookListingObj.summary = bookListing['summary']
        bookListingObj.intro = bookListing['intro']
        #keyword
        keywords = bookListing['keywords'].split(',')
        bookListingObj.keywords = keywords

        if 'play.php' in url:
            self.browser.open(url,method='post',headers={'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
                                                         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.3'})
            if len(self.browser.select('.chapter-title'))==0: return
            sectionTitle = self.browser.select('.chapter-title')[0].text
            bookTitle = self.browser.select('.chapter-caption > span')[0].text
            author =  self.browser.select('.chapter-caption a')[0].text if len(self.browser.select('.chapter-caption a'))>0 else ''
            contents = self.browser.select('.novel p')
            textbody = self.makeupcontent(contents)
            # setup book
            bookListingObj.bookTitle = bookTitle
            categoryList = self.getCategory(textbody)
            bookListingObj.category = categoryList[1]
            bookListingObj.categoryid = categoryList[0]
            bookListingObj.sectionTitle = sectionTitle
            bookListingObj.author = author
            bookListingObj.textBody = textbody
        else:
            self.browser.open(url,method='get',headers={'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
                                                         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.3'})
            #Style 1
            if len(self.browser.select(".blk_abstract"))>0:
                try:
                    bookTitle = self.browser.select('.blk_abstract a')[0].text
                except:
                    bookTitle = ''
                    print('can not parse book title:'+url)

                sectionTitle = self.browser.select('#artibodyTitle')[0].text
                try:
                    author = self.browser.select('.blk_abstract a')[1].text
                except:
                    author=''
                    print('can not parse book author:'+url)

                try:
                    publiser = self.browser.select('.blk_abstract a')[2].text
                except:
                    publiser=''
                    print('can not parse book publiser:'+url)

                contents = self.browser.select('#artibody p')
                textbody = self.makeupcontent(contents)

                bookListingObj.bookTitle = bookTitle
                bookListingObj.sectionTitle = sectionTitle
                bookListingObj.author = author
                bookListingObj.publisher = publiser
                bookListingObj.textBody = textbody
                categoryList = self.getCategory(textbody)
                bookListingObj.category = categoryList[1]

            #Style 2
            if len(self.browser.select('.blkContainerSblk'))>0:
                sectionTitle = self.browser.select('#artibodyTitle')[0].text
                contents = self.browser.select('#artibody p')
                textbody = self.makeupcontent(contents)
                categoryList = self.getCategory(textbody)
                bookListingObj.category = categoryList[1]
                bookListingObj.textBody = textbody
                bookListingObj.sectionTitle = sectionTitle
                try:
                    bookTitle = re.search('%s(.*)%s' % ('摘自'.decode('utf-8'), '》'.decode('utf-8')), textbody).group(1)+"》".decode('utf-8')
                    bookListingObj.bookTitle = bookTitle
                except:
                    print('can not parse book title:'+url)

        return bookListingObj







    def getCategory(self,text):
        self.browser.open('http://nlp.csai.tsinghua.edu.cn/app/ClassifierSys/FrontPage.jsp',headers={'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
                                                                                                  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.3'})
        form = self.browser.get_form(action="Result.jsp")
        textArea = form['article']
        textArea.value = text
        self.browser.submit_form(form)
        results = self.browser.select('.STYLE7')
        categoryId = results[0].text
        categoryName = results[1].text
        print(categoryId+" "+categoryName)
        return [categoryId,categoryName]



    def makeupcontent(self,lines):
        content=''
        for line in lines:
            content+=line.text
            content+="\n\n"
        return content




#print(r.text)
#bookL = BookListing()
#bookL.title = 'abc'
#print(bookL.to_JSON())
#print(int(time.time()))
a = ShuzhaiCrawl()
#a.processWeibo('weibo_lid_560.json')
#print(parse_datetime(u"1995年6月10号下午3点41分50秒"))
#a.crawlWeibo()

a.crawTengxun()