import socket
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

def get_ip():
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			s.connect(('10.255.255.255', 1))
			IP = s.getsockname()[0]
		except:
			IP = '127.0.0.1'
		finally:
			s.close()
		return IP

def clean(string):
	non_decimal = re.compile(r'[^\d.]+')
	string = non_decimal.sub('', string)
	string = string.strip()
	string = string.replace("$","")
	string = string.split('-')
	if '.' not in string[0]:
		string[0] = string[0][:-2] + '.' +string[0][-2:]
	return float(string[0])
