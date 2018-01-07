#import crawl_class
import set_loc
import entry_class
import os
import csv

ip = get_ip().split(".")
file_name = os.path.expanduser("/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/testrun"+ip[3]+".csv")
search_arr = []
with open(file_name,"r" )as f:
	r = csv.reader(f,delimiter = ",")
	for row in r:
		temp = entry_class.Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6],ip[3])
		search_arr.append(temp)
#set_cookies()
for obj in search_arr:
	obj.crawl()
	break
	obj.write_entry(os.path.expanduser("/media/p/IT/Data Warehosuse/Price Change Reports/Buyer Runs/test_out"+ip[3]+".csv"))
print("done")
