from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getWebDirver(type):
    if type == 0:
        return webdriver.Chrome('/opt/chrome/chromedriver')
    if type == 1:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)  # 1代表手动设置
        profile.set_preference("network.proxy.socks", "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", 1080)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile)
        return driver
        # option = Options()
        # #option.proxy = Proxy({'socksProxy':'140.82.47.171:8888','socksUsername':'','':''})
        # option.add_argument("--proxy-server=socks5://127.0.0.1:1080");
        # return webdriver.Firefox(options=option)

def loginYoutube(url):
    driver = getWebDirver(1)
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, 'svg'))
    )
    print('load OK')
    #loginButton = driver.find_element_by_partial_link_text('https://accounts.google.com/ServiceLogin')
    loginButton = driver.find_element_by_xpath("//a[@class='yt-simple-endpoint style-scope ytd-button-renderer']")
    print(loginButton.tag_name)
    ActionChains(driver).move_to_element(loginButton).click(loginButton).perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'input'))
    )
    inputs = driver.find_elements_by_tag_name('input')
    for input in inputs:
        print('tagName:'+input.tag_name+', class:'+input.get_attribute('class'))

    nextButton = driver.find_element_by_id('identifierNext')
    print(nextButton)
if __name__ == '__main__':
    path = 'https://www.youtube.com/watch?v=T3WtuIddokQ'
    loginYoutube(path)