__author__ = 'vincentnewpro'

import datetime
from pymongo import MongoClient
from bookListing import BookListing
import requests
import json
from robobrowser import RoboBrowser
import glob, os
import time

class ShuzhaiCrawl:
    client = MongoClient()
    client = MongoClient('107.170.115.138', 27017)
    db = client['shuzhai']
    collection = db['shuzhai_lists']
    # Browse to Rap Genius
    browser = RoboBrowser(history=True,user_agent='Mozilla/5.0 ... Safari/537.36')

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
                        self.readingWeiboBookListing(bookListing)
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
            sectionTitle = self.browser.select('.chapter-title')[0].text
            bookTitle = self.browser.select('.chapter-caption > span')[0].text
            author = self.browser.select('.chapter-caption a')[0].text
            contents = self.browser.select('.novel p')
            textbody = self.makeupcontent(contents)
            # setup book
            bookListingObj.bookTitle = bookTitle
            categoryList = self.getCategory(textbody)
            bookListingObj.category = categoryList[1]
            bookListingObj.categoryid = categoryList[0]
            bookListingObj.sectionTitle = sectionTitle
            bookListingObj.author = author
        else:
            self.browser.open(url,method='get',headers={'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
                                                         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.3'})
            print(self.browser.parsed)
        #print(bookListing)
        #print("\n")





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
#print(bookL.title)
#print(int(time.time()))
a = ShuzhaiCrawl()
#a.processWeibo('weibo_lid_544.json')
a.crawlWeibo()