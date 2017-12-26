from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
import socket
import os



chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_driver = os.path.expanduser('~/documents')+"\\chromedriver.exe"
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path = chrome_driver)
driver.get("https://www.google.com")
html = driver.page_source
print(html)

#def get_ip():
 #   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 #   try:
 #       # doesn't even have to be reachable
 #       s.connect(('10.255.255.255', 1))
 #       IP = s.getsockname()[0]
 #   except:
 #       IP = '127.0.0.1'
 #   finally:
 #       s.close()
 #   return IP
	
#var = get_ip()
#print (var)