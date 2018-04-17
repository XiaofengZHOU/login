#!/usr/bin/env python
#coding=utf-8
#%%
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import traceback
import sys
import re
import random
import _thread


#%%
def init_browser_chrome(product_url):
	UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1","Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36")
	ua = UAS[random.randrange(len(UAS))]
	options = webdriver.ChromeOptions()
	chrome_path= "chromedriver.exe"
	options.add_argument('lang=zh_CN.UTF-8')
	options.add_argument("user-agent='" + ua + "'")
	browser = webdriver.Chrome(chrome_path,chrome_options=options)
	browser.get(product_url)
	time.sleep(random.uniform(5, 10))
	return browser

def init_browser(product_url):
	UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1","Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36")
	firefox_capabilities = DesiredCapabilities.FIREFOX
	ua = UAS[random.randrange(len(UAS))]
	firefox_capabilities['marionette'] = True
	firefox_capabilities['handleAlerts'] = True
	firefox_capabilities['acceptSslCerts'] = True
	firefox_capabilities['acceptInsecureCerts'] = True
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", ua)
	"""
	profile.set_preference("network.proxy.type", 1);
	profile.set_preference("network.proxy.socks", "122.114.31.177");
	profile.set_preference("network.proxy.socks_port", 808);
	"""
	geckoPath = 'geckodriver.exe'
	browser = webdriver.Firefox(firefox_profile=profile,capabilities=firefox_capabilities, executable_path=geckoPath)
	browser.maximize_window()
	browser.get(product_url)
	time.sleep(random.uniform(5, 10))
	return browser



def login(dd,name,password):
	wait = WebDriverWait(dd, 10)
	try:
		ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='menubar']/li")))
		webdriver.ActionChains(dd).move_to_element(ele).perform()
		time.sleep(random.uniform(0.5, 2))
		ele.click()

	except:
		print ("move to login failed")
		print (traceback.print_exc())
	time.sleep(random.uniform(2, 10))


	try:
		#ele = dd.find_element_by_xpath("//input[@name='emailAddress']")
		ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='emailAddress']")))
		ele.click()
		ele.clear()
		for letter in name:
			time.sleep(random.uniform(0.1, 0.3))
			ele.send_keys(letter)
	except:
		print ('input name failed')
		print (traceback.print_exc())
	time.sleep(random.uniform(0.5, 2))


	try:
		#ele = dd.find_element_by_xpath("//input[@name='password']")
		ele = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='password']")))
		ele.click()
		ele.clear()
		for letter in password:
			time.sleep(random.uniform(0.1, 0.3))
			ele.send_keys(letter)
	except:
		print ('input password failed')
		print (traceback.print_exc())
	time.sleep(random.uniform(6, 10))


	try:
		#ele = dd.find_element_by_xpath("//input[@value='登录']")
		ele = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='登录']")))
		webdriver.ActionChains(dd).move_to_element(ele).perform()
		time.sleep(random.uniform(0.5, 2))
		ele.click()

	except:
		print ('login submit failed')
		print (traceback.print_exc())
	time.sleep(random.uniform(6, 10))



def get_sizes_available(browser) :
	size_dict = {}
	while len(size_dict.keys())==0:
		time.sleep(0.01)
		page_source = browser.page_source
		soup = BeautifulSoup(page_source, "html.parser")
		size_tags = soup.find("div", {"name":"skuAndSize"}).find_all("input", {"name":"skuAndSize"})
		for size_tag in size_tags :
			if size_tag.has_attr('disabled'):
				continue
			else:
				size_dict[size_tag.attrs['aria-label']] = size_tag.attrs['id']
	return size_dict



def add_to_cart(browser,product_url,sizes_preferred):
	size_dict = {}
	size_dict = get_sizes_available(browser)
	print("size available: ",size_dict)
	sizes = size_dict.keys()
	for size in sizes_preferred:
		if size in sizes:
			print('has size: ',size)
			size_id = size_dict[size]
			print(size,':',size_id)
			input_size = browser.find_element_by_xpath("//label[@for='"+ size_id + "']")
			webdriver.ActionChains(browser).move_to_element(input_size).perform()
			input_size.click()
			cart_button = browser.find_element_by_class_name("addToCartBtn")
			webdriver.ActionChains(browser).move_to_element(cart_button).perform()
			cart_button.click()
			break



def pay_cart(browser):
	cart_url = "https://secure-store.nike.com/cn/checkout/html/payment.jsp"
	browser.get(cart_url)
	buy_button = browser.find_element_by_class_name("ch4_reviewBtnTopRt")
	webdriver.ActionChains(browser).move_to_element(buy_button).perform()
	buy_button.click()



def processNike(product_url,sizes_preferred,emailAddress,password):
	#browser = init_browser(product_url)
	browser = init_browser_chrome(product_url)
	login(browser,emailAddress,password)
	add_to_cart(browser,product_url,sizes_preferred)
	pay_cart(browser)
	print("finish")

#%%

ele=browser.find_element_by_css_selector('li.exp-join-login button')
webdriver.ActionChains(browser).move_to_element(ele).perform()
time.sleep(random.uniform(0.5, 2))
ele.click()

#%%
ele = browser.find_element_by_xpath("//ul[@role='menubar']/li")
time.sleep(random.uniform(0.5, 2))
ele.click()

#%%
product_url = "https://www.nike.com/cn/t/lebron-15-ep-%E7%94%B7%E5%AD%90%E8%BF%90%E5%8A%A8%E9%9E%8B-0nTgJ11M/897649-300"
emailAddress = "9437852@gmail.com"
password = "Zxf77158950625@@"
browser = init_browser(product_url)
login(browser,emailAddress,password)

#%%
user_dict = {"9437852@gmail.com":"Zxf77158950625@@","1120166237@qq.com":"Xunuozhou757","1070015556@qq.com":"Ding87yuanyu09","876838896@qq.com":"Yjq#13647285977","826849299@qq.com":"Yy5253294"}
product_url = "https://www.nike.com/cn/t/lebron-15-ep-%E7%94%B7%E5%AD%90%E8%BF%90%E5%8A%A8%E9%9E%8B-0nTgJ11M/897649-300"
sizes_preferred = ["42","42.5","43","44","44.5","40","40.5","41"]
sizes_preferred_girl = ["38","37.5","36.5","38.5","36","39","40","42","41","40.5"]
for emailAddress,password in user_dict.items():
	try:
		_thread.start_new_thread( processNike, (product_url,sizes_preferred,emailAddress,password, ) )
	except:
		print (traceback.print_exc())

#%%

user_dict = {"9437852@gmail.com":"Zxf77158950625@@"}
product_url = "https://www.nike.com/cn/t/lebron-15-ep-%E7%94%B7%E5%AD%90%E8%BF%90%E5%8A%A8%E9%9E%8B-0nTgJ11M/897649-300"
sizes_preferred = ["42","42.5","43","44","44.5","40","40.5","41"]
sizes_preferred_girl = ["38","37.5","36.5","38.5","36","39","40","42","41","40.5"]
for emailAddress,password in user_dict.items():
	processNike(product_url,sizes_preferred,emailAddress,password)
