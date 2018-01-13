from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import aux_func
import csv
#from io import StringIO   #what is this line for?
#import sys   #what is this line for?
import os


class Entry:
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
		self.log_msg = None
		self.machine_ip = ip
		self.pagedata = None

	def write_entry(self, file):
		if (self.comp_price != None and self.comp_sale_price != None):
			self._log("Writing entry to file: " + file)
			with open(file, "a") as f:
				out = csv.writer(f, delimiter = ",")
				out.writerow(self._data_tup())
		else:
			self._log("Entry not written. comp_price or comp_sale_price is unset.")
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
			print(variables[i],":",values[i])
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
			self._log("Set competitor price to: " + price)
		else:
			self._log("Attempted to set competitor price as: {price} but it is not a number")
		return

	def set_sale_price(self,price):
		if isinstance(price, (int, long, float)):
			self.comp_sale_price = price
			self._log("Set competitor sale price to: " + price)
		else:
			self._log("Attempted to set competitor sale price to: {price} but it is not a number")
		return

	def set_shop_date(self):
		self.shop_date = now.strftime("%Y-%m-%d %H:%M:%S")
		return

	def set_third_party(self):
		self.comp_shop_third_party = True
		self.comp_match_id = 2
		self._log("Set link as third party")
		return

	def set_out_of_stock(self):
		self.comp_shop_out_of_stock = True
		self._log("Set item as \"out of stock\"")
		return

	def set_unique_id:
		self.unique_id = self.unique_id + '1'
		self._log("Corrected unique_id duplicate")
		return

	def _get_url(self):
		return str(self.url)

	def get_unique_id(self):
		return self.unique_id

	def _create_driver(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("user-data-dir=/home/test/.config/google-chrome")
		self.driver = webdriver.Chrome(os.path.expanduser('~/bin/chromedriver'),chrome_options = chrome_options)
		self._log("Driver created")
		return self.driver_path

	def _kill_driver(self):
		self.driver.quit()
		self._log("Driver destroyed")
		return

	def _log(self,log_msg,file= os.path.expanduser("/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/"+ip[3]+"self._log.log")):
		self.log_msg = self.Log_msg + " \n" + log_msg
		with open(file,"a") as f:
			f.write("Timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S") + " , sku: " + self.skum + " , Log Message: " + self.log_msg)
		print("Timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S") + " , sku: " + self.skum + " , Log Message: " + self.log_msg)
		return

	def crawl(self):
		self._log("Crawl intialized")
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
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _acehardware(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _basspro(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _blain(self):
		try:
			driver = self._create_driver()
		except:
			self._log("Driver failed to start")
		else:
			try:
				driver.get(self._get_url())
				self.pagedata = driver.page_source.encode('utf-8')
			except:
				self._log("Failed to retrieve url")
			else:
				self.set_shop_date()
				try:
					selectors = ["div.active-price>div.price>span","div.original-price>span.price>span"]
					for selector in selectors:
						price = clean(driver.find_element_by_css_selector().get_attribute("innerHTML"))
						if price:
							self.set_price(price)
							break
						else:
							continue
				except:
					self._log("Failed to retrieve competitor price using any known css selector")
				else:
					try:
						#https://www.farmandfleet.com/products/807682-blazer-international-led-emergency-mini-light-bar.html
						self.set_sale_price(clean(driver.find_element_by_css_selector("div.active-price.promo > div.price > span:not([class])").get_attribute("innerHTML"))
					except:
						self._log("No sale price found using current css selectors")
						self.set_sale_price("0.00")
					try:
						if not (EC.presence_of_element_located(BY.CSS_SELECTOR,"span.stock-msg.in-stock")):
							self.set_out_of_stock()
					except:
						pass
			finally:
				self._kill_driver()
		return

	def _bootbarn(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _cabela(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _dickeybub(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _home_depot(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _farm_and_home(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _lowes(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _menards(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _orscheln(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
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
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _shelper(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _tsc(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _valleyvet(self):
		self._create_driver()
		self._log("Competitor: {self.comp_id} not yet defined")
		self._kill_driver()
		return

	def _walmart(self):
		try:
			driver = self._create_driver()
		except:
			self._log("Driver failed to start")
		else:
			try:
				driver.get(self._get_url())
				self.pagedata = driver.page_source.encode('utf-8')
			except:
				self._log("Failed to retrieve url")
			else:
				self.set_shop_date()
				try:
					self.set_price(clean(driver.find_element_by_css_selector("span.display-inline-block.arrange-fit.Price.Price-enhanced.u-textNavyBlue").find_element_by_css_selector("span.Price-group").get_attribute("title")))
				except:
					self._log("Failed to retrieve competitor price using any known css selector")
				else:
					try:
						self.set_sale_price(clean(driver.find_element_by_css_selector("div.Price-old.display-inline-block.arrange-fill.font-normal.u-textNavyBlue.display-inline").find_element_by_css_selector("span.Price-group").get_attribute("title"))
					except:
						self._log("No sale price found using current css selectors")
						self.set_sale_price("0.00")
					try:
						check = EC.presence_of_element_located((By.CSS_SELECTOR, "a.font-bold.prod-SoldShipByMsg[href=http://help.walmart.com]"))
						if check != True:
							self.set_third_party()
					except:
						pass
					try:
						#https://www.walmart.com/ip/Holiday-Time-Net-Light-Set-Green-Wire-Blue-Bulbs-150-Count/21288309   //Out of stock link
						if (EC.presence_of_element_located(BY.CSS_SELECTOR,"span.copy-mini.display-block-xs.font-bold.u-textBlack[text=Out of stock]")):
							self.set_out_of_stock()
					except:
						pass
			finally:
				self._kill_driver()
		return

	def _default(self):
		self._log("Unknown Competitor ID")
		return
