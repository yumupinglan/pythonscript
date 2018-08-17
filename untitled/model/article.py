class Article:
    name = ""
    imgNumber = 0
    commentNum = 0
    url = ''
    author = ''
    imgList = []
    paragraphList = []

    def toString(self):
        return 'name :'+self.name+', imgNumber:'+str(self.imgNumber)+', commentNum:'\
               +str(self.commentNum)+', url:'+self.url+', author'\
                +self.author