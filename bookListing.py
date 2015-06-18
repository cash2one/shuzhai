__author__ = 'vincentnewpro'
import json
class BookListing(object):
    bookTitle = ''
    sectionTitle=''
    docid = 0
    url = ''
    summary = ''
    intro=''
    imgs = []
    category=''
    categoryid=''
    publisher=''
    initTime=0
    createTime=0
    author =''
    keywords=[]
    textBody=''
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
    def to_DICT(self):
        return json.loads(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
    #    def __init__(self,title,docid,url,summary,imgurl,category,publisher):
#        self.title = title
#        self.docid = docid
#        self.url = url
#        self.summary = summary
#        self.imgurl = imgurl
#        self.category = category
#        self.publisher = publisher
