import socket
import re

def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

def clean(string):
    string = string.replace("to","-")
    string = string.strip()
    string = string.replace("$","")
    string = string.split('-')
    if '.' not in string[0]:
        non_decimal = re.compile(r'[^\d.]+') # remove all alpha chars
        string[0] = non_decimal.sub('', string[0])
        string = string[0][:-2] + '.' + string[0][-2:]
    return float(string)
