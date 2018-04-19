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
import random
from multiprocessing import Process
from multiprocessing import Pool
import os
import re


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
	geckoPath = 'geckodriver.exe'
	browser = webdriver.Firefox(firefox_profile=profile,capabilities=firefox_capabilities, executable_path=geckoPath)
	time.sleep(2)
	try:
		browser.get(product_url)
	except:
		time.sleep(5)
		browser.get(product_url)
	return browser



def login(browser,name,password):
	wait = WebDriverWait(browser, 10)
	try:
		ele = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@aria-label='加入或登录']")))
		webdriver.ActionChains(browser).move_to_element(ele).perform()
		time.sleep(random.uniform(0.5, 2))
		ele.click()
	except:
		print ("move to login failed")
		print (traceback.print_exc())
		return False
	time.sleep(random.uniform(1, 2))

	try:
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
		ele = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='登录']")))
		webdriver.ActionChains(browser).move_to_element(ele).perform()
		time.sleep(random.uniform(0.5, 2))
		ele.click()
	except:
		print ('login submit failed')
		print (traceback.print_exc())
		return False
	time.sleep(random.uniform(8, 10))

	try:
		ele = browser.find_element_by_class_name("nike-unite-error-panel")
		ele = browser.find_element_by_class_name("modal-container")
		print(name+ " :login unsuccessful")
		return False
	except:
		print(name+" :login ok")
		print (traceback.print_exc())
		return True

def get_sizes_available_dropdown(browser) :
	wait = WebDriverWait(browser, 10)
	size_list = []
	while True:
		try:
			ele = browser.find_element_by_xpath("//div[@data-juno-name='sizeSelector']")
			ele.click()
			break
		except:
			time.sleep(0.001)
			continue

	grid = wait.until(EC.visibility_of_element_located((By.XPATH,"//ul[@data-juno-name='sizeGrid']")))
	eles = browser.find_elements_by_xpath("//ul[@data-juno-name='sizeGrid']/li")
	for ele in eles:
		if  "disabled" in ele.get_attribute("class"):
			continue
		size_list.append(ele.text)
	return size_list


def add_to_cart_dropdown(browser,sizes_preferred):
	size_list = get_sizes_available_dropdown(browser)
	print("size available: ",size_list)

	flag = False
	for size in sizes_preferred:
		for size_avai in size_list:
			if size in size_avai:
				flag = True
				break
		if flag :
			print('has size: ',size)
			input_size = browser.find_element_by_xpath("//li[@data-size='"+ size_avai + "']")
			input_size.click()

			cart_button = browser.find_element_by_class_name("js-buy")
			cart_button.click()
			break


def pay(browser):
	wait = WebDriverWait(browser, 20)
	wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='modal-container']")))
	wait.until(EC.visibility_of_element_located((By.ID,"0"))).click()
	browser.find_elements_by_xpath("//div[@data-juno-name='saveButton']/a")[2].click()
	wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"提交订单"))).click()
	wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"为您的订单付款"))).click()


def processNike(product_url,sizes_preferred,emailAddress,password):
	browser = init_browser(product_url)
	success = login(browser,emailAddress,password)
	count=1
	while success == False:
		if count%5==0:
			browser.quit()
			browser = init_browser(product_url)
			success = login(browser,emailAddress,password)
		else:
			browser.get(product_url)
			success = login(browser,emailAddress,password)
		count=count+1

	add_to_cart_dropdown(browser,sizes_preferred)
	pay(browser)


#%%
product_url = "https://www.nike.com/cn/launch/t/air-max-zero-bg-wang-junkai"
emailAddress = "9437852@gmail.com"
password = "Zxf77158950625@@"
browser = init_browser(product_url)
success = login(browser,emailAddress,password)
count=1
while success == False:
	if count%5==0:
		browser.quit()
		browser = init_browser(product_url)
		success = login(browser,emailAddress,password)
	else:
		browser.get(product_url)
		success = login(browser,emailAddress,password)
	count=count+1
add_to_cart_dropdown(browser,sizes_preferred)
pay(browser)
