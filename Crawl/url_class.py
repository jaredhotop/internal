from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import aux_func
import csv
import os

class URL:
    def __init__(self,sku,barcode,ip):
        self.sku = sku
        self.barcode = barcode
        self.url = None
        self.log_msg
        self.machine_ip = ip
        return

    def set_url(self,url):
        self.url = url
        return

    def create_entry_obj(self,comp_id,link_id="",manual="",shop_promo="",match_id=""):
        Entry(comp_id,link_id,self.sku,manual,shop_promo,match_id,self.url,self.machine_ip)

    def _walmart(self):
        self._log("Function has not been built out yet.")
        return

    def _home_depot(self):
        self._log("Function has not been built out yet.")
        return

    def _amazon(self):
        self._log("Function has not been built out yet.")
        return

    def _log(self,msg,file=os.path.expanduser("some default file")):
        self.log_msg = self.log_msg +"\n"+ msg
        with open(file,"a") as f:
			f.write("Timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S") + " , sku: " + self.skum + " , Log Message: " + self.log_msg)
		print("Timestamp: " + now.strftime("%Y-%m-%d %H:%M:%S") + " , sku: " + self.skum + " , Log Message: " + self.log_msg)
