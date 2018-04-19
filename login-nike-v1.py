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
from multiprocessing import Process
from multiprocessing import Pool
import os

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
	firefox_capabilities['marionette'] = True
	firefox_capabilities['handleAlerts'] = True
	firefox_capabilities['acceptSslCerts'] = True
	firefox_capabilities['acceptInsecureCerts'] = True
	ua = UAS[random.randrange(len(UAS))]
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", ua)
	"""
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	profile.set_preference("network.proxy.type", 1);
	profile.set_preference("network.proxy.socks", "122.114.31.177");
	profile.set_preference("network.proxy.socks_port", 808);
	"""
	geckoPath = 'geckodriver.exe'
	browser = webdriver.Firefox(firefox_profile=profile,capabilities=firefox_capabilities, executable_path=geckoPath)
	browser.maximize_window()
	try:
		browser.get(product_url)
	except:
		time.sleep(5)
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
		return False
	time.sleep(random.uniform(1, 2))


	try:
		#ele = dd.find_element_by_xpath("//input[@name='emailAddress']")
		ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='emailAddress']")))
		ele.click()
		ele.clear()
		for letter in name:
			time.sleep(random.uniform(0.2, 0.4))
			ele.send_keys(letter)
	except:
		print ('input name failed')
		print (traceback.print_exc())
		return False
	time.sleep(random.uniform(0.5, 2))


	try:
		#ele = dd.find_element_by_xpath("//input[@name='password']")
		ele = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@name='password']")))
		ele.click()
		ele.clear()
		for letter in password:
			time.sleep(random.uniform(0.2, 0.4))
			ele.send_keys(letter)
	except:
		print ('input password failed')
		print (traceback.print_exc())
		return False
	time.sleep(random.uniform(2, 4))


	try:
		#ele = dd.find_element_by_xpath("//input[@value='登录']")
		ele = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='登录']")))
		webdriver.ActionChains(dd).move_to_element(ele).perform()
		time.sleep(random.uniform(0.5, 2))
		ele.click()

	except:
		print ('login submit failed')
		print (traceback.print_exc())
	time.sleep(random.uniform(8, 10))


	try:
		ele = dd.find_element_by_xpath("//input[@value='略过此错误']")
		print(name+ " :login unsuccessful")
		return False
	except:
		print(name+" :login okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
		return True


def verify_conuntry(browser,product_url):
	cart_url = "https://secure-store.nike.com/cn/checkout/html/cart.jsp?country=CN&country=CN&l=cart"
	browser.get(cart_url)
	time.sleep(3)
	if "language" in browser.current_url:
		choose_country(browser)
		time.sleep(3)
		browser.get(product_url)
	else:
		browser.get(product_url)

def delete_article(browser):
	wait = WebDriverWait(browser, 10)
	cart_url = "https://secure-store.nike.com/cn/checkout/html/cart.jsp?country=CN&country=CN&l=cart"
	browser.get(cart_url)
	ele = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='删除']")))
	webdriver.ActionChains(browser).move_to_element(ele).perform()
	ele.click()



def get_sizes_available(browser) :
	size_dict = {}
	i=0
	while True:
		i=i+1
		try:
			page_source = browser.page_source
			soup = BeautifulSoup(page_source, "html.parser")
			size_graph = soup.find("div", {"name":"skuAndSize"})

			if size_graph == None:
				continue
			else:
				print("1 loop count:",i)
				break
		except:
			time.sleep(0.001)
			continue

	i=0
	while True:
		i=i+1
		try:
			page_source = browser.page_source
			soup = BeautifulSoup(page_source, "html.parser")
			size_graph = soup.find("div", {"name":"skuAndSize"})
			size_tags = size_graph.find_all("input", {"name":"skuAndSize"})
			for size_tag in size_tags :
				if size_tag.has_attr('disabled'):
					continue
				else:
					size_dict[size_tag.attrs['aria-label']] = size_tag.attrs['id']
			if size_dict != {}:
				print("2 loop count:",i)
				break
		except:
			time.sleep(0.001)
			continue

	return size_dict


def get_sizes_available_dropdown(browser) :
	size_dict = {}
	i=0
	while True:
		i=i+1
		try:
			ele = browser.find_element_by_xpath("//select[@name='skuAndSize']/..")
			ele.click()
			break
		except:
			time.sleep(0.001)
			continue

	while True:
		try:
			eles = browser.find_elements_by_xpath("/html/body/div[9]/div/div/div/div/div[1]/div[2]/div[4]/form/div[1]/div/div[2]/ul/li")
			if(len(eles)==0):
				continue
			for ele in eles:
				size_dict[ele.text] = ele.get_attribute('rel')
			if size_dict != {}:
				break
		except:
			time.sleep(0.001)
			continue
	return size_dict


