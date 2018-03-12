# Competitor pricing crawler v1.0
# written by: Jayson Scruggs
# Property of Buchheit
import set_loc
import entry_class_logger
import aux_func
import os
import csv
import smtplib
import sys
sys.path.append( os.path.expanduser("~/Documents"))
try:
	from crawlconfig import *
except:
	test_mach = 0
	email_crash_report = 1
import time

try:
    ip = aux_func.get_ip().split(".")
    file_name = os.path.expanduser("/media/WebCrawl/inputs/tsclinks%s.csv" %ip[3])
    search_arr = []
    with open(file_name,"r" )as f:
        r = csv.reader(f,delimiter = ",")
        for row in r:
            temp = entry_class_logger.Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6],ip[3])
            search_arr.append(temp)
	written_arr = []
    while search_arr:
		obj = search_arr[0]
		for entry in written_arr:
			if obj.get_unique_id == entry:
				obj.set_unique_id
			obj.crawl()
		obj.write_entry(os.path.expanduser("~/Documents/valid_records_%s.csv" %ip[3]))
		written_arr.append(obj.unique_id)
		search_arr = search_arr[1:]
		print(obj)
		print("search: ", len(search_arr))
		print("written: ", len(written_arr))
    os.rename(os.path.expanduser("~/Documents/unwritten_%s.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/unwritten_%s.csv" %ip[3]))
    os.rename(os.path.expanduser("~/Documents/valid_records_%s.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/outputs/valid_records_%s.csv" %ip[3]))
except:
    if email_crash_report:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('buchheit.emailer@gmail.com','!@#$%^&*()')
        msg ="Script Failed on Clone %s " %ip[3]
        server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg)
        server.quit()
    else:
        raise
print("Crawl Complete")
