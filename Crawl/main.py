#import crawl_class
import set_loc
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
file_name = os.path.expanduser("/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/testrun"+ip[3]+".csv")
search_arr = []
with open(file_name,"r" )as f:
	r = csv.reader(f,delimiter = ",")
	for row in r:
		temp = entry_class.Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
		search_arr.append(temp)
#set_cookies()
for obj in search_arr:
	obj.crawl()
	break
	obj.write_entry(os.path.expanduser("/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/test_out"+ip[3]+".csv"))
print("done")
