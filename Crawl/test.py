import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import entry_class

obj = entry_class.Entry('44','1234','4665',False,False,'1','https://www.sheplers.com/chippewa-mens-cordovan-cognac-7-engineer-boots---round-toe/036U56.html?dwvar_036U56_color=7051#start=3')
obj.crawl()
obj._print_readable()
