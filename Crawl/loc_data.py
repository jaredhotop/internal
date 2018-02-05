import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import entry_class
import time

def menards(obj,store):
    driver = obj.get_driver()
    driver.get("https://www.menards.com/main/storeDetails.html?store=%s&setMyStore=true/" %store)
    driver.find_element_by_link_text("Make My Store").click()
    driver.get_screenshot_as_file(os.path.expanduser("~/Documents/%s.png" %obj.sku))
    return driver

def tsc(obj,store):
    driver = obj.get_driver()
    driver.get("https://www.tractorsupply.com/tsc/store-locator?zipCode=%s" %store)
    driver.find_element_by_css_selector("span.makemystore_link_sl_sr.underlinehover").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dijitDialogPaneContent[data-dojo-attach-point=containerNode] button#str_mms_yes")))
    driver.find_element_by_css_selector("div.dijitDialogPaneContent[data-dojo-attach-point=containerNode] button#str_mms_yes").click()
    time.sleep(5)
    driver.get_screenshot_as_file(os.path.expanduser("~/Documents/%s.png" %obj.sku))
    return driver
