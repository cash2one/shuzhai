# -*- coding:utf-8 -*-
from __future__ import print_function, unicode_literals
__author__ = 'vincentnewpro'


import pymongo
import datetime
from pymongo import MongoClient
from robobrowser import RoboBrowser

from bosonnlp import BosonNLP

client = MongoClient()
client = MongoClient('107.170.115.138', 27017)
#client = MongoClient('mongodb://localhost:27017/')
db = client['Shuzhai']
post_collection = db['BookListings']

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

post_id=post_collection.find

browser = RoboBrowser(history=True,user_agent='Mozilla/5.0 ... Safari/537.36')
browserHeaders = {'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',"Content-Type":"text/html; charset=GB2312",
                  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.3'}

i=1
#for post in post_collection.find():
#    if "author" in post and len(post['author'])>50:
#        #print("author -->"+post['author'])
#        #print("textBody -->"+post['textBody'])
#        if True:
#            print(post['url'])
#            print(post['_id'])
#            browser.open(post['url'],method='get',headers=browserHeaders)
#            contents = browser.select('.split')
#            textBody = ''
#            getAuthorLine = False
#            for line in contents:
#                if getAuthorLine == False and line.text.find(u'》')!=-1 and line.text.find(u'《')!=-1 and line.text.find(u'出版')!=-1 and line.text.find(u'年')!=-1  and line.text.find(u'月')!=-1 :
#                    authLine =  line.text.split(u'。')[0]
#                    bookTitle=authLine[authLine.find(u'《')+len(u'《'):authLine.find(u'》')]
#                    #print(authLine)
#                    #print(bookTitle)
#                    post['bookTitle'] = u'《'+bookTitle+u'》'
#                    #post_collection.save(post)
#                    getAuthorLine = True
#
#                    print authLine
#                    for segment in authLine.split(u'，'):
#                        if u'出版社' in segment:
#                            print "publisher: "+segment
#                            post['publisher'] = segment
#                        if u'著' in segment or u'编' in segment:
#                            post['author'] = segment
#                            print "author "+segment
#
#                post_collection.save(post)
nlp = BosonNLP('ACkGzbZN.3168.-59p6xUUT4Y-')
nlp.cluster(['今天天气好', '今天天气好', '今天天气不错', '点点楼头细雨',
                         '重重江外平湖', '当年戏马会东徐', '今日凄凉南浦'])

#for post in post_collection.find():
#    print(post['url'])
#    if 'sina' in post['url'] or 'weibo' in post['url'] and len(post['keywords'])<9:
#        textbody = post['textBody']
#        textbody = textbody.replace("\n\n", "")
#        result = nlp.extract_keywords(textbody, top_k=10)
#        keywords = []
#        print(textbody)
#        for weight,word in result:
#            print(weight)
#            print(word)
#            print('\n')
#            keywords.append(word)
#        print(post['url'])
#        post['keywords'] = keywords
#        post_collection.save(post)

#        print post['bookTitle']
#        browser.open(post['url'],method='get',headers=browserHeaders)
#        contents = browser.select('.split')
#        textBody = ''
#        getAuthorLine = False
#        for line in contents:
#            if len(line.text)>200:
#                print(line.text)
#                post['textBody'] = line.text
#                post_collection.save(post)
#                i+=1
#                print(i)
#
#            if getAuthorLine == False and line.text.find(u'》')!=-1 and line.text.find(u'《')!=-1 and line.text.find(u'出版')!=-1 and line.text.find(u'年')!=-1  and line.text.find(u'月')!=-1 :
#                authLine =  line.text.split(u'。')[0]
#                bookTitle=authLine[authLine.find(u'《')+len(u'《'):authLine.find(u'》')]
#                #print(authLine)
#                #print(bookTitle)
#                post['bookTitle'] = u'《'+bookTitle+u'》'
#                #post_collection.save(post)
#                getAuthorLine = True