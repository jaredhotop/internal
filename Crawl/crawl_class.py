from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_driver = os.path.expanduser('~/documents')+"\\chromedriver.exe"
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path = chrome_driver)

class Crawl:
	def __init__(self, url):
		self.url = url
		driver.get(self.url)
		self.page_data = driver.page_source
		
	def _get_page_data(self):
		return str(self.page_data.encode('utf-8'))
		
	def find_i_c(self,id_1): 
		soup = BeautifulSoup(driver.page_source,"html.parser")
		print(soup.find(id="saleTopPrice").parent)
		#return str(driver.find_elements_by_class_name(value_1).find_element_by_id("plantTopPrice").get_attribute('innerHTML')).strip().replace("$","")
	
	def _kill(self):
		driver.close()
		
		