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
		self.unique_id = now.strftime("%Y%m%d")+match_id+sku
		self.comp_id = comp_id
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
		self.shop_date = self.creat_date
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
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-gpu")
		#chrome_driver = os.path.expanduser('~/Documents')+"\\chromedriver.exe"
		self.driver = webdriver.Chrome(os.path.expanduser('~/bin/chromedriver'),chrome_options = chrome_options)
		self.error = None

	def write_entry(self, file):
		with open(file, "a",newline='') as f:
			out = csv.writer(f, delimiter = ",")
			out.writerow(self._data_tup())

	def _print_readable(self):
		variables = ("unique_id", "comp_id", "comp_match", "comp_price", " \
		comp_sale_price", "comp_shop_leader", "comp_shop_notes", " \
		create_date", "created_by_tm", "last_update_date", "link_id", "\
		sku", "shop_date", "updated_by_tm", "reviewed", "reviewed_by", "\
		reviewed_date", "comp_shop_manual", "comp_shop_promo", "\
		comp_match_id","comp_shop_out_of_stock", "comp_shop_third_party", "url")
		values = self._data_tup()
		for i in range(len(variables)):
			print(variables[i],":",values[i])

	def _data_tup(self):
		return (self.unique_id, self.comp_id, self.comp_match, self.comp_price,  \
		self.comp_sale_price, self.comp_shop_leader, self.comp_shop_notes,  \
		self.create_date, self.created_by_tm, self.last_update_date, self.link_id, \
		self.sku, self.shop_date, self.updated_by_tm, self.reviewed, self.reviewed_by, \
		self.reviewed_date, self.comp_shop_manual, self.comp_shop_promo, \
		self.comp_match_id,self.comp_shop_out_of_stock, self.comp_shop_third_party, self.url)

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
		return

	def _menards(self):
		return

	def _ruralking(self):
		return

	def _walmart(self):
		print('hello world')
		return

	def crawl(self):
		switch = {
			'1' : self._academy,
			'2' : self._basspro,
			'3' : self._blain,
			'9' : self._walmart,
			'10': self._cabela,
			'37': self._acehardware,
			'43': self._bootbarn,


		}
		switch[self.comp_id]()
		return

search_arr = []
with open("test.csv","r") as f:
	r = csv.reader(f,delimiter=",")
	for row in r:
		obj = Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
		search_arr.append(obj)

for obj in search_arr:
	obj.crawl()
