from appJar import gui
import json
import os
import time

app=gui("WebCrawl Status",'400x400')
app.setSticky("news")
app.setExpand("both")

def update():
    with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
        status = json.load(inf)
    row_count = 0
    for stat in status:
        app.setLabel("mach{}".format(stat['ip']),"Machine {}".format(stat['ip']))
        app.setLabel("status{}".format(stat['ip']),stat['status'])
        app.setLabelBg("status{}".format(stat['ip']),"white")
        if 'Not Started' in stat['status']:
            app.setLabelBg("status{}".format(stat['ip']),"red")
        elif 'Started' in stat['status']:
            app.setLabelBg("status{}".format(stat['ip']),"green")
        row_count += 1



with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
    status = json.load(inf)
app.addButton("Refresh",update,0,2)
row_count = 0
for stat in status:
    app.addLabel("mach{}".format(stat['ip']),"Machine {}".format(stat['ip']),row_count,0,1)
    app.addLabel("status{}".format(stat['ip']),stat['status'],row_count,1,2)
    if 'Not Started' in stat['status']:
        app.setLabelBg("status{}".format(stat['ip']),"red")
    elif 'Started' in stat['status']:
        app.setLabelBg("status{}".format(stat['ip']),"green")
    row_count += 1

app.registerEvent(update)
app.go()
