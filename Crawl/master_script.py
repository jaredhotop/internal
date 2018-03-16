import os
import csv
import Queue

Q = Queue.Queue()

 def aggr_uwritten():
     for file in os.listdir("/media/WebCrawl"):
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

aggr_uwritten()
aggr_valid_records()
