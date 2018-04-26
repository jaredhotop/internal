from appJar import gui
import json
import os
import time

app=gui("WebCrawl Status")
app.setSticky("news")
app.setExpand("both")

def update():
    with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
        status = json.load(inf)
    row_count = 0
    for stat in status:
        try:
            app.getLabel("mach{}".format(stat['ip']))
        except:
            app.addLabel("mach{}".format(stat['ip']),"Machine {}".format(stat['ip']),row_count,0)
            app.addLabel("status{}".format(stat['ip']),stat['status'],row_count,1)
            app.addLabel("time{}".format(stat['ip']),stat['time'],row_count,2)
        app.setLabel("mach{}".format(stat['ip']),"Machine {}".format(stat['ip']))
        app.setLabel("status{}".format(stat['ip']),stat['status'])
        app.setLabel("time{}".format(stat['ip']),stat['time'])
        app.setLabelBg("status{}".format(stat['ip']),"white")
        if 'Not Started' in stat['status']:
            app.setLabelBg("status{}".format(stat['ip']),"red")
        elif 'Started' in stat['status']:
            app.setLabelBg("status{}".format(stat['ip']),"green")
        row_count += 1



with open(os.path.expanduser("C:/Program Files/crawl_status/current_status.txt"),'r') as inf:
    status = json.load(inf)
row_count = 0
for stat in status:
    app.addLabel("mach{}".format(stat['ip']),"Machine {}".format(stat['ip']),row_count,0)
    app.addLabel("status{}".format(stat['ip']),stat['status'],row_count,1)
    app.addLabel("time{}".format(stat['ip']),stat['time'],row_count,2)
    if 'Not Started' in stat['status']:
        app.setLabelBg("status{}".format(stat['ip']),"red")
    elif 'Started' in stat['status']:
        app.setLabelBg("status{}".format(stat['ip']),"green")
    row_count += 1
app.setPollTime(3)
app.registerEvent(update)
app.go()
