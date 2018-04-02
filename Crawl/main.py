# Competitor pricing crawler v1.0
# written by: Jayson Scruggs
# Property of Buchheit
import entry_class
import aux_func
import os
import csv
import smtplib
import sys
import shutil
import traceback
from tendo import singleton
from email.mime.text import MIMEText as Etext
sys.path.append( os.path.expanduser("~/Documents"))
try:
    from crawlconfig import *
except:
    test_mach = 0
    email_crash_report = 1
import time


me = singleton.SingleInstance()
ip = aux_func.get_ip().split(".")
try:
    os.remove(os.path.expanduser("/media/WebCrawl/unwritten/unwritten_%s.csv" %ip[3]))
    os.remove(os.path.expanduser("/media/WebCrawl/outputs/valid_records_%s.csv" %ip[3]))
except:
    print("Failed to delete previous files!")
    # server = smtplib.SMTP('smtp.gmail.com',587)
    # server.starttls()
    # server.login('buchheit.emailer@gmail.com','!@#$%^&*()')
    # msg =Etext("Script Failed to delete previous files on Clone {}:\n{}".format(ip[3],traceback.format_exc()))
    # msg['Subject'] = "Crawl Error"
    # server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
    # server.quit()

try:
    file_name = os.path.expanduser("/media/WebCrawl/inputs/price_shop_%s.csv" %ip[3])
    search_arr = []
    with open(file_name,"r" )as f:
        r = csv.reader(f,delimiter = ",")
        for row in r:
            temp = entry_class.Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6],ip[3])
            search_arr.append(temp)
    written_arr = []
    while search_arr:
        obj = search_arr[0]
        for entry in written_arr:
            if obj.unique_id == entry:
                obj.set_unique_id
        obj.crawl()
        obj.write_entry(os.path.expanduser("~/Documents/valid_records_%s.csv" %ip[3]))
        written_arr.append(obj.unique_id)
        search_arr = search_arr[1:]
        print(obj)
        del obj
        print("search: ", len(search_arr))
        print("written: ", len(written_arr))
except:
    if email_crash_report:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('buchheit.emailer@gmail.com','!@#$%^&*()')
        msg =Etext("Script Failed on Clone {}:\n{}".format(ip[3],traceback.format_exc()))
        msg['Subject']
        server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
        server.quit()
    else:
        raise
finally:
    try:
        shutil.move(os.path.expanduser("~/Documents/unwritten_%s.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/unwritten/unwritten_%s.csv" %ip[3]))
        shutil.move(os.path.expanduser("~/Documents/valid_records_%s.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/outputs/valid_records_%s.csv" %ip[3]))
    except IOError:
        pass
    print("Crawl Complete")
