from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time
import shutil



def create_driver():
    chrome_options = Options()
#   chrome_options.add_argument("--headless")
#   chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-data-dir=/home/test/.config/google-chrome")
#   chrome_driver = "/home\\lubuntu\\bin\\chromedriver.exe"
    driver_path = os.path.expanduser('~/bin/chromedriver')
    driver = webdriver.Chrome(driver_path,chrome_options = chrome_options)
    return driver



def set_cookies():
#    _version()
    _belleville()
    _cape()
    _farmington()
    _festus()
    _high_ridge()
    _jacksonville()
    _springfield()




#set location cookies functions

def _version():
    driver = create_driver()
    driver.get("chrome://version")
    time.sleep(30)
    driver.quit()
    return

def _belleville():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _home_depot(driver,"62226")
            _lowes(driver,"62221")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/belleville/Cookies"))


def _cape():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _tsc(driver,"63701")
            _lowes(driver,"63701")
            _menards(driver,"3286")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/cape/Cookies"))


def _farmington():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _tsc(driver,"63640")
#            _lowes(driver,"63640")
            _menards(driver,"3334")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/farmington/Cookies"))


def _festus():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _home_depot(driver,"63028")
            _lowes(driver,"63028")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/festus/Cookies"))


def _high_ridge():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _tsc(driver,"63049")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/high_ridge/Cookies"))


def _jacksonville():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _home_depot(driver,"62650")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/jacksonville/Cookies"))


def _springfield():
    try:
        os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
    except:
        pass
    driver = create_driver()
    counter = 0
    while(True):
        counter += 1
        try:
            _lowes(driver,"62704")
            _menards(driver,"3293")
        except:
            if counter == 5:
                driver.quit()
                raise
            else:
                continue
        break
    driver.quit()
    shutil.move(os.path.expanduser('~/.config/google-chrome/Default/Cookies'),os.path.expanduser("~/springfield/Cookies"))


#set store location functions


def _home_depot(driver,zip):
    driver.get("https://www.homedepot.com/l/search/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "storeSearchBox")))
    driver.find_element_by_id("storeSearchBox").send_keys(zip,Keys.ENTER)
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.bttn-outline[data-storeid]")))
    driver.find_element_by_css_selector("a.bttn-outline[data-storeid]").click()
    time.sleep(1)
    return driver

def _tsc(driver,zip):
    driver.get("https://tractorsupply.com")
    driver.find_element_by_id("stores_txt").click()
    driver.find_element_by_id("zipcode_input").send_keys(zip,Keys.ENTER)
    driver.find_element_by_class_name("makemystore_link_sl_sr").click()
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "fsrDeclineButton")))
        driver.find_element_by_class_name("fsrDeclineButton").click()
    except:
        pass
    time.sleep(5)
    alert = driver.switch_to.active_element
    alert.click()
    return driver

def _lowes(driver,zip):
    driver.get("https://www.lowes.com/")
    try:
        driver.find_elements_by_class_name("close")[1].click()
    except:
        pass
    driver.find_element_by_class_name("store-name").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search-box")))
    driver.find_element_by_id("search-box").send_keys(zip,Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-store-locator-select-store")))
    driver.find_element_by_class_name("js-store-locator-select-store").click()
    return driver

def _menards(driver,store_id):
    driver.get("https://www.menards.com/main/storeDetails.html?store="+store_id+"&setMyStore=true/")
    driver.find_element_by_link_text("Make My Store").click()
    return driver

#test_code

#set_cookies()
