from flask import Flask, request
import json
import os

app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
@app.route('/',methods=['POST'])
def result():
    if not os.path.isdir("C:/Program Files/crawl_status"):
        os.mkdir("C:/Program Files/crawl_status")
    with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
        prev = json.load(inf)
    for entry in prev:
        if request.form['ip'] == entry['ip']:
            entry['status'] = request.form['status']
            with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'w') as outf:
                json.dump(prev,outf)
            break
    return 'Received'


app.run('0.0.0.0')
