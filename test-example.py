from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()
driver.maximize_window()
driver.get("http://store.nike.com/us/en_us/pw/mens-tops-t-shirts/7puZobp?ipp=120")

wait = WebDriverWait(driver, 10)

driver.find_element_by_xpath(
    "//div[@id='exp-gridwall-wrapper']/div[2]/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/p").click()

# opening size dropdown
size_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".exp-pdp-size-and-quantity-container a.exp-pdp-size-dropdown")))
actions = ActionChains(driver)
actions.move_to_element(size_button).click().perform()

# selecting size
size = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[contains(@class, 'nsg-form--drop-down--option') and normalize-space(.) = 'S']")))
actions = ActionChains(driver)
actions.move_to_element(size).click().perform()

# adding to cart
driver.find_element_by_id("buyingtools-add-to-cart-button").click()

# checkout
checkout_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".checkout-button")))
actions = ActionChains(driver)
actions.move_to_element(checkout_button).click().perform()