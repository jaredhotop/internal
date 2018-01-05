import crawl_class
import entry_class
import socket
import os
import csv

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
 
 
ip = get_ip().split(".")
file_name = "test.csv"
#file_name = "price_shop_list_" + ip[3]+".csv"
#file_name = os.path.join("P:","IT","Data Warehouse","Price Change Reports", "Buyer Runs",file_name)
search_arr = []
with open(file_name,"r" )as f:
	r = csv.reader(f,delimiter = ",")
	for row in r:
		temp = entry_class.Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
		search_arr.append(temp)
		
for obj in search_arr:
	search = crawl_class.Crawl(obj.get_url())
	print(search._get_page_data())
	with open("test.txt", "w") as f:
		f.write(search._get_page_data())
	break		
		


