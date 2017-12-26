from datetime import datetime
import csv
from io import StringIO
import sys


#if __name__ == "__main__":
class Entry:
	def __init__(self, id, comp_id, link_id, sku, shop_prompt, match_id, url):
		future_date = datetime(3000, 12, 31, 1, 0, 0)
		now = datetime.now()
		self.unique_id = id
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
		self.shop_date = None
		self.updated_by_tm = 8
		self.reviewed = 0
		self.reviewed_by = 4
		self.reviewed_date = future_date.strftime("%Y-%m-%d %H:%M:%S")
		self.comp_shop_manual = False
		self.comp_shop_prompt = shop_prompt
		self.comp_match_id = match_id
		self.comp_shop_out_of_stock = False
		self.comp_shop_third_party = False
		self.url = url
		
	def write_entry(self, file):
	#	if(self.comp_price != none && self.shop_date != none)
		with open(file, "a",newline='') as f:
			out = csv.writer(f, delimiter = ",")
			out.writerow(self._data_tup())
	
	def _print_readable(self):
		variables = ("unique_id", "comp_id", "comp_match", "comp_price", " \
		comp_sale_price", "comp_shop_leader", "comp_shop_notes", " \
		create_date", "created_by_tm", "last_update_date", "link_id", "\
		sku", "shop_date", "updated_by_tm", "reviewed", "reviewed_by", "\
		reviewed_date", "comp_shop_manual", "comp_shop_prompt", "\
		comp_match_id","comp_shop_out_of_stock", "comp_shop_third_party", "url")
		values = self._data_tup()
		for i in range(len(variables)):
			print(variables[i],":",values[i])
			
	def _data_tup(self):
		return (self.unique_id, self.comp_id, self.comp_match, self.comp_price,  \
		self.comp_sale_price, self.comp_shop_leader, self.comp_shop_notes,  \
		self.create_date, self.created_by_tm, self.last_update_date, self.link_id, \
		self.sku, self.shop_date, self.updated_by_tm, self.reviewed, self.reviewed_by, \
		self.reviewed_date, self.comp_shop_manual, self.comp_shop_prompt, \
		self.comp_match_id,self.comp_shop_out_of_stock, self.comp_shop_third_party, self.url)
		
	def set_price(self,price):
		self.comp_price = price
		
	def set_sale_price(self,price):
		self.comp_sale_price = price
		
	def set_shop_date(self):
		self.shop_date = now.strftime("%Y-%m-%d %H:%M:%S")
	
#review this for proper variables access
	def set_third_party(self):
		self.comp_shop_third_party = True
		self.comp_match_id = 2
		
	def set_out_of_stock(self):
		self.comp_shop_out_of_stock = True

		
		
		
		
