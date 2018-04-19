#%%
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import _thread
import random
from lxml import etree

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
	size_dict = {}
	browser.get(product_url)
	try:
		size_dict = get_sizes_available(browser)
	except:
		pass
	while len(size_dict.keys())==0:
		try:
			size_dict = get_sizes_available(browser)
			time.sleep(0.01)
		except:
			pass
	print("size:",size_dict)
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

def pay_cart(browser):
    cart_url = "https://secure-store.nike.com/cn/checkout/html/payment.jsp"
    browser.get(cart_url)
    buy_button = browser.find_element_by_class_name("ch4_reviewBtnTopRt")
    buy_button.click()


def processNike(product_url,sizes_preferred,emailAddress,password):
	browser = init_browser()
	add_to_cart(browser,product_url,sizes_preferred)
	pay_cart(browser)
	print("finish")

#%%

product_url = "https://store.nike.com/cn/zh_cn/pd/vapor-12-elite-se-fg-%E5%A4%A9%E7%84%B6%E7%A1%AC%E8%B4%A8%E8%8D%89%E5%9C%B0%E8%B6%B3%E7%90%83%E9%9E%8B/pid-12306317/pgid-12517467/?cp=cn_brs_041618_a_GEN_SC_GNC_nwc_BY_GC_NFL&__gourl__=1oZt"
sizes_preferred = ["42","42.5","43","41"]
user_dict = {"1120166237@qq.com":"Xunuozhou757","1070015556@qq.com":"Ding87yuanyu09","876838896@qq.com":"Yjq#13647285977","826849299@qq.com":"Yy5253294"}
for emailAddress,password in user_dict.items():
	_thread.start_new_thread( processNike, (product_url,sizes_preferred,emailAddress,password, ) )


#%%
browser = init_browser()

#%%
nike_url = "https://www.nike.com/cn/zh_cn/"
browser.get(nike_url)

#%%
add_to_cart(browser,product_url,sizes_preferred)

#%%

buy_url = "https://secure-store.nike.com/cn/checkout/html/cart.jsp?_DARGS=/ap/checkout/common/includes/beginCheckout.jsp.cartForm"
browser.get(buy_url)

#%%
