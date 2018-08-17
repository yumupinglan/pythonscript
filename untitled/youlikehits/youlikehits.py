
from selenium.webdriver import ActionChains

from selenium.webdriver.firefox.options import Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getWebDirver(type):
    if type == 0:
        option = Options()
        # option.proxy = Proxy({'socksProxy':'140.82.47.171:8888','socksUsername':'','':''})
        option.add_argument("--proxy-server=socks5://127.0.0.1:1080");
        return webdriver.Chrome('/opt/chrome/chromedriver',options=option)
    if type == 1:
        option = Options()
        #option.proxy = Proxy({'socksProxy':'140.82.47.171:8888','socksUsername':'','':''})
        option.add_argument("--proxy-server=socks5://127.0.0.1:1080");
        return webdriver.Firefox()

def openpage(path):
    driver = getWebDirver(1)
    print('start')
    driver.get(path)
    print('load path')
    WebDriverWait(driver,10).until(
         EC.presence_of_element_located((By.ID, 'username'))
    )
    print('load ok')
    userNameElement = driver.find_element_by_id('username')
    pElement = driver.find_element_by_id('password')
    logButton = driver.find_element_by_xpath("//input[@value='Login'][@type='submit']")
    userNameElement.clear()
    userNameElement.send_keys('yumupinglan2')
    pElement.clear()
    pElement.send_keys('09yuwei@ahu')
    ActionChains(driver).move_to_element(logButton).click(logButton).perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'mainbodyloggedin'))
    )
    cookies = driver.get_cookies()
    print(cookies)
    driver.get("https://youlikehits.com/youtubelikes.php")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'followbutton'))
    )
    print('find followbutton')
    followbutton = driver.find_elements_by_class_name('followbutton')[0]
    ActionChains(driver).move_to_element(followbutton).click(followbutton).perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'likebutton'))
    )
    print('find likebutton')
    likebutton = driver.find_element_by_class_name('likebutton')
    driver.add_cookie()
    ActionChains(driver).move_to_element(likebutton).click(likebutton).perform()
    currentwin = driver.current_window_handle
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'https://accounts.google.com/ServiceLogin'))
    )
    driver.find_elements_by_partial_link_text('https://accounts.google.com/ServiceLogin')
    driver.find_elements_by_css_selector('#button > yt-icon > svg')


if __name__ == '__main__':
    path = 'https://youlikehits.com/index.php'
    openpage(path)