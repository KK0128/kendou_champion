#!/usr/local/bin/python3

import requests
from tabulate import tabulate
import time
from time import sleep
from prettytable import PrettyTable
import curses

url = 'http://www.google.com'
table = PrettyTable(['site','status code','ping'])
window = curses.initscr() 
curses.noecho()
curses.cbreak()

try:
    while(True):
        r = requests.get(url)
        localtime = time.asctime( time.localtime(time.time()) )
        # print(str(r.status_code).ljust(10),end='\r')
        table_data = [(url,r.status_code,'ping')]
        # print(tabulate(table_data, headers=table_header, tablefmt='grid'))
        table.add_row([url,r.status_code,'ping'])
        # print(table)
        window.addstr(0,0,str(localtime))
        window.addstr(1,0,str(table))
        window.addstr(2,0,str(tabulate(table_data, headers=table_header, tablefmt='grid'))
        window.refresh()
        table.clear_rows()
        sleep(5)
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()


