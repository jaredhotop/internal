from flask import Flask, request
import json
import os
import threading
import time
from datetime import datetime

def daemon():
    while True:
        if datetime.now().strftime("%H:%M") == "04:00":
            with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
                data = json.load(inf)
            for entry in data:
                if entry["status"] != "Started":
                    entry['status'] = "Not Started"
                    entry['time'] = "{} 00:00:00".format(datetime.now().strftime("%m/%d"))
            with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'w') as outf:
                json.dump(data,outf)
            time.sleep(36000)
        else:
            time.sleep(30)
d = threading.Thread(name='daemon', target=daemon)
d.daemon = True
d.start()

app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
@app.route('/',methods=['POST'])
def result():
    if not os.path.isdir("C:/Program Files/crawl_status"):
        os.mkdir("C:/Program Files/crawl_status")
    try:
        with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
            prev = json.load(inf)
    except:
        prev = []
    for entry in prev:
        if request.form['ip'] == entry['ip']:
            entry['status'] = request.form['status']
            entry['time'] = request.form['time']
            with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'w') as outf:
                json.dump(prev,outf)
            break
    else:
        prev.append(request.form)
        with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'w') as outf:
            json.dump(prev,outf)
    return 'Received'

app.run('0.0.0.0')
