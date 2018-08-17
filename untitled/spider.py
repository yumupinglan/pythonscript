import subprocess
import time

from selenium.webdriver.firefox.options import Options

import DBHelper
from selenium.webdriver import ActionChains
import imghdr
import model.article
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re


class SpiderTouTiao:

    def getWebDirver(self,type):
        if type == 0:
            return webdriver.Chrome('/opt/chrome/chromedriver')
        if type == 1:
            options = Options()
            options.headless=True
            driver = webdriver.Firefox(firefox_options=options)
            return driver

    def getArticles(self, url):
        driver = self.getWebDirver(1)
        driver.delete_all_cookies()
        print('spider picture from:'+url)
        driver.get(url)
        try:
            loadFinish = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'des'))
            )
            for i in range(0,20):
                print('load more pictures from:'+url)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)

            artcileElements = driver.find_elements_by_class_name('img-item')
            articles = []
            for element in artcileElements:
                name = element.find_element_by_class_name('des').text;
                name = re.sub('\s', '', name)
                uri = element.find_element_by_tag_name('a').get_attribute('href')
                imgNumber = element.find_element_by_class_name('pic-num').text
                extra = element.find_element_by_class_name('extra')
                author = extra.find_elements_by_tag_name('span')[0].text
                commentNum = '0评论'
                if len(extra.find_elements_by_tag_name('span')) > 1:
                    commentNum = extra.find_elements_by_tag_name('span')[1].text
                article = model.article.Article()
                article.name = name
                article.url = uri
                article.author = author
                article.imgNumber = int(imgNumber[0:(len(imgNumber)-1)])
                article.commentNum = int(commentNum[0:(len(commentNum)-2)])
                articles.append(article)

            return articles
        finally:
            driver.quit()

    def getImageAndText(self,article):
        driver = self.getWebDirver(1)
        driver.get(article.url)
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'abstract-index'))
            )
            topElement = driver.find_element_by_class_name('image-list')
            sourceImageList = topElement.find_elements_by_tag_name('a')
            if len(sourceImageList) != article.imgNumber :
                return
            imageList = []
            textList = []
            for i in range(0,article.imgNumber):
                imgUrl = sourceImageList[i].get_attribute('href')
                imageList.append(imgUrl)
                textElement = driver.find_element_by_class_name('abstract')
                textList.append(str(textElement.text)[4:])
                ActionChains(driver).move_to_element(topElement).click(topElement).perform()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'abstract-index'))
                )
            article.imgList = imageList
            article.paragraphList = textList
        finally:
            driver.quit()

    def genereateFiles(self,article,path):
        for i in range(0,article.imgNumber):
            fileOrder = ''
            if i >= 10:
                fileOrder = '0'+str((i+1))
            elif i < 10:
                fileOrder = '00'+str((i+1))
            picName = path+"orig" + fileOrder+'.info';
            textName = path+'text' + fileOrder+'.txt'
            print(article.imgList[i])
            ir = requests.get(article.imgList[i])
            if ir.status_code == 200:
                open(picName, 'wb').write(ir.content)
            type = imghdr.what(picName)
            newPicName = picName.replace('info',type)
            cmd = ['mv',picName,newPicName]
            cmd = map(lambda x: '%s' % x, cmd)
            subprocess.call(cmd)
            open(textName, 'w').write(article.paragraphList[i])
        titleName = path+'title.txt'
        open(titleName, 'w').write(article.name)

    def spiderTouTiao(self,path):
        url = 'https://www.toutiao.com/ch/news_image/'
        articles = self.getArticles(url)
        for article in articles:
            self.getImageAndText(article)
            self.genereateFiles(article, path)
            print(article.toString())

if __name__ == '__main__':
    url = 'https://www.toutiao.com/ch/news_image/'
    spider = SpiderTouTiao()
    articles = spider.getArticles(url)
    for article in articles:
        spider.getImageAndText(article)
        spider.genereateFiles(article,'/home/willieyu/youtubeWork/article/')
        print(article.toString())
