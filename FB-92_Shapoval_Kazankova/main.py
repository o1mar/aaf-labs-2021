from tabulate import tabulate
import re
import ourparser as p
import comands as c

tables = {}

while True:
   str = input('> ')
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
     #print("create")
     names, tb = c.create(a)
     tables.update({names: tb})
     #print(tables)
    elif cmd == 2:
     #print("insert")
     name, tb = c.insert(a, tables)
     tables.update({name: tb})
     #print(tables)
    elif cmd == 3:
     #print("select")
     t = tables
     tcopy = dict(tables)
     #print (tcopy is tables)
     #print (t is tables)
     c.select(a, tcopy)
    elif cmd == 4:
     #print("delete")
     tables = c.delete(a, tables)
     #print(tables)
   except: print ('Something wrong in comands.py')

