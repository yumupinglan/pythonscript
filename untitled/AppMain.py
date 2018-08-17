import os
import time
from shutil import rmtree
from covert import mytool
import DBHelper
import UploadYoutube
from spider import SpiderTouTiao

if __name__ == '__main__':
    DBHelper.create_table()
    UploadYoutube.loadConfig()
    path = '/home/willieyu/youtubeWork/article/'
    videoPath = '/home/willieyu/youtubeWork/'
    url = 'https://www.toutiao.com/ch/gallery_old_picture/'
    spider = SpiderTouTiao()
    mytool = mytool()
    while 1 > 0:
        articles = spider.getArticles(url)
        for article in articles:
            try:
                if DBHelper.findArticle(article.url) == 0:
                    spider.getImageAndText(article)
                    spider.genereateFiles(article, path)
                    mytool.genereateVideo(path,videoPath)
                    print(article.toString())
                    videoName = mytool.simple2tradition(article.name)+'.mp4'
                    UploadYoutube.upload(videoPath+videoName,videoName)
                    DBHelper.insertArticle(article)
                    mytool.rm_file(videoPath+videoName)
            except Exception:
                DBHelper.insertArticle(article)
                #mytool.rm_file(videoPath + videoName)
                rmtree(path)
                os.mkdir(path)
        print('start to sleep: 5000s')
        time.sleep(1200)
