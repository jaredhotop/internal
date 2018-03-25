#Master Aggregating script
# written by: Jayson Scruggs
# Property of Buchheit
import os
import csv
import Queue
from email.mime.text import MIMEText as Etext
import smtplib

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('buchheit.emailer@gmail.com','!@#$%^&*()')
Q = Queue.Queue()

def aggr_uwritten():
    for file in os.listdir("/media/WebCrawl/unwritten"):
        if file.endswith(".csv") and 'master' not in file:
            with open(os.path.join("/media/WebCrawl/unwritten/",file),"r") as in_f:
                read = csv.reader(in_f , delimiter=",")
                for row in read:
                    Q.put(row)
    with open("/media/WebCrawl/unwritten_master.csv","w") as out_f:
        write = csv.writer(out_f,delimiter = ",")
        while not Q.empty():
            write.writerow(Q.get())

def aggr_valid_records():
    for file in os.listdir("/media/WebCrawl/outputs"):
        if file.endswith(".csv") and 'master' not in file:
            with open(os.path.join("/media/WebCrawl/outputs",file),"r") as in_f:
                read = csv.reader(in_f , delimiter=",")
                for row in read:
                    Q.put(row)
    with open("/media/WebCrawl/outputs/valid_records_master.csv","w") as out_f:
        write = csv.writer(out_f,delimiter = ",")
        while not Q.empty():
            write.writerow(Q.get())
try:
    aggr_uwritten()
except:
    msg =Etext("Master failed to aggregate unwritten:\n{}".format(traceback.format_exc()))
    msg['Subject'] = "Master Failed to Aggregate Unwritten"
    server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
try:
    aggr_valid_records()
except:
    msg =Etext("Master failed to aggregate valid records:\n{}".format(traceback.format_exc()))
    msg['Subject'] = "Master Failed to Aggreagate Valid Records"
    server.sendmail('buchheit.emailer@gmail.com','jayson.scruggs.work@gmail.com',msg.as_string())
finally:
    server.quit()
