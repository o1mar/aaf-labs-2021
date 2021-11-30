import re
from tabulate import tabulate

def create(a, tables):
    a = re.sub(r"(,)|(INDEXED)", '', a)
    a = a.split()
    name = a[0]
    if name in tables.keys(): print("Table already exists")
    else:
       columns = a[1:]
       rows = []
       tb = [rows, columns]
       print('Table', name, 'has been created')
       return name, tb

def insert(a, tables):

    a = re.sub(r"(,)|(INTO)", '', a, flags=re.IGNORECASE)
    a = a.split()
    name = a[0]
    
    if name in tables.keys():
     tb = tables.get(name)
     row = a[1:]
     if len(row) == len(tb[1]):
         tb[0].append(row)
         tables.update({name: tb})
         #print (tabulate(tb[0], tb[1], tablefmt="grid"))
         print('1 row has been added')
     else: print("The amount of values must be equal the amount of columns!")
     return name, tb
     
    else: print("There is no such table")
    
def select(a, tables):
    a = re.sub(',', '', a)
    a = a.split()

    for i in range(0, len(a)): 
        if a[i] == 'from':
           name = a[i+1]
           curCol = a[:i] 
           condition = []
        try:
           if a[i+2] == 'where':
            condition = a[i+3:]
        except: pass

    if name in tables.keys():
     t = tables.get(name)
     tb = t.copy()
     rows, columns = tb

     if len(condition) == 3:
          if condition[1] == '=': condition[1] = '=='
          if condition[0] in columns and condition[2] in columns:
            i = 0
            selectedRows = []
            while i < len(rows):
                c = rows[i][columns.index(condition[0])], condition[1], rows[i][columns.index(condition[2])]
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          elif condition[0] in columns:
             i = 0
             selectedRows = []
             while i < len(rows):
                c = rows[i][columns.index(condition[0])], condition[1], condition[2]
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          elif condition[2] in columns:
             i = 0
             selectedRows = []
             while i < len(rows):
                c = condition[0], condition[1], rows[i][columns.index(condition[2])]
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          temp = []
          for i in curCol:
             row = []
             if i in columns:
                ind = columns.index(i)
                for j in range (len(selectedRows)):
                    row.append(selectedRows[j][ind])
             temp.append(row)
          selectedRows = temp
          selectedRows = list(zip(*selectedRows))
          print(tabulate(selectedRows, curCol, tablefmt="grid"))
     elif curCol[0] == '*': print(tabulate(rows, columns, tablefmt="grid"))
     else: 
         selectedRows = []
         for i in curCol:
          row = []
          if i in columns:
             ind = columns.index(i)
             for j in range (len(rows)):
              row.append(rows[j][ind])
          selectedRows.append(row)
         selectedRows = list(zip(*selectedRows))          
         print(tabulate(selectedRows, curCol, tablefmt="grid"))
        
def delete(a, tables):
    a = a.split()
    name = a[0]
    if name in tables.keys():
     tb = tables.get(name)
     rows, columns = tb
     if len(a)>1:
        if a[3] == '=': a[3] = '=='
        d = 0
        print(a[2], a[4])
        if a[2] in columns and a[4] in columns:
            i = 0
            while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 d += 1
                else: i +=1

        elif a[2] in columns:
             i = 0
             while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], a[4]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 d += 1
                else: i +=1

        elif a[4] in columns:
               i = 0
               while i < len(rows):
                c = a[2], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 d += 1
                else: i +=1
        tb[0] = rows
        tables.update({name: tb})
        print(d, 'rows have been deleted from the table', name)
        #print(tabulate(tb[0], tb[1], tablefmt="grid"))  
     else: 
         print('Table was deleted')
         tables.pop(name)
    else: print("There is no such table")
    return tables

