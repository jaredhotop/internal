# Competitor pricing crawler v1.0
# written by: Jayson Scruggs
# Property of Buchheit
import set_loc
import entry_class
import aux_func
import os
import csv

ip = aux_func.get_ip().split(".")
file_name = os.path.expanduser("/media/WebCrawl/inputs/tsclinks"+ip[3]+".csv")
search_arr = written_arr = []
with open(file_name,"r" )as f:
	r = csv.reader(f,delimiter = ",")
	for row in r:
		temp = entry_class.Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6],ip[3])
		search_arr.append(temp)
#set_cookies()
for obj in search_arr:
	for entry in written_arr:
		if obj.get_unique_id == entry.get_unique_id:
			obj.set_unique_id
	obj.crawl()
	obj.write_entry(os.path.expanduser("~/Documents/test_out"+ip[3]+".csv"))
	written_arr.append(obj)
	search_arr.pop()
os.rename(os.path.expanduser("~/Documents/test_out.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/outputs/test_out"+ip[3]+".csv"))
print("done")
