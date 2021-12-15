import re
import sys
import ourparser as p
import comands as c
import numpy as np
from tabulate import tabulate

tables = {}



while True:
   str = ''
   print('-----------------------')
   for line in sys.stdin: 
       str+=line
       if ';' in line: 
           break
   #print(str, 'string')
   if re.match(r'EXIT', str, re.IGNORECASE) !=None:
     print("Thanks, bye")
     break
   try:
     inpt=p.text_cleaner(str)
   except: print("Something went wrong in text_cleaner")
   try:
     cmnd=p.comand_recog(inpt)
   except: print("Something went wrong in comand_recog")
   try:
     cmd = 0
     cmd, a =p.command_type(cmnd)
   except: print("Something went wrong in command_type")
   try:
   
    if cmd == 1:
     names, tb = c.create(a, tables)
     tables.update({names: tb})
    elif cmd == 2:
     name, tb = c.insert(a, tables)
     tables.update({name: tb})
    elif cmd == 3:
     
     c.select(a, tables)
    elif cmd == 4:
     tables = c.delete(a, tables)
   except: print ('Something wrong in comands.py')

