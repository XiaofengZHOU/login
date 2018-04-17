#%%
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import _thread
import random

UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
       "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
       )
ua = UAS[random.randrange(len(UAS))]

def init_browser():
	firefox_capabilities = DesiredCapabilities.FIREFOX
	firefox_capabilities['marionette'] = True
	firefox_capabilities['handleAlerts'] = True
	firefox_capabilities['acceptSslCerts'] = True
	firefox_capabilities['acceptInsecureCerts'] = True
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", ua)
	geckoPath = 'geckodriver-017.exe'
	browser = webdriver.Firefox(firefox_profile=profile,capabilities=firefox_capabilities, executable_path=geckoPath)
	return browser

def show_login_form(browser):
	nike_url = "https://www.nike.com/cn/zh_cn/"
	browser.get(nike_url)
	time.sleep(random.uniform(1, 10))
	page_flag = False

	while page_flag == False:
		try:
			join_button = browser.find_element_by_css_selector('li.exp-join-login button')
			join_button.click()
			page_flag = True
		except:
			time.sleep(0.5)
			pass


def login(browser,emailAddress,password):
	time.sleep(random.uniform(1, 3))
	email = browser.find_element_by_xpath("//input[@name='emailAddress']")
	try:
		email.clear()
	except:
		pass
	for letter in emailAddress:
		time.sleep(random.uniform(0.5, 2))
		email.send_keys(letter)
	time.sleep(random.uniform(1, 3))
	pw = browser.find_element_by_xpath("//input[@name='password']")
	try:
		pw.clear()
	except:
		pass
	for letter in password:
		time.sleep(random.uniform(0.5, 2))
		pw.send_keys(letter)
	time.sleep(random.uniform(1, 3))
	login_button = browser.find_element_by_xpath("//input[@value='登录']")
	login_button.click()
	time.sleep(random.uniform(1, 3))

def get_sizes_available(browser) :
	page_source = browser.page_source
	soup = BeautifulSoup(page_source, "html.parser")
	size_tags = soup.find("div", {"name":"skuAndSize"}).find_all("input", {"name":"skuAndSize"})
	size_dict = {}
	for size_tag in size_tags :
		if size_tag.has_attr('disabled'):
			continue
		else:
			size_dict[size_tag.attrs['aria-label']] = size_tag.attrs['id']
	return size_dict


def add_to_cart(browser,product_url,sizes_preferred):
	browser.get(product_url)
	size_dict = get_sizes_available(browser)
	while len(size_dict.keys())==0:
		size_dict = get_sizes_available(browser)
		time.sleep(0.01)
	print(size_dict)
	sizes = size_dict.keys()
	for size in sizes_preferred:
		if size in sizes:
			print('has size: ',size)
			size_id = size_dict[size]
			print(size,':',size_id)
			input_size = browser.find_element_by_xpath("//label[@for='"+ size_id + "']")
			input_size.click()
			buy_button = browser.find_element_by_class_name("addToCartBtn")
			buy_button.click()
			break


def processNike(product_url,sizes_preferred,emailAddress,password):
	browser = init_browser()
	show_login_form(browser)
	login(browser,emailAddress,password)
	add_to_cart(browser,product_url,sizes_preferred)
	print("finish")


#%%
product_url = "https://www.nike.com/cn/t/lebron-15-ep-%E7%94%B7%E5%AD%90%E8%BF%90%E5%8A%A8%E9%9E%8B-0nTgJ11M/897649-300"
sizes_preferred = ["42","42.5","43","44","44.5","40","40.5","41","44","44","44","44"]
#,"1070015556@qq.com":"Ding87yuanyu09"

user_dict = {"9437852@gmail.com":"Zxf77158950625@@","1070015556@qq.com":"Ding87yuanyu09","876838896@qq.com":"Yjq#13647285977"}
for emailAddress,password in user_dict.items():
	_thread.start_new_thread( processNike, (product_url,sizes_preferred,emailAddress,password, ) )



#%%
product_url = "https://www.nike.com/cn/t/lebron-15-ep-%E7%94%B7%E5%AD%90%E8%BF%90%E5%8A%A8%E9%9E%8B-0nTgJ11M/897649-300"
sizes_preferred = ["42","42.5","43","41"]
emailAddress = "1070015556@qq.com"
password = "Ding87yuanyu09"
processNike(product_url,sizes_preferred,emailAddress,password)





#%%
