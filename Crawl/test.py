import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import entry_class



obj = entry_class.Entry('5','1234','4665',False,False,'1',\
'https://www.homedepot.com/p/Unbranded-50-lbs-Rock-Salt-Bag-4664/202523041','90')
obj.crawl()
# obj = entry_class.Entry('5','1234','4665',False,False,'1',\
# 'https://www.homedepot.com/p/Safe-Step-40-lb-5300-Max-Blend-Ice-Melter-57840/202564240','90')
# obj.crawl()
print(obj)
# url = 'https://www.orschelnfarmhome.com/view/product/si-waterproof-steel-toe-knee-work-boots-14-in/si5855988'
# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# # chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("user-data-dir=/home/jayson/.config/google-chrome")
# driver = webdriver.Chrome(os.path.expanduser('~/bin/chromedriver'),chrome_options = chrome_options)
# driver.get(url)
# print(driver.find_element_by_css_selector("span.product_unit_price").get_attribute('innerHTML'))
# diver.quit()



# price_selectors = [""]
# sale_selectors = [""]
# try:
#     self.pricing(price_selectors,'innerHTML')
# except:
#     self._log("Failed to acquire pricing data")
# finally:
#     self._kill_driver()
# return
