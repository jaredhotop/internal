from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from io import StringIO
import sys
import os


class Entry:
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
		self.error = None

	def write_entry(self, file):
		with open(file, "a") as f:
			out = csv.writer(f, delimiter = ",")
			out.writerow(self._data_tup())

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

	def _data_tup(self):
		return (self.unique_id, self.comp_id, self.comp_match, self.comp_price,  \
		self.comp_sale_price, self.comp_shop_leader, self.comp_shop_notes,  \
		self.create_date, self.created_by_tm, self.last_update_date, self.link_id, \
		self.sku, self.shop_date, self.updated_by_tm, self.reviewed, self.reviewed_by, \
		self.reviewed_date, self.comp_shop_manual, self.comp_shop_promo, \
		self.comp_match_id,self.comp_shop_out_of_stock, self.comp_shop_third_party)

	def set_price(self,price):
		self.comp_price = price

	def set_sale_price(self,price):
		self.comp_sale_price = price

	def set_shop_date(self):
		self.shop_date = now.strftime("%Y-%m-%d %H:%M:%S")

	def set_third_party(self):
		self.comp_shop_third_party = True
		self.comp_match_id = 2

	def set_out_of_stock(self):
		self.comp_shop_out_of_stock = True

	def get_url(self):
		return str(self.url)

	def _create_driver(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-gpu")
		chrome_options.add_argument("user-data-dir=/home/test/.config/google-chrome")
		self.driver = webdriver.Chrome(os.path.expanduser('~/bin/chromedriver'),chrome_options = chrome_options)
		return self.driver_path

	def _kill_driver(self):
		self.driver.quit()


#Competitor specific methods

	def _academy(self):
		return

	def _acehardware(self):
		return

	def _basspro(self):
		return

	def _blain(self):
		return

	def _bootbarn(self):
		return

	def _cabela(self):
		print('cabelas')
		return

	def _dickeybub(self):
		return

	def _home_depot(self):
		return

	def _farm_and_home(self):
		return

	def _lowes(self):
		return

	def _menards(self):
		return

	def _orscheln(self):
		return

	def _ruralking(self):
		return

	def _sears(self):
		return

	def _shelper(self):
		return

	def _tsc(self):
		return

	def _valleyvet(self):
		return

	def _walmart(self):
		print('hello world')
		return



	def _default(self):
		self.error = "Invalid Competitor ID"
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
