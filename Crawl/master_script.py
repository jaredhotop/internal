import os
import csv



for file in os.listdir("/media/WebCrawl"):
    if file.endswith(".csv"):
        with open("/media/WebCrawl/unwritten_master.csv","w") as out_f:
            write = csv.writer(out_f,delimiter = ",")
            with open(os.path.join("/media/WebCrawl/",file),"r") as in_f:
                read = csv.reader(in_f , delimiter=",")
                for row in read:
                    write.writerow(row)
