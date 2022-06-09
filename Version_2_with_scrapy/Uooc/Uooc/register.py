import time
import emoji
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions


def register():
    options = ChromeOptions()
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=options)
    # 绕过 Chrome 检测
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                          {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    driver.maximize_window()

    login = "http://www.uooc.net.cn/league/union"
    account  = 你的账号
    password = 你的密码

    time.sleep(2)
    driver.get(login)
    driver.implicitly_wait(10)
    driver.find_element(by=By.CSS_SELECTOR,value="#loginBtn").click()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element(by=By.CSS_SELECTOR,value="#layui-layer-iframe1"))
    time.sleep(1)
    driver.find_element(by=By.CSS_SELECTOR,value="#account").clear()
    driver.find_element(by=By.CSS_SELECTOR,value="#account").click()
    driver.find_element(by=By.CSS_SELECTOR,value="#account").send_keys(account)
    driver.find_element(by=By.CSS_SELECTOR,value="#password").clear()
    driver.find_element(by=By.CSS_SELECTOR,value="#password").click()
    driver.find_element(by=By.CSS_SELECTOR,value="#password").send_keys(password)
    driver.find_element(by=By.CSS_SELECTOR,value="#rectTop").click()
    time.sleep(4)
    driver.find_element(by=By.CSS_SELECTOR,value="body > div > div.loginer-body > form > button").click()
    driver.implicitly_wait(10)
    print("登录成功",emoji.emojize(":white_check_mark:",use_aliases=True)*3)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    driver.find_element(by=By.CSS_SELECTOR,value="#top_avatar").click()
    driver.find_element(by=By.CSS_SELECTOR,value="h3 > a").click()
    driver.find_element(by=By.XPATH,value="//a[@class='btn btn-lg info-bottom-btn btn-warning ng-scope']").click()
    driver.find_element(by=By.XPATH,value="//a[@class='btn btn-danger ng-binding ng-scope']").click()
    driver.implicitly_wait(5)
    chapter_ids = [i.get_attribute("id") for i in driver.find_elements(by=By.XPATH,value="//li[@class='catalogItem ng-scope']")]
    chapter_names = [i.text for i in driver.find_elements(by=By.XPATH,value="//li[@class='catalogItem ng-scope']//span[@class='oneline ng-binding']")]
    # driver.get("{}/{}".format(spider.base_url[0],chapter_ids[0]))
    return driver,chapter_names,chapter_ids
