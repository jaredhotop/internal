# Competitor pricing crawler v1.0
# written by: Jayson Scruggs
# Property of Buchheit

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import aux_func
import loc_data
import csv
import shutil
#from io import StringIO   #what is this line for?
import sys
import os
import time


class Entry:

	machine_ip = aux_func.get_ip().split(".")
	

	def __init__(self, comp_id, link_id, sku, manual, shop_promo, match_id, url):
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
		self.broken_flag = False
		self.log_msg = ''
		self.pagedata = None

	def write_entry(self, file):
		if (self.comp_price != None and self.comp_sale_price != None and self.comp_price != False and self.comp_price != '0.0'):
			self._log("Writing entry to file: " + file,True)
			with open(file, "a") as f:
				out = csv.writer(f, delimiter = ",")
				out.writerow(self._data_tup())
		elif self.broken_flag:
			self._log("Entry not valid. Writing to alternate file.")
			self._log("Link flagged as broken, %s" %self.url,False,os.path.expanduser('/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/unwritten.csv'))
		else:
			self._log("Entry not valid. Writing to alternate file.")
			self._log("Closer inspection needed, %s" %self.url,False,os.path.expanduser('/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/unwritten.csv'))

		return

	def _print_readable(self):
		variables = ("unique_id", "comp_id", "comp_match", "comp_price", \
		"comp_sale_price", "comp_shop_leader", "comp_shop_notes", \
		"create_date", "created_by_tm", "last_update_date", "link_id", \
		"sku", "shop_date", "updated_by_tm", "reviewed", "reviewed_by", \
		"reviewed_date", "comp_shop_manual", "comp_shop_promo", \
		"comp_match_id","comp_shop_out_of_stock", "comp_shop_third_party")
		values = self._data_tup()
		for i in range(len(variables)):
			print(variables[i],values[i])
		return

	def _data_tup(self):
		return (self.unique_id, self.comp_id, self.comp_match, self.comp_price,  \
		self.comp_sale_price, self.comp_shop_leader, self.comp_shop_notes,  \
		self.create_date, self.created_by_tm, self.last_update_date, self.link_id, \
		self.sku, self.shop_date, self.updated_by_tm, self.reviewed, self.reviewed_by, \
		self.reviewed_date, self.comp_shop_manual, self.comp_shop_promo, \
		self.comp_match_id,self.comp_shop_out_of_stock, self.comp_shop_third_party)

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

	def _get_url(self):
		return str(self.url)

	def get_unique_id(self):
		return self.unique_id

	def get_driver(self):
		return self.driver

	def get_comp_id(self):
		return self.comp_id

	def _get_broken(self):
		if self.broken_flag:
			print(True)
		else:
			print(False)
		return

	def _get_price(self):
		return self.comp_price

	def _create_driver(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")
		# chrome_options.add_argument("user-data-dir=%s" %os.path.expanduser('~/.config/google-chrome'))
		self.driver = webdriver.Chrome(os.path.expanduser('~/bin/chromedriver'),chrome_options = chrome_options)
		self._log("Driver created",True)
		return self.driver

	def _kill_driver(self):
		if self.driver:
			self.driver.quit()
			self._log("Driver destroyed",True)
		else:
			self._log("Error driver doesn't exist")
		return

	def _log(self,log_msg,print_only = False,file= os.path.expanduser("/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/"+machine_ip[3]+"self_log.log")):
		self.log_msg = self.log_msg + " \n" + log_msg
		now = datetime.now()
		# if not print_only:
		# 	with open(file,"a") as f:
		# 		f.write("Timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S") + ", comp_id: " +  str(self.comp_id) + ", sku: " + self.sku + ", Log Message: " + log_msg + "\n")
		print("sku: " + self.sku + " , Log Message: " + log_msg)
		return

	def _retrieve_data(self,selector,value = None):
		temp = self.driver.find_element_by_css_selector(selector).get_attribute(value) if value else self.driver.find_element_by_css_selector(selector)
		if not temp:
			return False
		else:
			return aux_func.clean(temp.encode('utf-8'))

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
 			self._log("Driver failed to start")
 		else:
 			try:
				if loc_ins:
					eval(loc_ins)
 				driver.get(self._get_url())
				driver.get_screenshot_as_file(os.path.expanduser("~/Documents/%s.png" %self.sku))
				self.pagedata = driver.page_source.encode('utf-8')
				with open(os.path.expanduser("~/Documents/pagedata.txt"),'w') as f:
					f.write(self.pagedata)

 			except:
				raise
 				self._log("Failed to retrieve url")
 			else:
 #Find Price
 				self.set_shop_date()
 				try:
 					for key,value in price_dict.iteritems():
 						try:
							price = self._retrieve_data(key,value)
							if price:
 								self.set_price(price)
								break
							# else:
							# 	self._log("Retrieve_data return false. Check your selector and attribute values")
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
									self.set_sale_price(self._retrieve_data(key,value)) if self._retrieve_data(key,value) != self.comp_price else self.set_sale_price(0.00)
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
							self.broken_flag = True
				except:
					pass
		return


	def crawl(self):
		switch = {
			1 : self._academy,
			2 : self._basspro,
			3 : self._blain,
			4 : self._farm_and_home,
			5 : self._home_depot,
			6 : self._lowes,
			7 : self._menards,
			8 : self._tsc,
			9 : self._walmart,
			10: self._cabela,
			11: self._orscheln,
			12: self._ruralking,
			13: self._sears,
			14: self._valleyvet,
			15: self._lowes,
			16: self._lowes,
			17: self._home_depot,
			23: self._home_depot,
			24: self._lowes,
			25: self._farm_and_home,
			26: self._menards,
			27: self._menards,
			36: self._dickeybub,
			37: self._acehardware,
			43: self._bootbarn,
			44: self._shelper,
			73: self._tsc,
			74: self._tsc
		}
		switch.get(self.comp_id,self._default)()
		return

#Competitor specific methods

	def _academy(self):
		price_selectors = {"input#dlItemPrice":"value",}
		sale_selectors = {"span#currentPrice":"innerHTML",}
		broken_link_selectors = {"p#search_results_total_count":"innerHTML"}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors)
		except:
			self._log("Failed to aquire pricing data")
