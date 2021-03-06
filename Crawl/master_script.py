#Master Aggregating script
# written by: Jayson Scruggs
# Property of Buchheit
import os
import csv
import Queue
from email.mime.text import MIMEText as Etext
import smtplib
import traceback
import shutil

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('','')
Q = Queue.Queue()

def aggr_uwritten():
    for file in os.listdir("/media/WebCrawl/unwritten"):
        if file.endswith(".csv") and 'master' not in file and '255' not in file:
            with open(os.path.join("/media/WebCrawl/unwritten/",file),"r") as in_f:
                read = csv.reader(in_f , delimiter=",")
                for row in read:
                    Q.put(row)
    with open("/media/WebCrawl/unwritten/unwritten_master.csv","w") as out_f:
        write = csv.writer(out_f,delimiter = ",")
        while not Q.empty():
            write.writerow(Q.get())

def aggr_valid_records():
    for file in os.listdir("/media/WebCrawl/outputs"):
        if file.endswith(".csv") and 'master' not in file and '255' not in file:
            with open(os.path.join("/media/WebCrawl/outputs",file),"r") as in_f:
                read = csv.reader(in_f , delimiter=",")
                for row in read:
                    Q.put(row)
            shutil.copy("/media/WebCrawl/outputs/{}".format(file),os.path.expanduser("/media/WebCrawl/logs/"))
            os.remove("/media/WebCrawl/outputs/{}".format(file))
    with open("/media/WebCrawl/outputs/valid_records_master.csv","w") as out_f:
        write = csv.writer(out_f,delimiter = ",")
        while not Q.empty():
            write.writerow(Q.get())
try:
    aggr_uwritten()
except:
    msg =Etext("Master failed to aggregate unwritten:\n{}".format(traceback.format_exc()))
    msg['Subject'] = "Master Failed to Aggregate Unwritten"
    server.sendmail('','',msg.as_string())
try:
    aggr_valid_records()
except:
    msg =Etext("Master failed to aggregate valid records:\n{}".format(traceback.format_exc()))
    msg['Subject'] = "Master Failed to Aggreagate Valid Records"
    server.sendmail('','',msg.as_string())
finally:
    server.quit()
