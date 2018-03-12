# Competitor pricing crawler v1.0
# written by: Jayson Scruggs
# Property of Buchheit

from datetime import datetime
from selenium import webdriver
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
#from io import StringIO   #what is this line for?
import sys
sys.path.append( os.path.expanduser("~/Documents"))
try:
	from crawlconfig import *
except:
	test_mach = 0
	email_crash_report = 1
import time


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
			self._log("Writing entry to file: " + file,True)
			with open(file, "a") as f:
				out = csv.writer(f, delimiter = ",")
				out.writerow(self._data_tup())
		elif self._broken_flag:
			self._log("Link flagged as broken, %s" %self.url,False,os.path.expanduser('~/Documents/unwritten%s.csv' %self.ip))
		elif not self._defined:
			self._log("Competitor Undefined, %s" %self.url,False,os.path.expanduser('~/Documents/unwritten%s.csv' %self.ip))
		else:
			self._log("Entry not valid. Writing to alternate file.")
			self._log("Closer inspection needed, %s" %self.url,False,os.path.expanduser('~/Documents/unwritten%s.csv' %self.ip))
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
			self._log("Set competitor price to: " + str(price))
		else:
			self._log("Attempted to set competitor price as: %s but it is not a number" %price,True)
		return

	def set_sale_price(self,price):
		if isinstance(price, (int, long, float)):
			self.comp_sale_price = price
			if price != 0.00:
				self._log("Set competitor sale price to: " + str(price))
		else:
			self._log("Attempted to set competitor sale price to: %s but it is not a number" %price,True)
		return

	def set_shop_date(self):
		now = datetime.now()
		self.shop_date = now.strftime("%Y-%m-%d %H:%M:%S")
		return

	def set_third_party(self, bool_val = True):
		self.comp_shop_third_party = bool_val
		self.comp_match_id = 2
		self._log("Set third party to " + str(bool_val),True)
		return

	def set_out_of_stock(self):
		self.comp_shop_out_of_stock = True
		self._log("Set item as \"out of stock\"",True)
		return

	def set_unique_id(self):
		self.unique_id = self.unique_id + '1'
		self._log("Corrected unique_id duplicate")
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
		firefox_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")
		self.driver = webdriver.Firefox(executable_path = os.path.expanduser('~/bin/geckodriver'),firefox_options = firefox_options)
		self._log("Driver created",True)
		return self.driver

	def _kill_driver(self):
		if self.driver:
			self.driver.quit()
			self._log("Driver destroyed",True)
		else:
			self._log("Error driver doesn't exist")
		return

	def _log(self,log_msg,print_only = False,file= os.path.expanduser("/media/WebCrawl/logs/machine{}.log")):
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
			temp = self.driver.find_element_by_css_selector(selector).get_attribute(value) if value else self.driver.find_element_by_css_selector(selector)
		except:
			return False
		else:
			return temp.encode('utf-8')

	def _find_data(self,select,value = 'innerHTML'):
		try:
			self.driver.find_element_by_css_selector(select).get_attribute(value)
			return True
		except:
			 return False

	def pricing(self,price_dict,sale_dict = None,broken_dict = None,loc_ins = None):
		try:
			driver = self._create_driver()
 		except:
			self.driver = None
 			self._log("Driver failed to start")
			raise
 		else:
 			try:
				if loc_ins:
					for x in range(5):
						try:
							exec(loc_ins)
						except:
							raise
							continue
						else:
							break
 				driver.get(str(self.url))
				self.pagedata = driver.page_source.encode('utf-8')
				# with open(os.path.expanduser("~/Documents/pagedata.txt"),'w') as f:
				# 	f.write(self.pagedata)
 			except:
				raise
 				self._log("Failed to retrieve url")
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
 				except:
 					self._log("Failed to retrieve competitor price")
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
									self._log("No sale price found with current selectors")
								self.set_sale_price(0.00)
						except:
							self._log("Failed to acquire sales price")
							self.set_sale_price(0.00)
					else:
						self.set_sale_price(0.00)
				try:
					for key,value in broken_dict.iteritems():
						if self._find_data(key,value):
							self._broken_flag = True
				except:
					pass
		return


	def crawl(self):
		switch = {
			1  : stores._academy,
			2  : stores._basspro,
			3  : stores._blain,
			4  : stores._farm_and_home,
			5  : stores._home_depot,
			6  : stores._lowes,
			7  : stores._menards,
			8  : stores._tsc,
			9  : stores._walmart,
			10 : stores._cabela,
			11 : stores._orscheln,
			12 : stores._ruralking,
			13 : stores._sears,
			14 : stores._valleyvet,
			15 : stores._lowes,
			16 : stores._lowes,
			17 : stores._home_depot,
			23 : stores._home_depot,
			24 : stores._lowes,
			25 : stores._farm_and_home,
			26 : stores._menards,
			27 : stores._menards,
			36 : stores._dickeybub,
			37 : stores._acehardware,
			43 : stores._bootbarn,
			44 : stores._shelper,
			73 : stores._tsc,
			74 : stores._tsc,
			124: stores._tsc
		}
		switch.get(self.comp_id,stores._default)(self)
		return

#Competitor specific methods