def add_to_cart_dropdown(browser,sizes_preferred):
	size_dict = {}
	size_dict = get_sizes_available_dropdown(browser)
	sizes = size_dict.keys()
	for size in sizes_preferred:
		if size in sizes:
			print('has size: ',size)
			size_id = size_dict[size]
			print(size,':',size_id)
			input_size = browser.find_element_by_xpath("//li[@rel='"+ size_id + "']")
			webdriver.ActionChains(browser).move_to_element(input_size).perform()
			input_size.click()

			cart_button = browser.find_element_by_xpath("//button[@id='buyingtools-add-to-cart-button']")
			webdriver.ActionChains(browser).move_to_element(cart_button).perform()
			for i in range(1):
				cart_button.click()
				time.sleep(0.001)
			break

def add_to_cart(browser,sizes_preferred):
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
			for i in range(1):
				input_size.click()
				time.sleep(0.001)

			cart_button = browser.find_element_by_class_name("addToCartBtn")
			webdriver.ActionChains(browser).move_to_element(cart_button).perform()
			for i in range(1):
				cart_button.click()
				time.sleep(0.001)
			break


def pay_cart(browser):
	cart_url = "https://secure-store.nike.com/cn/checkout/html/cart.jsp?country=CN&country=CN&l=cart"
	browser.get(cart_url)
	buy_button = browser.find_element_by_class_name("ch4_reviewBtnTopRt")
	webdriver.ActionChains(browser).move_to_element(buy_button).perform()
	buy_button.click()


def pay_cart_direct_dropdown(browser):
	wait = WebDriverWait(browser, 10)
	ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='checkout-button']")))
	webdriver.ActionChains(browser).move_to_element(ele).perform()
	ele.click()
	while True:
		if "payment" in browser.current_url:
			break
		else:
			time.sleep(0.001)

	ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@value='确认并支付']")))
	ele.click()

def pay_cart_direct(browser):
	wait = WebDriverWait(browser, 10)
	ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-test='qa-cart-checkout']")))
	#buy_button = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div[2]/button[2]")
	webdriver.ActionChains(browser).move_to_element(ele).perform()
	ele.click()

	while True:
		if "payment" in browser.current_url:
			break
		else:
			time.sleep(0.001)

	ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@value='确认并支付']")))
	ele.click()


def choose_country(browser):
	wait = WebDriverWait(browser, 10)
	ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-region='asia-pac']")))
	webdriver.ActionChains(browser).move_to_element(ele).perform()
	ele.click()

	ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@data-country='CN']")))
	webdriver.ActionChains(browser).move_to_element(ele).perform()
	ele.click()



def processNike(product_url,sizes_preferred,emailAddress,password):
	browser = init_browser(product_url)
	success = login(browser,emailAddress,password)
	while success==False:
		browser.quit()
		browser = init_browser(product_url)
		success = login(browser,emailAddress,password)
	verify_conuntry(browser,product_url)
	add_to_cart_dropdown(browser,sizes_preferred)
	pay_cart_direct_dropdown(browser)
	print(emailAddress+" :finish buy okkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")




#%%
if __name__=='__main__':
	print ('Parent process %s.' % os.getpid())
	user_dict = {"9437852@gmail.com":"Zxf77158950625@@","1120166237@qq.com":"Xunuozhou757","1070015556@qq.com":"Ding87yuanyu09","876838896@qq.com":"Yjq#13647285977","826849299@qq.com":"Yy5253294"}
	product_url = "https://www.nike.com/cn/t/air-jordan-11-retro-low-gg-%E5%A4%8D%E5%88%BB%E5%A4%A7%E7%AB%A5%E8%BF%90%E5%8A%A8%E7%AB%A5%E9%9E%8B-0ZqXwv"
	sizes_preferred = ["42","42.5","43","44","44.5","40","40.5","41"]
	sizes_preferred_girl = ["38","37.5","36.5","38.5","36","39","40","42","41","40.5"]
	for emailAddress,password in user_dict.items():
		time.sleep(2)
		Process(target=processNike, args=(product_url,sizes_preferred,emailAddress,password)).start()
