#!/usr/local/bin/python3

import requests
from tabulate import tabulate
import time
import curses

site_dict = [
    {'index':'1','site_name':'GOOGLE','url':'http://www.google.com','ip':'192.168.1.1'}
]

window = curses.initscr() 
curses.noecho()
curses.cbreak()
table_header = ['Index','Site Name','FQDN','status code','IP Address']

try:
    while(True):
        for site in site_dict:
            index = site['index']
            site_name = site['site_name']
            url = site['url']
            ip = site['ip']
            r = requests.get(url)
            localtime = time.asctime( time.localtime(time.time()) )
            table_data = [
                (index,site_name,url,r.status_code,ip)
                ]
            table= str(tabulate(table_data, headers=table_header, tablefmt='fancy',numalign='center',stralign='center'))
            window.addstr(0,0,str(localtime))
            window.addstr(1,0,table)
            window.refresh()        
            time.sleep(5)
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()


