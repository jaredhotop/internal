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
from datetime import datetime
from tendo import singleton
from email.mime.text import MIMEText as Etext
import requests



test_mach = 0
email_crash_report = 1
sys.path.append( os.path.expanduser("~/Documents"))
try:
    from crawlconfig import *
except:
    pass



def status_post(status):
    try:
        r = requests.post("http://10.0.5.201:5000",data = {'status':status,'ip':ip[3],'time':'{}'.format(datetime.now().strftime("%m/%d %H:%M:%S"))})
    except:
        print("Failed to post to Jon's server")
    try:
        r = requests.post("http://10.0.10.19:5000",data = {'status':status,'ip':ip[3],'time':'{}'.format(datetime.now().strftime("%m/%d %H:%M:%S"))})
    except:
        print("Failed to post to Dawn's server")
    try:
        r = requests.post("http://10.0.10.246:5000",data = {'status':status,'ip':ip[3],'time':'{}'.format(datetime.now().strftime("%m/%d %H:%M:%S"))})
    except:
        print("Failed to post to Jayson's server")

def append_to_log(message,err=None,file = os.path.expanduser('~/Documents/run.log'),email=True):
    print(message)
    with open(file, 'a') as f:
        f.write(message)
    status_post("Error")
    if email_crash_report:
        if email:
            msg =Etext("{}\n Machine-{}\n\n{}".format(message,ip[3],err))
            msg['Subject'] = "Machine-{}".format(ip[3])
            server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
    return

ip = aux_func.get_ip().split(".")

me = singleton.SingleInstance()
status_post("Started")

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('buchheit.emailer@gmail.com','!@#$%^&*()')

try:
    with open(os.path.expanduser("~/Documents/run.log"),'a') as f:
        f.write("{}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
except:
    print("Crawl failed to log start time")

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
        msg['Subject'] = "Generic Script Failure"
        server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
        server.quit()
    else:
        raise
finally:
    try:
        if os.path.exists("/media/WebCrawl/unwritten/unwritten_%s.csv" %ip[3]):
            os.remove(os.path.expanduser("/media/WebCrawl/unwritten/unwritten_%s.csv" %ip[3]))
        if os.path.exists("/media/WebCrawl/outputs/valid_records_%s.csv" %ip[3]):
            os.remove(os.path.expanduser("/media/WebCrawl/outputs/valid_records_%s.csv" %ip[3]))
        if os.path.exists("/media/WebCrawl/logs/machine%s.log" %ip[3]):
            os.remove(os.path.expanduser("/media/WebCrawl/logs/machine%s.log" %ip[3]))
    except:
        err = traceback.format_exc()
        append_to_log("Failed to delete previous files!",err = err)
    try:
        err = False
        try:
            if os.path.exists(os.path.expanduser("~/Documents/valid_records_%s.csv" %ip[3])):
                shutil.move(os.path.expanduser("~/Documents/valid_records_%s.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/outputs/valid_records_%s.csv" %ip[3]))
        except:
            err = traceback.format_exc()
            append_to_log('Failed to move Valid records.',err = err)
        try:
            if os.path.exists(os.path.expanduser("~/Documents/unwritten_%s.csv" %ip[3])):
                shutil.move(os.path.expanduser("~/Documents/unwritten_%s.csv" %ip[3]),os.path.expanduser("/media/WebCrawl/unwritten/unwritten_%s.csv" %ip[3]))
        except:
            err = traceback.format_exc()
            append_to_log('Failed to move unwritten.',err = err)
        try:
            shutil.move(os.path.expanduser("~/Documents/machine%s.log" %ip[3]),os.path.expanduser("/media/WebCrawl/logs/machine%s.log" %ip[3]))
        except:
            err = traceback.format_exc()
            append_to_log('Failed to move log file.',err = err)
        try:
            for file in os.listdir('/tmp'):
                if 'tmpaddon' in file:
                    os.remove('/tmp/{}'.format(file))
        except:
            err = traceback.format_exc()
            append_to_log('Error deleting temp files.',err = err)
        server.quit()
        if not err:
            status_post("Completed")
        print("Crawl Complete: {}".format(datetime.now().strftime("%m/%d/%Y")))
    except:
        if email_crash_report:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('buchheit.emailer@gmail.com','!@#$%^&*()')
            msg =Etext("Failed to move files on Clone {}:\n{}".format(ip[3],traceback.format_exc()))
            msg['Subject'] = "Failed File Movement"
            server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
            server.quit()
