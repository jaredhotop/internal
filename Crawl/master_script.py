import os
import csv


def aggr_uwritten():
    for file in os.listdir("/media/WebCrawl"):
        with open("/media/WebCrawl/unwritten_master.csv","w") as out_f:
            write = csv.writer(out_f,delimiter = ",")
            if file.endswith(".csv") and 'master' not in file:
                with open(os.path.join("/media/WebCrawl/",file),"r") as in_f:
                    read = csv.reader(in_f , delimiter=",")
                    for row in read:
                        write.writerow(row)
def aggr_valid_records():
    for file in os.listdir("/media/WebCrawl/outputs"):
        with open("/media/WebCrawl/outputs/valid_records_master.csv","w") as out_f:
            write = csv.writer(out_f,delimiter = ",")
            if file.endswith(".csv") and 'master' not in file:
                with open(os.path.join("/media/WebCrawl/outputs",file),"r") as in_f:
                    read = csv.reader(in_f , delimiter=",")
                    for row in read:
                        write.writerow(row)

aggr_uwritten()
aggr_valid_records()
