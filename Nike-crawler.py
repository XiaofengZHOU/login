#%%
from bs4 import BeautifulSoup
from tools import get_html_doc
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys

#%%

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['handleAlerts'] = True
firefox_capabilities['acceptSslCerts'] = True
firefox_capabilities['acceptInsecureCerts'] = True
geckoPath = 'geckodriver-017.exe'
browser = webdriver.Firefox(capabilities=firefox_capabilities, executable_path=geckoPath)


#%%
nike_url = "https://www.nike.com/cn/zh_cn/"
browser.get(nike_url)
time.sleep(2)

#%%
browser.find_element_by_css_selector('li.exp-join-login button').click()



#%%
email = browser.find_element_by_xpath("//input[@name='emailAddress']")
email.clear()
email.send_keys("1070015556@qq.com")
password = browser.find_element_by_xpath("//input[@name='password']")
password.clear()
password.send_keys("Ding87yuanyu09")
login_button = browser.find_element_by_xpath("//input[@value='登录']")
login_button.click()
#%%

product_url = "https://www.nike.com/cn/t/lebron-15-ep-%E7%94%B7%E5%AD%90%E8%BF%90%E5%8A%A8%E9%9E%8B-0nTgJ11M/897649-300"
browser.get(product_url)
page_source = browser.page_source
soup = BeautifulSoup(page_source, "html.parser")
sizes_preferred = ["42","42.5","43","41"]
sizes = soup.find("div", {"name":"skuAndSize"}).find_all("input", {"name":"skuAndSize"})
for size in sizes :
    if size.has_attr('disabled'):
        continue
    else:
        print(size.attrs['id'],' : ',size.attrs['aria-label'])

#%%


input_size = browser.find_element_by_xpath("//label[@for='skuAndSize__20448527:40.5']")
input_size.click()
buy_button = browser.find_element_by_class_name("addToCartBtn")
buy_button.click()