#No third party
#check out of stock
		try:
			try:
				oos = self.driver.find_element_by_css_selector("button#add2CartBtn").get_attribute("innerHTML")
			except:
				oos = "in stock"
			if "Out of Stock" in oos:
				self.set_out_of_stock()
		except:
			self._log("Out of stock check failed")
		finally:
			self._kill_driver()
		return

	def _acehardware(self):
		price_selectors = {"div.productPrice span script":"innerHTML",}
		try:
			self.pricing(price_selectors)
		except:
			self._log("Failed to aquire pricing data")
#No third party
#No out of stock
		finally:
			self._kill_driver()
		return

	def _basspro(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _blain(self):
		price_selectors = {"meta[itemprop=lowprice]":"content",\
		"div.active-price>div.price>span":"innerHTML",\
		"div.original-price>span.price>span":"innerHTML"}
		sale_selectors = {"div.active-price.promo > div.price > span:not([class])":"innerHTML",}
		broken_link_selectors = {"div.list-header-text > span":"innerHTML"}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors)
		except:
			self._log("Failed to acquire pricing data")
#No third party
		try:
			if not self._find_data("span.stock-msg.in-stock"):
				self.set_out_of_stock()
		except:
			self._log("Out of stock check failed")
		finally:
			self._kill_driver()
		return

	def _bootbarn(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _cabela(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _dickeybub(self):
		price_selectors = {"p.price > del > span.woocommerce-Price-amount.amount" : "innerHTML",\
		"p.price > span.woocommerce-Price-amount.amount" : "innerHTML",}
		sale_selectors = {"p.price > ins > span.woocommerce-Price-amount.amount" : "innerHTML",}
		try:
			self.pricing(price_selectors,sale_selectors,)
		except:
			self._log("Failed to acquire pricing data")
		finally:
			self._kill_driver()
		return

	def _home_depot(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _farm_and_home(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _lowes(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _menards(self):
		if self.get_comp_id() == 7:
			loc_ins = "loc_data.menards(self,'3286')"
		elif self.get_comp_id() == 26:
			loc_ins = "loc_data.menards(self,'3334')"
		elif self.get_comp_id() == 27:
			loc_ins = "loc_data.menards(self,'3293')"

		price_selectors = {"span.bargainStrike" : "innerHTML",\
		"span.EDLP.fontSize16.fontBold.alignRight" : "innerHTML",\
		"span#totalItemPriceFloater" : "innerHTML"}
		sale_selectors = {"span.bargainPrice" : "innerHTML", \
		"span#totalItemPriceFloater" : "innerHTML"}
		broken_link_selectors = {"h3.resettitle":"innerHTML"}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
		except:
			self._log("Failed to acquire pricing data")
		finally:
			self._kill_driver()
			# os.remove(os.path.expanduser('~/.config/google-chrome/Default/Cookies'))
		return

	def _orscheln(self):
		price_selectors = {"span.product_unit_price" : "innerHTML",}
		sale_selectors = {"":""}
		broken_link_selectors = {"":""}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors)
		except:
			self._log("Failed to acquire pricing data")
#No third party
#No out of stock
		finally:
			self._kill_driver()
		return

	def _ruralking(self):
		# try:
		# 	driver = self._create_driver()
		# except:
		# 	self._log("Driver failed to start")
		# else:
		# 	try:
		# 		driver.get(self._get_url())
		# 		self.pagedata = driver.page_source.encode('utf-8')
		# 	except:
		# 		self._log("Failed to retrieve url")
		# 	else:
		# 		self.set_shop_date()
		# 		try:
		# 			self.set_price(clean(driver.find_element_by_css_selector("div.price-box > span.regular-price > span.price").get_attribute("text")))
		# 		except:
		# 			self._log("Failed to retrieve competitor price using any known css selector")
		# 		else:
		# 			try:
		# 				self.set_sale_price(clean(driver.find_element_by_css_selector("div.Price-old.display-inline-block.arrange-fill.font-normal.u-textNavyBlue.display-inline").find_element_by_css_selector("span.Price-group").get_attribute("title"))
		# 			except:
		# 				self._log("No sale price found using current css selectors")
		# 				self.set_sale_price("0.00")
		# 			try:
		# 				check = EC.presence_of_element_located((By.CSS_SELECTOR, "a.font-bold.prod-SoldShipByMsg[href=http://help.walmart.com]"))
		# 				if check != True:
		# 					self.set_third_party()
		# 			except:
		# 				pass
		# 			try:
		# 				#https://www.walmart.com/ip/Holiday-Time-Net-Light-Set-Green-Wire-Blue-Bulbs-150-Count/21288309   //Out of stock link
		# 				if (EC.presence_of_element_located(BY.CSS_SELECTOR,"span.copy-mini.display-block-xs.font-bold.u-textBlack[text=Out of stock]")):
		# 					self.set_out_of_stock()
		# 			except:
		# 				pass
		# 	finally:
		# 		self._kill_driver()
		return

	def _sears(self):
		price_selectors = {"span.price-wrapper":"innerHTML"}
		sale_selectors = {"h4.redSalePrice span.price-wrapper":"innerHTML"}
		broken_link_selectors = {"":""}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors)
		except:
			raise
			self._log("Failed to acquire pricing data")
#No Third Party
#No out of Stock
		finally:
			self._kill_driver()
		return

	def _shelper(self):
		price_selectors = {"div.product-content-inner > div.product-price > span.price-original.price-holder-alt > strong" : "innerHTML",}
		sale_selectors = {"div.product-content-inner > div.product-callout > h6.product-callout-title > strong" : "innerHTML",}
		broken_link_selectors = {"":""}
		try:
			self.pricing(price_selectors,sale_selectors)
		except:
			self._log("Failed to acquire pricing data")
#No third party
#No out of stock
		finally:
			self._kill_driver()
		return

	def _tsc(self):
		#view in cart item
		# https://www.tractorsupply.com/tsc/product/jonsered-502cc-gas-chainsaw-cs2250s?cm_vc=-10005
		if self.get_comp_id() == 73:
			loc_ins = "loc_data.tsc(self,'63049')"
		elif self.get_comp_id() == 74:
			loc_ins = "loc_data.tsc(self,'63701')"
		elif self.get_comp_id() == 8:
			loc_ins = "loc_data.tsc(self,'63640')"
		price_selectors = {"span.was_text":"innerHTML","span.dollar_price":"innerHTML"}
		sale_selectors = {"span.dollar_price":"innerHTML"}
		broken_link_selectors = {"":""}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
		except:
			self._log("Failed to acquire pricing data")
#no third party
#no out of stock
		finally:
			self._kill_driver()
		return

	def _valleyvet(self):
		self._log("Competitor: %d not yet defined" %self.comp_id)
		return

	def _walmart(self):
		price_selectors = {"div.Price-old.display-inline-block.arrange-fill.font-normal.u-textNavyBlue.display-inline > span.Price-group" : "title",\
		"div.prod-BotRow.prod-showBottomBorder.prod-OfferSection.prod-OfferSection-twoPriceDisplay div.Grid-col:nth-child(4) span.Price-group" : "title",\
		"span.display-inline-block.arrange-fit.Price.Price-enhanced.u-textNavyBlue > span.Price-group" : "title",\
		"span.display-inline-block.arrange-fit.Price.Price-enhanced.u-textGray > span.Price-group" : "title",}
		broken_link_selectors = {"div.font-semibold.prod-Bot-partial-head" : "innerHTML",\
		"p.error-ErrorPage-copy":"innerHTML"}
		sale_selectors = {}
		try:
			self.pricing(price_selectors,sale_selectors,broken_link_selectors)
		except:
			self._log("Failed to aquire pricing data")
#check for Third party
		try:
			if self._find_data("span.seller-shipping-msg.font-semibold.u-textBlue"):
					sellers = self.driver.find_elements_by_css_selector("div.secondary-bot div.arrange.seller-container")
					for sell in sellers:
						if sell.find_element_by_css_selector("span.seller-shipping-msg.font-semibold.u-textBlue").get_attribute("innerHTML").encode('utf-8') == 'Walmart':
							self.set_price(aux_func.clean(sell.find_element_by_css_selector("span.Price-group").get_attribute('title')))
							break
			elif not self._find_data("a.font-bold.prod-SoldShipByMsg[href='http://help.walmart.com']"):
				self.set_third_party()

		except:
			self._log("Third party check failed")
#check Out of stock
		try:
			try:
				oos = self.driver.find_element_by_css_selector("span.copy-mini.display-block-xs.font-bold.u-textBlack").get_attribute("innerHTML")
			except:
				oos = "in stock"
			if "Out of stock" in oos:
				self.set_out_of_stock()
		except:
			self._log("Out of stock check failed")
		finally:
				self._kill_driver()
		return

	def _default(self):
		self._log("Unknown Competitor ID")
		return
