# Competitor pricing crawler v1.0
# written by: Jayson Scruggs
# Property of Buchheit

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import aux_func
import loc_data
import csv
import shutil
import os
import stores
import time
#from io import StringIO   #what is this line for?
import sys
sys.path.append( os.path.expanduser("~/Documents"))
try:
	from crawlconfig import *
except:
	test_mach = 0
	email_crash_report = 1


class Entry:

	# machine_ip = aux_func.get_ip().split(".")


	def __init__(self, comp_id, link_id, sku, manual, shop_promo, match_id, url,ip):
		future_date = datetime(3000, 12, 31, 1, 0, 0)
		now = datetime.now()
		self.unique_id = now.strftime("%Y%m%d")+comp_id+sku
		self.comp_id = int(comp_id)
		self.comp_match = 0
		self.comp_price = None
		self.comp_sale_price = None
		self.comp_shop_leader = False
		self.comp_shop_notes = None
		self.create_date = now.strftime("%Y-%m-%d %H:%M:%S")
		self.created_by_tm = 8
		self.last_update_date = self.create_date
		self.link_id = link_id
		self.sku = sku
		self.shop_date = self.create_date
		self.updated_by_tm = 8
		self.reviewed = 0
		self.reviewed_by = 4
		self.reviewed_date = future_date.strftime("%Y-%m-%d %H:%M:%S")
		self.comp_shop_manual = manual
		self.comp_shop_promo = shop_promo
		self.comp_match_id = match_id
		self.comp_shop_out_of_stock = False
		self.comp_shop_third_party = False
		self.url = url
		self._driver = None
		self._broken_flag = False
		self._log_msg = ''
		self.pagedata = None
		self._defined = True
		self.ip = ip

	def __repr__(self):
		return "Entry('{}','{}','{}','{}','{}','{}','{}','{}')".format(self.comp_id, self.link_id,\
		self.sku, self.comp_shop_manual, self.comp_shop_promo, self.comp_match_id, self.url, self.ip)

	def __str__(self):
		return "**********\nSku: {}\nPrice: {}\nSale Price: {}\nThird Party: {}\nOut of Stock: {}\nComp_id: {}\nUrl: {}\n**********".format(\
		self.sku, self.comp_price, self.comp_sale_price, self.comp_shop_third_party, self.comp_shop_out_of_stock,self.comp_id, self.url)

	def write_entry(self, file):
		if (self.comp_price != None and self.comp_sale_price != None and self.comp_price != False and self.comp_price != '0.0'):
			self.log("Writing entry to file: " + file,True)
			with open(file, "a") as f:
				out = csv.writer(f, delimiter = ",")
				out.writerow(self._data_tup())
		elif self._broken_flag:
			self.log("Link flagged as broken, %s" %self.url,False,os.path.expanduser('~/Documents/unwritten_%s.csv' %self.ip))
		elif not self._defined:
			self.log("Competitor Undefined, %s" %self.url,False,os.path.expanduser('~/Documents/unwritten_%s.csv' %self.ip))
		else:
			self.log("Entry not valid. Writing to alternate file.")
			self.log("Closer inspection needed, %s" %self.url,False,os.path.expanduser('~/Documents/unwritten_%s.csv' %self.ip))
		return


	def _data_tup(self):
		return (self.unique_id, self.comp_id, self.comp_match, self.comp_price,  \
		self.comp_sale_price, self.comp_shop_leader, self.comp_shop_notes,  \
		self.create_date, self.created_by_tm, self.last_update_date, self.link_id, \
		self.sku, self.shop_date, self.updated_by_tm, self.reviewed, self.reviewed_by, \
		self.reviewed_date, self.comp_shop_manual, self.comp_shop_promo, \
		self.comp_match_id,self.comp_shop_out_of_stock, self.comp_shop_third_party,self.ip)

	def set_price(self,price):
		if isinstance(price, (int, long, float)):
			self.comp_price = price
			self.log("Set competitor price to: " + str(price))
		else:
			self.log("Attempted to set competitor price as: %s but it is not a number" %price,True)
		return

	def set_sale_price(self,price):
		if isinstance(price, (int, long, float)):
			self.comp_sale_price = price
			if price != 0.00:
				self.log("Set competitor sale price to: " + str(price))
		else:
			self.log("Attempted to set competitor sale price to: %s but it is not a number" %price,True)
		return

	def set_shop_date(self):
		now = datetime.now()
		self.shop_date = now.strftime("%Y-%m-%d %H:%M:%S")
		return

	def set_third_party(self, bool_val = True):
		self.comp_shop_third_party = bool_val
		self.comp_match_id = 2
		self.log("Set third party to " + str(bool_val),True)
		return

	def set_out_of_stock(self):
		self.comp_shop_out_of_stock = True
		self.log("Set item as \"out of stock\"",True)
		return

	def set_unique_id(self):
		self.unique_id = self.unique_id + '1'
		self.log("Corrected unique_id duplicate")
		return

	def set_undefined(self):
		self._defined = False
		return

	def _get_broken(self):
		return True if self._broken_flag else False

	def _get_price(self):
		return self.comp_price

	def _create_driver(self):
		firefox_options = Options()
		firefox_options.add_argument("--headless")
		# chrome_options.add_argument("--disable-gpu")
		# firefox_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")
		self._driver = webdriver.Firefox(executable_path = os.path.expanduser('~/bin/geckodriver'),firefox_options = firefox_options)
		self.log("Driver created",True)
		return self._driver

	def kill_driver(self):
		if self._driver:
			self._driver.quit()
			self.log("Driver destroyed",True)
		else:
			self.log("Error driver doesn't exist")
		return

	def log(self,log_msg,print_only = False,file= os.path.expanduser("/media/WebCrawl/logs/machine{}.log")):
		file = file.format(self.ip)
		self._log_msg = self._log_msg + " \n" + log_msg
		now = datetime.now()
		if not print_only and not test_mach:
			with open(file,"a") as f:
				f.write("Timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S") + ", comp_id: " +  str(self.comp_id) + ", sku: " + self.sku + ", Log Message: " + log_msg + "\n")
		print("sku: " + self.sku + " , Log Message: " + log_msg)
		return

	def _retrieve_data(self,selector,value = None):
		try:
			temp = self._driver.find_element_by_css_selector(selector).get_attribute(value) if value else self._driver.find_element_by_css_selector(selector)
		except:
			return ""
		else:
			return temp.encode('utf-8')

	def _find_data(self,select,value = 'innerHTML'):
		param = value.split('|||')
		if  len(param) >= 2:
			value = param[0]
			check_value = param[1]
		else:
			check_value = None
		try:
			if check_value:
				if check_value in self._driver.find_element_by_css_selector(select).get_attribute(value):
					return True
				else:
					return False
			else:
				try:
					self._driver.find_element_by_css_selector(select).get_attribute(value)
					return True
				except:
			 		return False
		except NoSuchElementException:
			pass
		except:
			self.log("Error in _find_data")

	def pricing(self,price_dict,sale_dict = None,broken_dict = None,loc_ins = None):
		try:
			driver = self._create_driver()
 		except:
			self._driver = None
 			self.log("Driver failed to start")
 		else:
 			try:
				if loc_ins:
					for x in range(5):
						try:
							exec(loc_ins)
						except:
							continue
						else:
							break
 				driver.get(str(self.url))
				if self.comp_id == 12:
					time.sleep(5)
				self.pagedata = driver.page_source.encode('utf-8')
				# with open(os.path.expanduser("~/Documents/pagedata.txt"),'w') as f:
				# 	f.write(self.pagedata)
 			except:
 				self.log("Failed to retrieve url")
 			else:
				#Find Price
 				self.set_shop_date()
 				try:
 					for key,value in price_dict.iteritems():
 						try:
							price = aux_func.clean(self._retrieve_data(key,value))
							if price:
 								self.set_price(price)
								break
 						except:
 							continue
					else:
						self.log("No valid price found")
 				except:
 					self.log("Failed to retrieve competitor price")
 				#Find Sale Price
 				else:
					if sale_dict:
						try:
							for key,value in sale_dict.iteritems():
								try:
									self.set_sale_price(aux_func.clean(self._retrieve_data(key,value))) if aux_func.clean(self._retrieve_data(key,value)) != self.comp_price else self.set_sale_price(0.00)
									break
								except:
									continue
							else:
								if self.comp_price != None:
									self.log("No sale price found with current selectors")
								self.set_sale_price(0.00)
						except:
							self.log("Failed to acquire sales price")
							self.set_sale_price(0.00)
					else:
						self.set_sale_price(0.00)
				try:
					for key,value in broken_dict.iteritems():
						if value:
							if self._find_data(key,value):
								self._broken_flag = True
								self.log("link flagged as broken")
						else:
							if self._find_data(key):
								self._broken_flag = True
								self.log("link flagged as broken")
				except:
					self.log("Error checking broken link in the pricing function")
		return


	def crawl(self):
		switch = {
			1  : stores.academy,
			2  : stores.basspro,
			3  : stores.blain,
			4  : stores.farm_and_home,
			5  : stores.home_depot,
			6  : stores.lowes,
			7  : stores.menards,
			8  : stores.tsc,
			9  : stores.walmart,
			10 : stores.cabela,
			11 : stores.orscheln,
			12 : stores.ruralking,
			13 : stores.sears,
			14 : stores.valleyvet,
			15 : stores.lowes,
			16 : stores.lowes,
			17 : stores.home_depot,
			23 : stores.home_depot,
			24 : stores.lowes,
			25 : stores.farm_and_home,
			26 : stores.menards,
			27 : stores.menards,
			36 : stores.dickeybub,
			37 : stores.acehardware,
			43 : stores.bootbarn,
			44 : stores.shelper,
			73 : stores.tsc,
			74 : stores.tsc,
			124: stores.tsc
		}
		switch.get(self.comp_id,stores._default)(self)
		return

#Competitor specific methods
