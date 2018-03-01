import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

def lowes(obj,store):
    driver = obj.get_driver()
    driver.get("https://www.lowes.com/")
    try:
        driver.find_elements_by_class_name("close")[1].click()
    except:
        pass
    driver.find_element_by_class_name("store-name").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search-box")))
    driver.find_element_by_id("search-box").send_keys(store,Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-store-locator-select-store")))
    driver.find_element_by_class_name("js-store-locator-select-store").click()
    driver.get_screenshot_as_file(os.path.expanduser("~/Documents/%s.png"%obj.sku))
    return driver

def home_depot(obj,store):
    driver = obj.get_driver()
    driver.get("https://www.homedepot.com/l/search/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "storeSearchBox")))
    driver.find_element_by_id("storeSearchBox").send_keys(store,Keys.ENTER)
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.bttn-outline[data-storeid]")))
    driver.find_element_by_css_selector("a.bttn-outline[data-storeid]").click()
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.sfmystoreicon")))
    return driver

def basspro(obj):
    driver = obj.get_driver()
    driver.get(obj._get_url())
    driver.get_screenshot_as_file(os.path.expanduser("~/Documents/%s.png" %obj.sku))
    bpsku = obj._retrieve_data("meta[name=pageId]","content")
    if not bpsku:
        obj._log("Failed to extract BassPro Sku")
        return
    else:
        return int(bpsku)
